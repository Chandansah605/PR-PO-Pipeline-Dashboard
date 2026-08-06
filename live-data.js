(function () {
  'use strict';

  const PROXY_BASE = 'https://pr-po-dashboard-proxy-b4budzexh7eveved.uaenorth-01.azurewebsites.net';
  const REFRESH_MS = 3 * 60 * 1000;
  const REQUEST_TIMEOUT_MS = 30 * 1000;
  let inFlight = null;
  let refreshTimer = null;

  function humanize(value) {
    if (value == null) return null;
    const text = String(value).replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/_/g, ' ').trim();
    return text ? text.charAt(0).toUpperCase() + text.slice(1).toLowerCase() : null;
  }

  function liveApprovers(row) {
    const values = Array.isArray(row.pendingApprovers)
      ? row.pendingApprovers
      : String(row.pendingApprover || '').split(',');
    return [...new Set(values.map(value => String(value || '').trim()).filter(Boolean))];
  }

  function mapPR(row, overlays) {
    const overlay = overlays[row.purchaseRequisition] || {};
    const approvers = liveApprovers(row);
    return {
      'Purchase requisition': row.purchaseRequisition || null,
      'Quotation reference': row.quotationReference || null,
      'Name': row.name || null,
      'Preparer': row.preparer || null,
      'Project ID': row.projectId || null,
      'Status': humanize(row.status),
      'Created date': row.createdDate || null,
      'Submitted date': row.submittedDate || null,
      'Requisition purpose': humanize(row.requisitionPurpose),
      'Submission Status': row.submissionStatus || overlay.submissionStatus || null,
      'Accepted By/Assign To': row.acceptedByAssignTo || overlay.acceptedBy || null,
      'Department': row.department || overlay.department || null,
      'Location': row.location || overlay.location || null,
      'Contract': row.contract || overlay.contract || null,
      'Request for quotation case': row.rfqCase || overlay.rfqCase || null,
      'Total amount': Number(row.totalAmount) || 0,
      // Approver is always live. Never overwrite this with the daily Excel export.
      'Pending Approver/User': approvers.join(', ') || null,
      'Pending Approvers': approvers,
      // Friendly step label/date remain a clearly identified daily-export overlay
      // until F&O exposes the authoritative custom fields.
      'Step name': overlay.step || row.stepName || null,
      'Step date and time': overlay.stepDate || row.stepDateTime || null,
      'Workflow work items': row.pendingWorkItems || [],
      'Workflow due date and time': row.workItemDueDateTime || null
    };
  }

  function mapPO(row) {
    const approvers = liveApprovers(row);
    return {
      'Purchase order': row.purchaseOrder || null,
      'Purchase requisition': row.linkedPR || null,
      'Vendor name': row.vendorName || null,
      'Name': row.name || null,
      'Approval status': humanize(row.approvalStatus),
      'Purchase order status': humanize(row.poStatus),
      'Currency': row.currency || null,
      'Project ID': row.projectId || null,
      'Requested receipt date': row.createdDate || null,
      'Created date and time': row.createdDate || null,
      'Department': row.department || null,
      'Location': row.location || null,
      'Contract': row.contract || null,
      'Total amount': Number(row.totalAmount) || 0,
      'Pending Approver/User': approvers.join(', ') || null,
      'Pending Approvers': approvers,
      'Step name': row.stepName || null,
      'Step date and time': row.stepDateTime || null,
      'Workflow work items': row.pendingWorkItems || [],
      'Workflow due date and time': row.workItemDueDateTime || null
    };
  }

  async function json(url) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    try {
      const response = await fetch(url, {
        cache: 'no-store',
        headers: { Accept: 'application/json' },
        signal: controller.signal
      });
      if (!response.ok) throw new Error(response.status + ' ' + response.statusText + ' at ' + url);
      return response.json();
    } finally {
      clearTimeout(timeout);
    }
  }

  function setSource(kind, detail) {
    const tag = document.getElementById('cacheTag');
    if (!tag) return;
    tag.style.display = 'inline-flex';
    tag.innerHTML = kind === 'live'
      ? '<i class="fa-solid fa-satellite-dish"></i> Live F&amp;O · approvers'
      : '<i class="fa-solid fa-triangle-exclamation"></i> Excel fallback';
    tag.title = detail || '';
  }

  async function runLoad(options) {
    const opts = options || {};
    if (!opts.silent && typeof showLoader === 'function') showLoader('Pulling live PR / PO approvals from F&O...');
    const bust = '?t=' + Date.now();
    const [prResult, poResult, overlayResult] = await Promise.allSettled([
      json(PROXY_BASE + '/api/pr' + bust),
      json(PROXY_BASE + '/api/po' + bust),
      json('pr_steps.json' + bust)
    ]);
    const overlays = overlayResult.status === 'fulfilled' ? overlayResult.value : {};
    const pr = prResult.status === 'fulfilled' && Array.isArray(prResult.value.rows) ? prResult.value : null;
    const po = poResult.status === 'fulfilled' && Array.isArray(poResult.value.rows) ? poResult.value : null;
    if (!pr && !po) throw new Error('Neither PR nor PO live endpoint returned a valid data contract');

    if (pr) PR_DATA.splice(0, PR_DATA.length, ...pr.rows.map(row => mapPR(row, overlays || {})));
    if (po) PO_DATA.splice(0, PO_DATA.length, ...po.rows.map(mapPO));

    const loaded = [pr && 'PR', po && 'PO'].filter(Boolean);
    const failed = [!pr && 'PR', !po && 'PO'].filter(Boolean);
    const generatedAt = [pr && pr.generatedAt, po && po.generatedAt].filter(Boolean).sort().pop() || new Date().toISOString();
    if (typeof idbPut === 'function') {
      const snapshotWrites = [];
      if (pr) snapshotWrites.push(idbPut('PR', PR_DATA));
      if (po) snapshotWrites.push(idbPut('PO', PO_DATA));
      snapshotWrites.push(idbPut('__meta__', {
        savedAt: generatedAt,
        source: 'live',
        prUpdated: Boolean(pr),
        poUpdated: Boolean(po)
      }));
      await Promise.allSettled(snapshotWrites);
    }
    const detail = 'Live WorkflowWorkItems approvers loaded for ' + loaded.join(' + ') + '.'
      + (failed.length ? ' ' + failed.join(' + ') + ' retained from the last available snapshot.' : '')
      + ' Step label/date uses the latest daily export where required.';
    setSource('live', detail);
    const lastRefresh = document.getElementById('lastRefresh');
    if (lastRefresh) lastRefresh.innerText = 'Live F&O: ' + new Date(generatedAt).toLocaleString();
    if (!opts.deferRender && window.__dashInited && typeof rebuild === 'function') rebuild();
    if (!opts.silent && typeof hideLoader === 'function') hideLoader();
    return { pr, po, partial: failed.length > 0 };
  }

  window.loadLive = function loadLive(options) {
    if (inFlight) return inFlight;
    inFlight = runLoad(options).catch(error => {
      console.error('Live F&O load failed:', error);
      setSource('fallback', 'Live proxy failed: ' + error.message);
      if (typeof hideLoader === 'function') hideLoader();
      throw error;
    }).finally(() => { inFlight = null; });
    return inFlight;
  };

  window.startLiveAutoRefresh = function startLiveAutoRefresh() {
    if (refreshTimer) clearInterval(refreshTimer);
    refreshTimer = setInterval(() => window.loadLive({ silent: true }).catch(() => {}), REFRESH_MS);
  };
})();
