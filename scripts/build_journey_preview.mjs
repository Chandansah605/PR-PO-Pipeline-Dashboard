import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repo = resolve(import.meta.dirname, '..');
const boardPath = resolve(repo, 'journey-board.html');
const previewPath = resolve(repo, 'journey-preview.html');
const proxyUrl = 'https://ssg-prpo-proxy-h4cvfegaduftedhz.uaenorth-01.azurewebsites.net/api/dataset';
const org = 'https://operations-ifahr-live.crm15.dynamics.com';
const api = `${org}/api/data/v9.2`;
const formatted = '@OData.Community.Display.V1.FormattedValue';

const token = JSON.parse(execFileSync('powershell.exe', [
  '-NoProfile', '-Command', `az account get-access-token --resource ${org} -o json`
], { encoding: 'utf8' })).accessToken;

const authHeaders = {
  Authorization: `Bearer ${token}`,
  Accept: 'application/json',
  Prefer: 'odata.maxpagesize=5000,odata.include-annotations="OData.Community.Display.V1.FormattedValue"'
};

async function json(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}: ${url}`);
  return response.json();
}

async function paged(url, headers = authHeaders) {
  const rows = [];
  while (url) {
    const page = await json(url, { headers });
    rows.push(...(page.value || []));
    url = page['@odata.nextLink'];
  }
  return rows;
}

function chunks(values, size) {
  const result = [];
  for (let i = 0; i < values.length; i += size) result.push(values.slice(i, i + size));
  return result;
}

async function pool(groups, worker, width = 4) {
  const out = [];
  let cursor = 0;
  async function run() {
    while (cursor < groups.length) {
      const index = cursor++;
      out[index] = await worker(groups[index]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(width, groups.length) }, run));
  return out.flat();
}

const norm = value => String(value || '').trim().toUpperCase();
const key = (company, number) => `${String(company || '').trim().toLowerCase()}|${norm(number)}`;
const clean = value => {
  const text = String(value || '').trim();
  return !text || /^0+$/.test(text) || /^\d+$/.test(text) ? 'not recorded' : text;
};
const validDate = value => {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) || date.getUTCFullYear() <= 1900 ? null : date;
};
const calendarDays = (a, b) => a && b ? Math.max(0, Math.floor((b - a) / 86400000)) : null;
const workingDays = (a, b) => {
  if (!a || !b) return null;
  const cursor = new Date(Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate()));
  const end = new Date(Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate()));
  let count = 0;
  while (cursor < end) {
    cursor.setUTCDate(cursor.getUTCDate() + 1);
    if (![0, 6].includes(cursor.getUTCDay())) count++;
  }
  return count;
};
const median = values => {
  const sorted = values.filter(Number.isFinite).sort((a, b) => a - b);
  if (!sorted.length) return null;
  const m = sorted.length >> 1;
  return sorted.length % 2 ? sorted[m] : (sorted[m - 1] + sorted[m]) / 2;
};
const percentile = (values, p) => {
  const sorted = values.filter(Number.isFinite).sort((a, b) => a - b);
  return sorted.length ? sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * p / 100) - 1)] : null;
};
const one = value => value == null ? null : +Number(value).toFixed(1);

const divisionByDepartment = new Map([
  ['building services', 'Facilities Management'],
  ['landscaping services', 'Facilities Management'],
  ['contracted cleaning services', 'Facilities Management'],
  ['leisure services', 'Facilities Management'],
  ['security services', 'Facilities Management'],
  ['concierge services', 'Facilities Management'],
  ['home maintenance services', 'Home Services'],
  ['housekeeping services', 'Home Services'],
  ['laundry services', 'Home Services'],
  ['fitout services', 'FitOut Solutions'],
  ['surveying services', 'FitOut Solutions'],
  ['accounts & tax', 'Factory — Head Office'],
  ['finance', 'Factory — Head Office'],
  ['procurement', 'Factory — Head Office'],
  ['marketing', 'Factory — Head Office'],
  ['call centre', 'Factory — Head Office'],
  ['stationery', 'Factory — Head Office'],
  ['office support', 'Factory — Head Office'],
  ['it', 'Factory — Head Office'],
  ['company secretary', 'Factory — Head Office'],
  ['qhse', 'Factory — Head Office'],
  ['hr', 'Factory — Head Office'],
  ['risk control', 'Factory — Head Office'],
  ['accomodation services', 'Factory — Head Office'],
  ['accommodation services', 'Factory — Head Office'],
  ['transportation', 'Factory — Head Office']
]);
const departmentsByDivision = {
  'Facilities Management': ['Building Services', 'Landscaping Services', 'Contracted Cleaning Services', 'Leisure Services', 'Security Services', 'Concierge Services'],
  'Home Services': ['Home Maintenance Services', 'Housekeeping Services', 'Laundry Services'],
  'FitOut Solutions': ['FitOut Services', 'Surveying Services'],
  'Factory — Head Office': ['Finance', 'Procurement', 'Marketing', 'Call Centre', 'Stationery', 'Office Support', 'IT', 'Company Secretary', 'QHSE', 'HR', 'Risk Control']
};

function divisionOf(department, quoteDivision) {
  const departmentMatch = divisionByDepartment.get(String(department || '').trim().toLowerCase());
  if (departmentMatch) return departmentMatch;
  const source = String(quoteDivision || '').toLowerCase();
  if (source.includes('facilit')) return 'Facilities Management';
  if (source.includes('home')) return 'Home Services';
  if (source.includes('fit')) return 'FitOut Solutions';
  if (source.includes('factory') || source.includes('head office')) return 'Factory — Head Office';
  return 'Division not recorded';
}

function gateOf(step) {
  const value = String(step || '').trim();
  const map = {
    'Sourcing': 'PR to procurement',
    'PR In Review': 'PR to procurement',
    'RFQ to suppliers': 'RFQ to supplier',
    'Qt received & Logged': 'Quotation received',
    'Qt Shared to Op': 'Operations confirm',
    'OP confirms material': 'Operations confirm',
    'Unit Price Updated': 'Unit price updated',
    'Priced — awaiting approval': 'Price written back to CRM',
    'Dep Managers': 'Department approval',
    'Finance': 'Finance approval',
    'Director': 'Director approval',
    'CEO': 'CEO approval'
  };
  return map[value] || 'approval — unmapped';
}

function nextAction(gate) {
  const actions = {
    'PR to procurement': 'Procurement: start sourcing and record the next step.',
    'RFQ to supplier': 'Procurement: issue the supplier RFQ.',
    'Quotation received': 'Procurement: log the supplier quotation.',
    'Operations confirm': 'Operations: confirm the material or scope.',
    'Unit price updated': 'Procurement: write the agreed cost into CRM.',
    'Price written back to CRM': 'Commercial: send the quote to the customer.',
    'Department approval': 'Department head: approve or return with a reason.',
    'Finance approval': 'Finance: review and release the requisition.',
    'Director approval': 'Director: approve or return with a reason.',
    'CEO approval': 'CEO: approve or return with a reason.',
    'approval — unmapped': 'Procurement: map this approval step before acting.'
  };
  return actions[gate] || 'Owner: progress this item and record the next step.';
}

function summariseRecords(records) {
  const ages = records.map(row => row.waitedWd).filter(Number.isFinite);
  const within = ages.length ? +(ages.filter(value => value <= 10).length / ages.length * 100).toFixed(1) : 0;
  const legs = [[], [], []];
  for (const row of records) {
    const gate = row.gate;
    const index = gate === 'PR to procurement' ? 0
      : ['Department approval', 'Finance approval', 'Director approval', 'CEO approval'].includes(gate) ? 2 : 1;
    if (Number.isFinite(row.waitedWd)) legs[index].push(row.waitedWd);
  }
  return {
    count: records.length,
    medianWd: one(median(ages)) || 0,
    p90Wd: one(percentile(ages, 90)) || 0,
    within10Pct: within,
    legs: legs.map(values => one(median(values)) || 0),
    stuck: legs.map(values => ({
      n: values.length,
      medianAgeWd: one(median(values)) || 0,
      oldestWd: values.length ? Math.max(...values) : 0,
      over20: values.filter(value => value > 20).length
    }))
  };
}

function buildDivisionCircuits(records) {
  const order = ['Facilities Management', 'Home Services', 'FitOut Solutions', 'Factory — Head Office', 'Division not recorded'];
  return order.map((division) => {
    const rows = records.filter(row => row.division === division);
    if (!rows.length) return null;
    const departments = [...new Set([...(departmentsByDivision[division] || []), ...rows.map(row => row.department)])].sort().map(department => {
      const subset = rows.filter(row => row.department === department);
      return { department, ...summariseRecords(subset) };
    });
    return { id: division.toLowerCase().replace(/[^a-z0-9]+/g, '-'), kind: 'division', division,
      type: 'PR · CPR', ...summariseRecords(rows), departments };
  }).filter(Boolean);
}

function formattedValue(row, field) {
  return row[`${field}${formatted}`] || '';
}

const dataset = await json(proxyUrl, { headers: { Accept: 'application/json' } });
const now = new Date();
const openPr = dataset.pr.rows.filter(row => ['in review', 'approved'].includes(String(row.Status || '').trim().toLowerCase()));
const cpr = openPr.filter(row => norm(row['Purchase requisition']).startsWith('CPR'));
const quoteNumbers = [...new Set(cpr.map(row => norm(row['Quotation reference'])).filter(Boolean))];
const cprNumbers = [...new Set(cpr.map(row => norm(row['Purchase requisition'])).filter(Boolean))];
const quoteSelect = [
  'quoteid', 'quotenumber', 'ssg_prnumber', 'ssg_textdepartment', '_ssg_communityproject_value',
  '_ssg_division_value', '_customerid_value', 'ssg_scopeofwork', 'totalamount', 'ssg_totalcost',
  'ssg_totalcost_date', 'createdon', 'modifiedon', 'statecode', 'statuscode'
].join(',');
const quoteRows = await pool(chunks(cprNumbers, 40), async group => {
  const filter = group.map(value => `ssg_prnumber eq '${value.replaceAll("'", "''")}'`).join(' or ');
  const url = new URL(`${api}/quotes`);
  url.searchParams.set('$select', quoteSelect);
  url.searchParams.set('$filter', filter);
  return paged(url.toString());
});

const quotesByNumber = new Map();
const quotesByPr = new Map();
for (const quote of quoteRows) {
  const qn = norm(quote.quotenumber);
  const pr = norm(quote.ssg_prnumber);
  if (qn) (quotesByNumber.get(qn) || quotesByNumber.set(qn, []).get(qn)).push(quote);
  if (pr) (quotesByPr.get(pr) || quotesByPr.set(pr, []).get(pr)).push(quote);
}

function quoteFor(row) {
  const number = norm(row['Purchase requisition']);
  const reference = norm(row['Quotation reference']);
  const exact = (quotesByNumber.get(reference) || []).filter(quote => norm(quote.ssg_prnumber) === number);
  const candidates = exact.length ? exact : (quotesByPr.get(number) || []);
  return candidates.slice().sort((a, b) => new Date(b.modifiedon) - new Date(a.modifiedon))[0] || null;
}

const prRecords = openPr.map(row => {
  const quote = quoteFor(row);
  const department = clean((quote && quote.ssg_textdepartment) || row.Department);
  const location = clean((quote && formattedValue(quote, '_ssg_communityproject_value')) || row.Location);
  const division = divisionOf(department, quote && formattedValue(quote, '_ssg_division_value'));
  const stepDate = validDate(row['Step date and time']);
  const created = validDate(row['Created date']);
  const gate = gateOf(row['Step name']);
  const scope = quote && clean(quote.ssg_scopeofwork);
  return {
    id: norm(row['Purchase requisition']), kind: norm(row['Purchase requisition']).startsWith('CPR') ? 'CPR' : 'PR',
    division, department, location,
    what: clean(row.Name || (scope !== 'not recorded' ? scope : '')),
    gate, holder: clean(row['Pending Approver/User']),
    waitedDays: calendarDays(stepDate || created, now), waitedWd: workingDays(stepDate || created, now),
    value: Number(row['Total amount']) || 0,
    nextAction: nextAction(gate), quote: quote ? norm(quote.quotenumber) : 'not recorded',
    priceBackAt: quote ? (quote.ssg_totalcost_date || quote.modifiedon || null) : null,
    clock: stepDate ? (String(row['Clock provenance'] || '').includes('SEED') ? 'seeded' : 'captured') : 'not recorded'
  };
});

const storeSelect = [
  'mserp_purchaseordernumber', 'mserp_defaultreceivingwarehouseid', 'mserp_purchaseorderstatus',
  'mserp_documentapprovalstatus', 'mserp_purchaseordername', 'mserp_dataareaid', 'mserp_accountingdate'
].join(',');
const storeUrl = new URL(`${api}/mserp_purchpurchaseorderheaderv2entities`);
storeUrl.searchParams.set('$select', storeSelect);
storeUrl.searchParams.set('$filter', "mserp_defaultreceivingwarehouseid eq 'W001'");
const [storeHeaders, headerCountPage] = await Promise.all([
  paged(storeUrl.toString()),
  json(`${api}/mserp_purchpurchaseorderheaderv2entities?$select=mserp_purchaseordernumber&$count=true&$top=1`, { headers: authHeaders })
]);
const poByKey = new Map(dataset.po.rows.map(row => [key(row['Legal entity'], row['Purchase order']), row]));
const storeRecords = storeHeaders.map(header => {
  const number = norm(header.mserp_purchaseordernumber);
  const raw = poByKey.get(key(header.mserp_dataareaid, number)) || {};
  const status = formattedValue(header, 'mserp_purchaseorderstatus') || 'not recorded';
  const approval = formattedValue(header, 'mserp_documentapprovalstatus') || 'not recorded';
  const gate = status === 'Invoiced' ? 'Invoice received'
    : status === 'Received' ? 'Receipt posted'
    : status === 'Canceled' ? 'Cancelled'
    : approval === 'Confirmed' ? 'Open order' : `${approval} order`;
  const created = validDate(raw['Created date and time']) || validDate(header.mserp_accountingdate);
  const stageDate = validDate(raw['Stage event date and time']) || validDate(raw['Step date and time']);
  const supplierSide = ['Receipt posted', 'Invoice received'].includes(gate);
  return {
    id: number, kind: 'STORE', division: 'Store orders',
    department: clean(raw.Department), location: clean(raw.Location),
    what: clean(header.mserp_purchaseordername || raw['Vendor name']), gate,
    holder: clean(supplierSide ? raw['Vendor name'] : raw['Pending Approver/User']),
    waitedDays: calendarDays(stageDate || created, now), waitedWd: workingDays(stageDate || created, now),
    value: Number(raw['Total amount']) || 0,
    nextAction: gate === 'Invoice received' ? 'Complete: invoice is recorded.'
      : gate === 'Receipt posted' ? 'Finance: record the supplier invoice.'
      : gate === 'Cancelled' ? 'No action: order is cancelled.'
      : 'Procurement: progress the order to receipt.',
    quote: 'not applicable', priceBackAt: null, clock: stageDate ? clean(raw['Clock label']) : 'not recorded'
  };
});
const storeStatus = { open: 0, received: 0, invoiced: 0, cancelled: 0 };
for (const record of storeRecords) {
  if (record.gate === 'Invoice received') storeStatus.invoiced++;
  else if (record.gate === 'Receipt posted') storeStatus.received++;
  else if (record.gate === 'Cancelled') storeStatus.cancelled++;
  else storeStatus.open++;
}
const storeDepartments = [...new Set(storeRecords.map(row => row.department))].sort().map(department => {
  const rows = storeRecords.filter(row => row.department === department);
  const counts = { open: 0, received: 0, invoiced: 0, cancelled: 0 };
  for (const row of rows) {
    if (row.gate === 'Invoice received') counts.invoiced++;
    else if (row.gate === 'Receipt posted') counts.received++;
    else if (row.gate === 'Cancelled') counts.cancelled++;
    else counts.open++;
  }
  return { department, count: rows.length, counts };
});

const poLines = await paged(`${api}/mserp_purchpurchaseorderlinev2entities?$select=mserp_purchaseordernumber,mserp_purchaserequisitionid,mserp_dataareaid&$filter=mserp_purchaserequisitionid%20ne%20null`);
const reqBi = await paged(`${api}/mserp_purchreqlinebientities?$select=mserp_purchid,mserp_purchiddataarea,mserp_purchreqtable_bigint&$filter=mserp_purchid%20ne%20null`);
const reqHeaders = await paged(`${api}/mserp_purchreqtablebientities?$select=mserp_purchreqid,mserp_sourcekey_bigint`);
const reqBySource = new Map(reqHeaders.map(row => [String(row.mserp_sourcekey_bigint), norm(row.mserp_purchreqid)]));
const routeOne = new Map();
const routeTwo = new Map();
function addRoute(map, routeKey, pr) {
  if (!routeKey || !pr) return;
  if (!map.has(routeKey)) map.set(routeKey, new Set());
  map.get(routeKey).add(pr);
}
for (const row of poLines) addRoute(routeOne, key(row.mserp_dataareaid, row.mserp_purchaseordernumber), norm(row.mserp_purchaserequisitionid));
for (const row of reqBi) addRoute(routeTwo, key(row.mserp_purchiddataarea, row.mserp_purchid), reqBySource.get(String(row.mserp_purchreqtable_bigint)));
const openPo = dataset.po.rows.filter(row => Boolean(row['Open pipeline']));
let routeOneCount = 0, routeTwoCount = 0, unionCount = 0, multiCount = 0;
for (const row of openPo) {
  const k = key(row['Legal entity'], row['Purchase order']);
  const oneSet = routeOne.get(k) || new Set();
  const twoSet = routeTwo.get(k) || new Set();
  if (oneSet.size) routeOneCount++;
  if (twoSet.size) routeTwoCount++;
  const union = new Set([...oneSet, ...twoSet]);
  if (union.size) unionCount++;
  if (union.size > 1) multiCount++;
}

const matchedCpr = cpr.filter(row => Boolean(quoteFor(row)));
const resolvedQuoteReferences = cpr.filter(row => {
  const reference = norm(row['Quotation reference']);
  return reference && (quotesByNumber.get(reference) || []).length;
});
const preAprilCpr = cpr.filter(row => validDate(row['Created date']) < new Date('2026-04-01T00:00:00Z'));
const preAprilMatched = preAprilCpr.filter(row => Boolean(quoteFor(row)));
const circuits = buildDivisionCircuits(prRecords);
circuits.push({
  id: 'store-orders', kind: 'store', division: 'Store orders', type: 'W001',
  count: storeRecords.length, liveCount: storeStatus.open + storeStatus.received,
  status: storeStatus, departments: storeDepartments
});

const snapshot = {
  meta: {
    frozenAt: now.toISOString(), proxyGeneratedAt: dataset.generatedAt, proxyRevision: dataset.revision,
    route: 'Existing Microsoft sign-in; silent Dynamics CRM delegated token; read-only Web API.',
    source: 'F&O proxy dataset plus direct read-only Dataverse Web API'
  },
  backfill: {
    legacyExclusion: 831, openCrmBorn: cpr.length, recovered: matchedCpr.length,
    unresolved: cpr.length - matchedCpr.length,
    quoteReferencesResolved: resolvedQuoteReferences.length, quoteReferencesTotal: quoteNumbers.length,
    preAprilOpen: preAprilCpr.length, preAprilRecovered: preAprilMatched.length,
    preAprilUnresolved: preAprilCpr.length - preAprilMatched.length
  },
  store: {
    warehouse: 'W001', total: storeRecords.length, ...storeStatus,
    nonStore: Number(headerCountPage['@odata.count']) - storeRecords.length,
    allOrders: Number(headerCountPage['@odata.count'])
  },
  lineage: {
    audited: { joined: 743, total: 983, multipleOrderNumbers: 11 },
    current: { routeOne: routeOneCount, routeTwo: routeTwoCount, joined: unionCount,
      total: openPo.length, unresolved: openPo.length - unionCount, multipleCompositeOrders: multiCount }
  },
  clocks: { captureSince: '2026-08-07', pollMinutes: 3, missingStart: 67, placeholder1900: 35 },
  circuits,
  records: [...prRecords, ...storeRecords]
};

function embed(source, data) {
  const payload = JSON.stringify(data).replaceAll('</script', '<\\/script');
  const block = `/* JOURNEY_SNAPSHOT_START */window.__JOURNEY_SNAPSHOT__=${payload};/* JOURNEY_SNAPSHOT_END */`;
  if (!/\/\* JOURNEY_SNAPSHOT_START \*\/[\s\S]*?\/\* JOURNEY_SNAPSHOT_END \*\//.test(source)) {
    throw new Error('Journey snapshot markers were not found.');
  }
  return source.replace(/\/\* JOURNEY_SNAPSHOT_START \*\/[\s\S]*?\/\* JOURNEY_SNAPSHOT_END \*\//, block);
}

let board = embed(readFileSync(boardPath, 'utf8'), snapshot);
writeFileSync(boardPath, board, 'utf8');
let preview = board
  .replace('<title>Race Control — PR→PO Journey Board</title>', '<title>Race Control — Journey Board Snapshot</title>')
  .replace('</head><body>', '<script>window.__JOURNEY_PREVIEW__=true;</script></head><body>')
  .replace(/<link href="https:\/\/fonts\.googleapis\.com[^"]+" rel="stylesheet">\r?\n?/, '');
writeFileSync(previewPath, preview, 'utf8');

console.log(JSON.stringify({
  frozenAt: snapshot.meta.frozenAt,
  proxyRevision: snapshot.meta.proxyRevision,
  backfill: snapshot.backfill,
  store: snapshot.store,
  lineage: snapshot.lineage,
  records: snapshot.records.length,
  circuits: snapshot.circuits.map(row => `${row.division}:${row.count}`)
}, null, 2));
