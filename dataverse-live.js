(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.PRPO_DATAVERSE = api;
})(typeof window !== 'undefined' ? window : null, function () {
  'use strict';

  const ORIGIN = 'https://operations-ifahr-live.crm15.dynamics.com';
  const SCOPE = ORIGIN + '/user_impersonation';
  const FORMATTED = '@OData.Community.Display.V1.FormattedValue';
  const DEFAULT_TIMEOUT_MS = 120000;

  const PATHS = {
    prHeaders: 'mserp_purchaserequisitionheaderv2entities?$select=' + [
      'mserp_requisitionnumber', 'mserp_requisitionname', 'mserp_requisitionstatus',
      'mserp_requisitionpurpose', 'mserp_preparerpersonnelnumber', 'mserp_defaultprojectid',
      'mserp_defaultaccountingdate', 'mserp_defaultrequesteddate', 'mserp_ifahrquotationreference',
      'mserp_projectbuyinglegalentityid'
    ].join(','),
    prLines: 'mserp_purchaserequisitionlinev2entities?$select=' + [
      'mserp_requisitionnumber', 'mserp_lineamount', 'mserp_defaultledgerdimensiondisplayvalue',
      'mserp_deliveryaddressname', 'mserp_projectid', 'mserp_buyinglegalentityid'
    ].join(','),
    prApprovals: 'mserp_purchreqapprovalheaderentities?$select=' + [
      'mserp_requisitionnumber', 'mserp_approvaluser', 'mserp_workflowelementid',
      'mserp_workitemrecid_bigint', 'mserp_workitemrecid'
    ].join(','),
    poHeaders: 'mserp_purchpurchaseorderheaderv2entities?$select=' + [
      'mserp_purchaseordernumber', 'mserp_ordervendoraccountnumber',
      'mserp_invoicevendoraccountnumber', 'mserp_purchaseorderstatus',
      'mserp_documentapprovalstatus', 'mserp_dataareaid', 'mserp_currencycode',
      'mserp_accountingdate', 'mserp_requesteddeliverydate', 'mserp_deliveryaddressname',
      'mserp_projectid', 'mserp_defaultledgerdimensiondisplayvalue',
      'mserp_ordererpersonnelnumber', 'mserp_purchaseordername'
    ].join(','),
    poLines: 'mserp_purchpurchaseorderlinev2entities?$select=' + [
      'mserp_purchaseordernumber', 'mserp_lineamount', 'mserp_defaultledgerdimensiondisplayvalue',
      'mserp_deliveryaddressname', 'mserp_projectid', 'mserp_purchaserequisitionid', 'mserp_dataareaid'
    ].join(','),
    poApprovals: 'mserp_purchapprovalheaderentities?$select=' + [
      'mserp_purchaseordernumber', 'mserp_approvaluser', 'mserp_workflowelementid',
      'mserp_workitemrecid_bigint', 'mserp_workitemrecid', 'mserp_currencycode',
      'mserp_legalentity', 'mserp_ordervendoraccountnumber', 'mserp_purchaseordername'
    ].join(',')
  };

  function clean(value) {
    if (value === null || value === undefined) return null;
    const text = String(value).trim();
    return text || null;
  }

  function numberOrZero(value) {
    const number = Number(value);
    return Number.isFinite(number) ? number : 0;
  }

  function formatted(row, field) {
    return clean(row && row[field + FORMATTED]) || clean(row && row[field]);
  }

  function parseLedgerDimension(value) {
    // F&O exposes a fixed-position display string. Empty dimension slots are
    // significant, so filtering them would shift account into department.
    const parts = String(value || '').split('-').map(function (part) {
      return part.trim();
    });
    return {
      contract: parts[1] || null,
      department: parts[3] || null,
      location: parts[5] || null
    };
  }

  function compositeKey(documentNumber, company) {
    return String(company || '').trim().toLowerCase() + '|' + String(documentNumber || '').trim();
  }

  function attachUniqueDocumentIndex(grouped) {
    const candidates = new Map();
    grouped.forEach(function (value, key) {
      const documentNumber = key.slice(key.indexOf('|') + 1);
      if (!candidates.has(documentNumber)) candidates.set(documentNumber, []);
      candidates.get(documentNumber).push(value);
    });
    grouped.byDocument = new Map();
    candidates.forEach(function (values, documentNumber) {
      if (values.length === 1) grouped.byDocument.set(documentNumber, values[0]);
    });
    return grouped;
  }

  function aggregateLines(rows, documentField, companyField) {
    const grouped = new Map();
    (rows || []).forEach(function (row) {
      const documentNumber = clean(row[documentField]);
      if (!documentNumber) return;
      const key = compositeKey(documentNumber, companyField ? row[companyField] : null);
      let item = grouped.get(key);
      if (!item) {
        item = { total: 0, dimension: null, project: null, deliveryAddress: null, linkedPR: null };
        grouped.set(key, item);
      }
      item.total += numberOrZero(row.mserp_lineamount);
      if (!item.dimension && clean(row.mserp_defaultledgerdimensiondisplayvalue)) {
        item.dimension = clean(row.mserp_defaultledgerdimensiondisplayvalue);
      }
      item.project = item.project || clean(row.mserp_projectid);
      item.deliveryAddress = item.deliveryAddress || clean(row.mserp_deliveryaddressname);
      item.linkedPR = item.linkedPR || clean(row.mserp_purchaserequisitionid);
    });
    grouped.forEach(function (item) {
      item.total = Math.round(item.total * 100) / 100;
      item.parsedDimension = parseLedgerDimension(item.dimension);
    });
    return attachUniqueDocumentIndex(grouped);
  }

  function lookupByDocument(grouped, documentNumber, company) {
    return grouped.get(compositeKey(documentNumber, company)) || (grouped.byDocument && grouped.byDocument.get(documentNumber)) || null;
  }

  function latestApprovals(rows, documentField, companyField) {
    const grouped = new Map();
    (rows || []).forEach(function (row) {
      const documentNumber = clean(row[documentField]);
      if (!documentNumber) return;
      const recId = numberOrZero(row.mserp_workitemrecid_bigint || row.mserp_workitemrecid);
      const key = compositeKey(documentNumber, companyField ? row[companyField] : null);
      const current = grouped.get(key);
      if (!current || recId > current.recId) {
        grouped.set(key, { recId: recId, row: row });
      }
    });
    const result = new Map();
    grouped.forEach(function (value, key) { result.set(key, value.row); });
    return attachUniqueDocumentIndex(result);
  }

  function workflowMatch(lookup, keys) {
    const source = lookup || {};
    for (const key of keys) {
      if (key && Object.prototype.hasOwnProperty.call(source, key)) return { found: true, value: source[key] || {} };
    }
    return { found: false, value: {} };
  }

  function guardedStep(fileStep, mappedLiveStep, hasPublishedStep) {
    const published = clean(fileStep);
    const mapped = clean(mappedLiveStep);
    if (hasPublishedStep) return published;
    return mapped;
  }

  function mapPRRows(headers, lines, approvals, options) {
    options = options || {};
    const lineMap = aggregateLines(lines, 'mserp_requisitionnumber', 'mserp_buyinglegalentityid');
    const approvalMap = latestApprovals(approvals, 'mserp_requisitionnumber');
    const stepMap = options.stepMap || {};
    const workflowLookup = options.workflowLookup || {};

    return (headers || []).map(function (header) {
      const number = clean(header.mserp_requisitionnumber) || '';
      const legalEntity = clean(header.mserp_projectbuyinglegalentityid);
      const line = lookupByDocument(lineMap, number, legalEntity) || { total: 0, parsedDimension: {} };
      const dimension = line.parsedDimension || {};
      const approval = lookupByDocument(approvalMap, number, null) || {};
      const workflowResult = workflowMatch(workflowLookup, [number]);
      const workflow = workflowResult.value;
      const hasPublishedWorkflow = workflowResult.found;
      const elementId = String(approval.mserp_workflowelementid || '').toLowerCase();
      const mappedLiveStep = stepMap[elementId] || null;

      return {
        'Purchase requisition': number,
        'Quotation reference': clean(header.mserp_ifahrquotationreference),
        'Name': clean(header.mserp_requisitionname),
        'Preparer': clean(header.mserp_preparerpersonnelnumber),
        'Project ID': clean(header.mserp_defaultprojectid),
        'Status': formatted(header, 'mserp_requisitionstatus'),
        'Created date': clean(header.mserp_defaultaccountingdate) || clean(header.mserp_defaultrequesteddate),
        'Submitted date': null,
        'Requisition purpose': formatted(header, 'mserp_requisitionpurpose'),
        'Submission Status': clean(workflow.submissionStatus),
        'Accepted By/Assign To': clean(workflow.acceptedBy),
        'Department': clean(dimension.department),
        'Location': clean(dimension.location) || clean(line.project),
        'Contract': clean(dimension.contract),
        'Request for quotation case': clean(workflow.rfqCase),
        'Total amount': line.total || 0,
        'Pending Approver/User': hasPublishedWorkflow ? clean(workflow.pendingUser) : clean(approval.mserp_approvaluser),
        'Step name': guardedStep(workflow.step, mappedLiveStep, hasPublishedWorkflow),
        'Step date and time': clean(workflow.stepDate),
        '_liveWorkflowElementId': elementId || null,
        '_liveWorkflowStep': clean(mappedLiveStep),
        '_liveLegalEntity': legalEntity,
        '_workflowGuarded': !!(hasPublishedWorkflow && clean(mappedLiveStep) !== clean(workflow.step))
      };
    });
  }

  function derivedPOStep(approvalStatus, poStatus) {
    if (approvalStatus === 'Confirmed' && poStatus === 'Received') return 'LPO sent/shared with supplier';
    if (approvalStatus === 'Confirmed' && poStatus === 'Open order') return 'LPO sent/shared with supplier';
    return null;
  }

  function mapPORows(headers, lines, approvals, options) {
    options = options || {};
    const lineMap = aggregateLines(lines, 'mserp_purchaseordernumber', 'mserp_dataareaid');
    const approvalMap = latestApprovals(approvals, 'mserp_purchaseordernumber', 'mserp_legalentity');
    const stepMap = options.stepMap || {};
    const workflowLookup = options.workflowLookup || {};

    return (headers || []).map(function (header) {
      const number = clean(header.mserp_purchaseordernumber) || '';
      const legalEntity = clean(header.mserp_dataareaid);
      const line = lookupByDocument(lineMap, number, legalEntity) || { total: 0, parsedDimension: {} };
      const lineDimension = line.parsedDimension || {};
      const headerDimension = parseLedgerDimension(header.mserp_defaultledgerdimensiondisplayvalue);
      const dimension = {
        contract: lineDimension.contract || headerDimension.contract,
        department: lineDimension.department || headerDimension.department,
        location: lineDimension.location || headerDimension.location
      };
      const approval = lookupByDocument(approvalMap, number, legalEntity) || {};
      const vendorAccount = clean(header.mserp_ordervendoraccountnumber);
      const vendorName = clean(header.mserp_purchaseordername);
      const workflowKeys = [];
      if (vendorAccount) workflowKeys.push(number + '|' + vendorAccount.toLowerCase());
      if (vendorName) workflowKeys.push(number + '|' + vendorName.toLowerCase());
      if (!workflowKeys.length) workflowKeys.push(number);
      const workflowResult = workflowMatch(workflowLookup, workflowKeys);
      const workflow = workflowResult.value;
      const hasPublishedWorkflow = workflowResult.found;
      const elementId = String(approval.mserp_workflowelementid || '').toLowerCase();
      const mappedLiveStep = stepMap[elementId] || null;
      const approvalStatus = formatted(header, 'mserp_documentapprovalstatus');
      const poStatus = formatted(header, 'mserp_purchaseorderstatus');
      const fallbackStep = mappedLiveStep || derivedPOStep(approvalStatus, poStatus);

      return {
        'Purchase order': number,
        'Vendor account': vendorAccount,
        'Invoice account': clean(header.mserp_invoicevendoraccountnumber),
        'Vendor name': vendorName || vendorAccount,
        'Purchase type': 'Purchase order',
        'Approval status': approvalStatus,
        'Purchase order status': poStatus,
        'Currency': clean(header.mserp_currencycode) || clean(approval.mserp_currencycode),
        'Requested receipt date': clean(header.mserp_requesteddeliverydate),
        'Mode of delivery': null,
        'Delivery terms': null,
        'Purchase agreement': null,
        'Direct delivery': null,
        'Project subcontract number': null,
        'Created date and time': clean(header.mserp_accountingdate) || clean(header.mserp_requesteddeliverydate),
        'Purchase requisition': clean(line.linkedPR),
        'RFQ number': null,
        'Total amount': line.total || 0,
        'Department': clean(dimension.department),
        'Location': clean(dimension.location) || clean(line.project) || clean(header.mserp_projectid),
        'Contract': clean(dimension.contract),
        'Pending Approver/User': hasPublishedWorkflow ? clean(workflow.pendingUser) : clean(approval.mserp_approvaluser),
        'Step name': guardedStep(workflow.step, fallbackStep, hasPublishedWorkflow),
        'Step date and time': clean(workflow.stepDate),
        '_liveWorkflowElementId': elementId || null,
        '_liveWorkflowStep': clean(mappedLiveStep),
        '_liveLegalEntity': legalEntity,
        '_workflowGuarded': !!(hasPublishedWorkflow && clean(fallbackStep) !== clean(workflow.step))
      };
    });
  }

  async function odataAll(fetchImpl, token, path, signal) {
    let url = ORIGIN + '/api/data/v9.2/' + path;
    const rows = [];
    let pages = 0;
    while (url && pages++ < 100) {
      const response = await fetchImpl(url, {
        method: 'GET',
        headers: {
          Authorization: 'Bearer ' + token,
          Accept: 'application/json',
          Prefer: 'odata.maxpagesize=5000,odata.include-annotations="OData.Community.Display.V1.FormattedValue"'
        },
        signal: signal
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error('Dataverse ' + response.status + ' for ' + path.split('?')[0] + ': ' + body.slice(0, 180));
      }
      const payload = await response.json();
      rows.push.apply(rows, payload.value || []);
      url = payload['@odata.nextLink'] || null;
    }
    if (url) throw new Error('Dataverse paging limit exceeded for ' + path.split('?')[0]);
    return rows;
  }

  async function load(options) {
    options = options || {};
    if (!options.accessToken) throw new Error('Dataverse access token is missing');
    const fetchImpl = options.fetchImpl || (typeof fetch !== 'undefined' ? fetch.bind(null) : null);
    if (!fetchImpl) throw new Error('Fetch is unavailable');
    const controller = new AbortController();
    const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
    const timer = setTimeout(function () { controller.abort(); }, timeoutMs);
    try {
      const values = await Promise.all([
        odataAll(fetchImpl, options.accessToken, PATHS.prHeaders, controller.signal),
        odataAll(fetchImpl, options.accessToken, PATHS.prLines, controller.signal),
        odataAll(fetchImpl, options.accessToken, PATHS.prApprovals, controller.signal),
        odataAll(fetchImpl, options.accessToken, PATHS.poHeaders, controller.signal),
        odataAll(fetchImpl, options.accessToken, PATHS.poLines, controller.signal),
        odataAll(fetchImpl, options.accessToken, PATHS.poApprovals, controller.signal)
      ]);
      const pr = mapPRRows(values[0], values[1], values[2], {
        stepMap: options.prStepMap,
        workflowLookup: options.prWorkflowLookup
      });
      const po = mapPORows(values[3], values[4], values[5], {
        stepMap: options.poStepMap,
        workflowLookup: options.poWorkflowLookup
      });
      return {
        pr: pr,
        po: po,
        fetchedAt: new Date().toISOString(),
        counts: {
          prHeaders: values[0].length,
          prLines: values[1].length,
          prApprovals: values[2].length,
          poHeaders: values[3].length,
          poLines: values[4].length,
          poApprovals: values[5].length
        }
      };
    } catch (error) {
      if (error && error.name === 'AbortError') throw new Error('Dataverse read timed out after ' + Math.round(timeoutMs / 1000) + ' seconds');
      throw error;
    } finally {
      clearTimeout(timer);
    }
  }

  function newestDataDate(prRows, poRows) {
    let newest = null;
    function consider(value) {
      if (!value) return;
      const date = value instanceof Date ? value : new Date(value);
      if (!Number.isNaN(date.getTime()) && (!newest || date > newest)) newest = date;
    }
    (prRows || []).forEach(function (row) {
      consider(row['Step date and time']);
      consider(row['Created date']);
    });
    (poRows || []).forEach(function (row) {
      consider(row['Step date and time']);
      consider(row['Created date and time']);
    });
    return newest;
  }

  function workingDaysOld(value, now) {
    const startValue = value instanceof Date ? value : new Date(value);
    const endValue = now instanceof Date ? now : new Date(now || Date.now());
    if (Number.isNaN(startValue.getTime()) || Number.isNaN(endValue.getTime())) return null;
    const cursor = new Date(startValue.getFullYear(), startValue.getMonth(), startValue.getDate());
    const end = new Date(endValue.getFullYear(), endValue.getMonth(), endValue.getDate());
    let count = 0;
    while (cursor < end) {
      cursor.setDate(cursor.getDate() + 1);
      const day = cursor.getDay();
      if (day !== 0 && day !== 6) count++;
    }
    return count;
  }

  return {
    ORIGIN: ORIGIN,
    SCOPE: SCOPE,
    PATHS: PATHS,
    parseLedgerDimension: parseLedgerDimension,
    aggregateLines: aggregateLines,
    latestApprovals: latestApprovals,
    mapPRRows: mapPRRows,
    mapPORows: mapPORows,
    newestDataDate: newestDataDate,
    workingDaysOld: workingDaysOld,
    load: load
  };
});
