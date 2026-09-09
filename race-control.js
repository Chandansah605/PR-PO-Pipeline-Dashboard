(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.RACE_CONTROL = api;
})(typeof window !== 'undefined' ? window : null, function () {
  'use strict';

  const OWNER_ALIASES = {
    'dinesh laxman laxman': 'dinesh.laxman',
    'gokul krishna pillai': 'Gokul.Krishna',
    'pramod chandrasenan chandrasenan': 'pramod.c',
    'shijil choyaprath chandran': 'shijil.c',
    'zaheer ahmed ameer': 'Zaheer.Ahmed',
    'd365crm admin': 'it.solutions',
    'd365crmadmin': 'it.solutions',
    'it department': 'it.solutions'
  };

  const PR_STAGES = ['Procurement', 'Operations to Confirm', 'Step not reported by F&O', 'Dep Managers', 'Finance', 'Director', 'CEO'];
  const PO_STAGES = ['Procurement', 'Finance', 'Director', 'CEO', 'Not yet sent', 'Sent to supplier', 'Receipt posted'];
  const NOT_RECORDED = 'not recorded';

  function clean(value) {
    return String(value == null ? '' : value).trim();
  }

  function ownerKey(value) {
    return clean(value).toLowerCase().replace(/\s+/g, ' ');
  }

  function canonicalOwner(value) {
    const original = clean(value);
    if (!original || /^0+$/.test(original) || /^\d+$/.test(original)) return NOT_RECORDED;
    return OWNER_ALIASES[ownerKey(original)] || original;
  }

  function holderNames(row) {
    const source = row && Array.isArray(row.holders) ? row.holders : [row && row.pendingUser];
    const seen = new Set(), output = [];
    source.forEach(function (value) {
      String(value == null ? '' : value).split(',').forEach(function (part) {
        const owner = canonicalOwner(part), key = ownerKey(owner);
        if (owner === NOT_RECORDED || seen.has(key)) return;
        seen.add(key); output.push(owner);
      });
    });
    return output.length ? output : [NOT_RECORDED];
  }

  function finiteAges(rows) {
    return (rows || []).filter(function (row) {
      return row && row.aging != null && clean(row.aging) !== '';
    }).map(function (row) { return Number(row.aging); })
      .filter(function (value) { return Number.isFinite(value); });
  }

  function ageOf(row) {
    if (!row || row.aging == null || clean(row.aging) === '') return null;
    const value = Number(row.aging);
    return Number.isFinite(value) ? value : null;
  }

  function median(values) {
    const sorted = (values || []).filter(Number.isFinite).slice().sort(function (a, b) { return a - b; });
    if (!sorted.length) return null;
    const middle = sorted.length >> 1;
    return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
  }

  function average(values) {
    const usable = (values || []).filter(Number.isFinite);
    if (!usable.length) return null;
    return usable.reduce(function (sum, value) { return sum + value; }, 0) / usable.length;
  }

  function rounded(value) {
    return value == null ? null : Math.round(value * 10) / 10;
  }

  function numeric(value) {
    if (typeof value === 'number') return Number.isFinite(value) ? value : 0;
    const parsed = Number(clean(value).replace(/[^0-9.-]/g, ''));
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function amount(row) {
    const rawAmount = row && row.raw && row.raw['Total amount'];
    return clean(rawAmount) ? numeric(rawAmount) : numeric(row && row.amount);
  }

  function hasRecordedAmount(row) {
    const hasRaw = row && row.raw && Object.prototype.hasOwnProperty.call(row.raw, 'Total amount');
    const raw = hasRaw ? row.raw['Total amount'] : row && row.amount;
    return clean(raw) !== '' && numeric(raw) > 0;
  }

  function metric(rows) {
    const ages = finiteAges(rows);
    const priced = (rows || []).filter(hasRecordedAmount);
    return {
      items: (rows || []).length,
      pricedItems: priced.length,
      unpricedItems: (rows || []).length - priced.length,
      value: Math.round(priced.reduce(function (sum, row) { return sum + amount(row); }, 0) * 100) / 100,
      averageDays: rounded(average(ages)),
      medianDays: rounded(median(ages)),
      oldestDays: ages.length ? Math.max.apply(null, ages) : null,
      over7: ages.filter(function (age) { return age > 7; }).length
    };
  }

  function documentNumber(row) {
    return clean(row && row.docNumber).toUpperCase();
  }

  function buildStuck(prLive, configured) {
    const liveByDocument = new Map((prLive || []).map(function (row) { return [documentNumber(row), row]; }));
    const entries = [];
    const configuredByDocument = new Map();
    (configured || []).forEach(function (item) {
      const number = clean(item.documentNumber).toUpperCase();
      if (!number || configuredByDocument.has(number)) return;
      configuredByDocument.set(number, item);
      const row = liveByDocument.get(number) || null;
      entries.push({
        documentNumber: number,
        reason: clean(item.reason) || 'Maintained IT clean-up item.',
        reportedBy: clean(item.reportedBy) || '—',
        reportedDate: clean(item.reportedDate) || null,
        age: ageOf(row),
        holder: row ? holderNames(row).join(' · ') : NOT_RECORDED,
        active: !!row,
        automatic: false
      });
    });
    (prLive || []).forEach(function (row) {
      const number = documentNumber(row);
      if (!number || configuredByDocument.has(number)) return;
      if (!row.raw || row.raw._hasLiveLine !== false) return;
      entries.push({
        documentNumber: number,
        reason: 'No purchase requisition lines returned by live Dataverse.',
        reportedBy: 'Automatic live check',
        reportedDate: null,
        age: ageOf(row),
        holder: holderNames(row).join(' · '),
        active: true,
        automatic: true
      });
    });
    entries.sort(function (a, b) {
      if (a.active !== b.active) return a.active ? -1 : 1;
      return (b.age == null ? -1 : b.age) - (a.age == null ? -1 : a.age);
    });
    return {
      entries: entries,
      excludedDocuments: new Set(entries.filter(function (item) { return item.active; }).map(function (item) { return item.documentNumber; }))
    };
  }

  function stageName(row) {
    return clean(row.hdrBucket || row.bucket) || 'Needs review';
  }

  function personOwner(row, type) {
    if (type === 'PR') return holderNames(row)[0];
    const approval = clean(row.raw && row.raw['Approval status']);
    if (approval === 'In review' || approval === 'InReview' || approval === 'Draft') return holderNames(row)[0];
    return '';
  }

  function personRows(prRows, poRows) {
    const combined = [];
    (prRows || []).forEach(function (row) {
      const stage = stageName(row);
      if (stage === 'Director' || stage === 'CEO') return;
      holderNames(row).forEach(function (owner) {
        if (owner !== NOT_RECORDED) combined.push({ row: row, type: 'PR', owner: owner });
      });
    });
    (poRows || []).forEach(function (row) {
      const stage = stageName(row);
      const approval = clean(row.raw && row.raw['Approval status']);
      if (!['In review', 'InReview', 'Draft'].includes(approval)) return;
      if (['Director', 'CEO', 'Sent to supplier', 'Receipt posted'].includes(stage)) return;
      holderNames(row).forEach(function (owner) {
        if (owner !== NOT_RECORDED) combined.push({ row: row, type: 'PO', owner: owner });
      });
    });
    return combined;
  }

  function aggregateHolders(prRows, poRows) {
    const grouped = new Map();
    personRows(prRows, poRows).forEach(function (item) {
      const key = ownerKey(item.owner);
      let value = grouped.get(key);
      if (!value) {
        value = { key: key, name: item.owner, rows: [], prItems: 0, poItems: 0 };
        grouped.set(key, value);
      }
      value.rows.push(item.row);
      if (item.type === 'PR') value.prItems++;
      else value.poItems++;
    });
    return Array.from(grouped.values()).map(function (holder) {
      return Object.assign({ key: holder.key, name: holder.name, prItems: holder.prItems, poItems: holder.poItems }, metric(holder.rows));
    }).sort(function (a, b) { return b.items - a.items || b.oldestDays - a.oldestDays || a.name.localeCompare(b.name); });
  }

  function aggregateStages(prRows, poRows) {
    const output = [];
    [['PR', PR_STAGES, prRows || []], ['PO', PO_STAGES, poRows || []]].forEach(function (group) {
      const type = group[0], order = group[1], rows = group[2];
      order.forEach(function (name) {
        const matching = rows.filter(function (row) { return stageName(row) === name; });
        if (!matching.length) return;
        output.push(Object.assign({ key: type + '|' + name, type: type, name: name }, metric(matching)));
      });
    });
    return output;
  }

  function historicalWeeks(weekly, currentDate) {
    if (!weekly || !weekly.weeks) return [];
    const limit = clean(currentDate).slice(0, 10);
    return Object.keys(weekly.weeks).filter(function (key) { return !limit || key <= limit; }).sort().slice(-2);
  }

  function historicalRace(weekly, key) {
    return key && weekly && weekly.weeks && weekly.weeks[key] && weekly.weeks[key].raceControl || null;
  }

  function buildModel(options) {
    options = options || {};
    const prLive = options.prLive || [];
    const poLive = options.poLive || [];
    const stuck = buildStuck(prLive, options.stuckItems || []);
    const cleanPR = prLive.filter(function (row) { return !stuck.excludedDocuments.has(documentNumber(row)); });
    const allClean = cleanPR.concat(poLive);
    const holders = aggregateHolders(cleanPR, poLive);
    const stages = aggregateStages(cleanPR, poLive);
    const weekKeys = historicalWeeks(options.weeklySnapshots, options.currentDate);
    return {
      source: clean(options.source) || 'Current dashboard source',
      overall: metric(allClean),
      holders: holders,
      stages: stages,
      stuck: stuck.entries,
      excludedCount: stuck.excludedDocuments.size,
      automaticLineCheck: prLive.some(function (row) { return row.raw && typeof row.raw._hasLiveLine === 'boolean'; }),
      history: [
        { key: weekKeys.length > 1 ? weekKeys[0] : null, data: historicalRace(options.weeklySnapshots, weekKeys.length > 1 ? weekKeys[0] : null) },
        { key: weekKeys.length ? weekKeys[weekKeys.length - 1] : null, data: historicalRace(options.weeklySnapshots, weekKeys.length ? weekKeys[weekKeys.length - 1] : null) }
      ]
    };
  }

  function createLineTracker(baseFetch) {
    const lineDocuments = new Set();
    async function trackedFetch(url, options) {
      const response = await baseFetch(url, options);
      if (response.ok && String(url).includes('/mserp_purchaserequisitionlinev2entities')) {
        const payload = await response.clone().json();
        (payload.value || []).forEach(function (row) {
          const number = clean(row.mserp_requisitionnumber).toUpperCase();
          if (number) lineDocuments.add(number);
        });
      }
      return response;
    }
    return {
      fetch: trackedFetch,
      hasDocument: function (documentNumberValue) { return lineDocuments.has(clean(documentNumberValue).toUpperCase()); },
      size: function () { return lineDocuments.size; }
    };
  }

  function esc(value) {
    return clean(value).replace(/[&<>"']/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character];
    });
  }

  function one(value) {
    return value == null ? '—' : Number(value).toFixed(1);
  }

  function whole(value) {
    return value == null ? '—' : Number(value).toLocaleString('en-US', { maximumFractionDigits: 0 });
  }

  function money(value) {
    return 'AED ' + whole(value);
  }

  function dateLabel(value) {
    if (!value) return 'No prior snapshot';
    const date = new Date(value + 'T00:00:00');
    return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' });
  }

  function delta(current, prior, lowerIsBetter) {
    if (current == null || prior == null) return '<span class="rc-delta muted">—</span>';
    const change = Math.round((current - prior) * 10) / 10;
    if (!change) return '<span class="rc-delta muted">● 0</span>';
    const good = lowerIsBetter ? change < 0 : change > 0;
    return '<span class="rc-delta ' + (good ? 'good' : 'bad') + '">' + (change > 0 ? '▲ +' : '▼ ') + one(Math.abs(change)) + '</span>';
  }

  function historyMetric(history, field, key) {
    if (!history || !history.data) return null;
    if (!key) return history.data.overall || null;
    const rows = history.data[field] || [];
    return rows.find(function (row) { return row.key === key; }) || null;
  }

  function movementCells(current, field, key, history) {
    const two = historyMetric(history[0], field, key);
    const last = historyMetric(history[1], field, key);
    function cell(value, prior) {
      if (!value) return '<td><span class="rc-pair">—</span></td>';
      return '<td><span class="rc-pair"><b>' + whole(value.items) + '</b> items · <b>' + one(value.medianDays) + 'd</b> median</span>' +
        (prior ? delta(value.items, prior.items, false) + delta(value.medianDays, prior.medianDays, true) : '') + '</td>';
    }
    return cell(two, null) + cell(last, two) + cell(current, last);
  }

  function render(container, model) {
    if (!container) return;
    const overall = model.overall;
    const stageRows = model.stages.map(function (stage) {
      return '<tr><td><span class="rc-type ' + stage.type.toLowerCase() + '">' + stage.type + '</span><b>' + esc(stage.name) + '</b></td>' +
        '<td>' + whole(stage.items) + '</td><td>' + one(stage.averageDays) + 'd</td><td><b>' + one(stage.medianDays) + 'd</b></td><td class="rc-over">' + whole(stage.over7) + '</td></tr>';
    }).join('');
    const holderRows = model.holders.map(function (holder) {
      const preferred = holder.poItems > holder.prItems ? 'PO' : 'PR';
      return '<tr class="rc-holder" tabindex="0" data-holder="' + esc(holder.key) + '" data-type="' + preferred + '">' +
        '<td><b>' + esc(holder.name) + '</b><span class="rc-person-sub">PR ' + holder.prItems + ' · PO ' + holder.poItems + '</span></td>' +
        '<td><b>' + whole(holder.items) + '</b></td><td>' + (holder.pricedItems ? whole(holder.pricedItems) + ' priced · ' + money(holder.value) : 'Not yet priced') + '</td><td>' + one(holder.oldestDays) + 'd</td><td>' + one(holder.medianDays) + 'd</td><td class="rc-over">' + holder.over7 + '</td><td><button class="rc-view">View queue <i class="fa-solid fa-arrow-right"></i></button></td></tr>';
    }).join('');
    const history = model.history;
    const movementHolderRows = model.holders.map(function (holder) {
      return '<tr><td><b>' + esc(holder.name) + '</b></td>' + movementCells(holder, 'holders', holder.key, history) + '</tr>';
    }).join('');
    const movementStageRows = model.stages.map(function (stage) {
      return '<tr><td><span class="rc-type ' + stage.type.toLowerCase() + '">' + stage.type + '</span><b>' + esc(stage.name) + '</b></td>' + movementCells(stage, 'stages', stage.key, history) + '</tr>';
    }).join('');
    const stuckRows = model.stuck.map(function (item) {
      return '<article class="rc-stuck-item ' + (item.active ? '' : 'inactive') + '"><div class="rc-stuck-top"><b>' + esc(item.documentNumber) + '</b><span>' + (item.age == null ? 'Not in live queue' : whole(item.age) + 'd') + '</span></div>' +
        '<p>' + esc(item.reason) + '</p><small>' + esc(item.reportedBy) + (item.reportedDate ? ' · ' + esc(item.reportedDate) : '') + (item.automatic ? ' · automatic' : '') + '</small></article>';
    }).join('');
    const stuckAges = model.stuck.map(function (item) { return item.age; }).filter(Number.isFinite);
    const oldestStuck = stuckAges.length ? Math.max.apply(null, stuckAges) : null;
    const excludedText = model.excludedCount + ' stuck item' + (model.excludedCount === 1 ? '' : 's') + ' excluded — see lane';
    container.innerHTML = '<div class="rc-shell">' +
      '<header class="rc-hero"><div><span class="rc-eyebrow"><i class="fa-solid fa-flag-checkered"></i> Race Control</span><h2>Who is holding what — and is it getting better?</h2><p>Live action queue · source-labelled age · ' + esc(model.source) + '. Each document counts once overall; shared holders each receive one personal attribution.</p></div><div class="rc-exclusion"><b>' + model.excludedCount + '</b><span>' + esc(excludedText) + '</span></div></header>' +
      '<section class="rc-block"><div class="rc-block-head"><span>01</span><div><h3>How long are things taking?</h3><p>Live pipeline only. Detail rows say whether age starts at raised date or a distinct step date.</p></div></div>' +
        '<div class="rc-overall"><div><span>Average source age</span><b>' + one(overall.averageDays) + '<small>d</small></b></div><div><span>Median source age</span><b>' + one(overall.medianDays) + '<small>d</small></b></div><div><span>Live action items</span><b>' + whole(overall.items) + '</b></div><div><span>Past seven days</span><b class="danger">' + whole(overall.over7) + '</b></div></div>' +
        '<div class="rc-table-wrap"><table class="rc-table rc-stage-table"><thead><tr><th>Header stage</th><th>Items</th><th>Average</th><th>Median</th><th>&gt;7d</th></tr></thead><tbody>' + stageRows + '</tbody></table></div></section>' +
      '<section class="rc-block"><div class="rc-block-head"><span>02</span><div><h3>Who is holding what?</h3><p>Click a person to ring-fence their existing detail queue. Recorded value names its priced-item count.</p></div></div><div class="rc-table-wrap"><table class="rc-table rc-holder-table"><thead><tr><th>Person</th><th>Items</th><th>Recorded value</th><th>Oldest source age</th><th>Median source age</th><th>&gt;7d</th><th></th></tr></thead><tbody>' + holderRows + '</tbody></table></div></section>' +
      '<section class="rc-block"><div class="rc-block-head"><span>03</span><div><h3>Is it getting better?</h3><p>Two Sunday positions against the live queue. Dashes mean no trustworthy snapshot.</p></div></div>' +
        '<div class="rc-trend-overall"><div class="rc-trend-label">Overall live queue</div><table class="rc-table"><thead><tr><th></th><th>' + dateLabel(history[0].key) + '</th><th>' + dateLabel(history[1].key) + '</th><th>Live now</th></tr></thead><tbody><tr><td><b>All stages</b></td>' + movementCells(overall, null, null, history) + '</tr></tbody></table></div>' +
        '<div class="rc-trend-grid"><div><h4>Holders</h4><div class="rc-table-wrap"><table class="rc-table"><thead><tr><th>Person</th><th>' + dateLabel(history[0].key) + '</th><th>' + dateLabel(history[1].key) + '</th><th>Live now</th></tr></thead><tbody>' + movementHolderRows + '</tbody></table></div></div>' +
        '<div><h4>Header stages</h4><div class="rc-table-wrap"><table class="rc-table"><thead><tr><th>Stage</th><th>' + dateLabel(history[0].key) + '</th><th>' + dateLabel(history[1].key) + '</th><th>Live now</th></tr></thead><tbody>' + movementStageRows + '</tbody></table></div></div></div></section>' +
      '<section class="rc-block rc-stuck"><div class="rc-block-head"><span>04</span><div><h3>What is garbage?</h3><p>Stuck in system — IT clean-up. Labelled and removed from personal and ageing figures.</p></div></div>' +
        '<div class="rc-stuck-summary"><b>' + model.stuck.length + ' listed</b><span>Oldest active clock: ' + (oldestStuck == null ? '—' : one(oldestStuck) + 'd') + '</span><span>' + (model.automaticLineCheck ? 'Automatic no-line check active' : 'Automatic no-line check waits for live data') + '</span></div><div class="rc-stuck-grid">' + stuckRows + '</div></section>' +
      '</div>';
  }

  return {
    OWNER_ALIASES: OWNER_ALIASES,
    NOT_RECORDED: NOT_RECORDED,
    ownerKey: ownerKey,
    canonicalOwner: canonicalOwner,
    holderNames: holderNames,
    median: median,
    average: average,
    metric: metric,
    buildStuck: buildStuck,
    aggregateHolders: aggregateHolders,
    aggregateStages: aggregateStages,
    personOwner: personOwner,
    buildModel: buildModel,
    createLineTracker: createLineTracker,
    render: render
  };
});
