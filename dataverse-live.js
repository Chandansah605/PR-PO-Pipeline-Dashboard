(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.PRPO_DATAVERSE = api;
})(typeof window !== 'undefined' ? window : null, function (root) {
  'use strict';

  const ORIGIN = 'https://ssg-prpo-proxy-h4cvfegaduftedhz.uaenorth-01.azurewebsites.net';
  const DATASET_URL = ORIGIN + '/api/dataset';
  const CACHE_KEY = 'ssg-prpo-live-dataset-v1';
  const DEFAULT_TIMEOUT_MS = 120000;

  function parseLedgerDimension(value) {
    const parts = String(value || '').split('-').map(function (part) { return part.trim(); });
    return { contract: parts[1] || null, department: parts[3] || null, location: parts[5] || null };
  }

  function newestDataDate(prRows, poRows) {
    let newest = null;
    function consider(value) {
      if (!value) return;
      const date = value instanceof Date ? value : new Date(value);
      if (!Number.isNaN(date.getTime()) && (!newest || date > newest)) newest = date;
    }
    (prRows || []).forEach(function (row) { consider(row['Step date and time']); consider(row['Created date']); });
    (poRows || []).forEach(function (row) { consider(row['Stage event date and time']); consider(row['Step date and time']); });
    return newest;
  }

  function workingDaysOld(value, now) {
    const start = value instanceof Date ? value : new Date(value);
    const endValue = now instanceof Date ? now : new Date(now || Date.now());
    if (Number.isNaN(start.getTime()) || Number.isNaN(endValue.getTime())) return null;
    const cursor = new Date(start.getFullYear(), start.getMonth(), start.getDate());
    const end = new Date(endValue.getFullYear(), endValue.getMonth(), endValue.getDate());
    let count = 0;
    while (cursor < end) { cursor.setDate(cursor.getDate() + 1); if (![0, 6].includes(cursor.getDay())) count++; }
    return count;
  }

  function readCache() {
    if (!root || !root.localStorage) return null;
    try {
      const value = JSON.parse(root.localStorage.getItem(CACHE_KEY) || 'null');
      return value && value.pr && value.po ? value : null;
    } catch (_) { return null; }
  }

  function saveCache(value) {
    if (!root || !root.localStorage) return;
    try { root.localStorage.setItem(CACHE_KEY, JSON.stringify(value)); } catch (_) { /* storage can be disabled */ }
  }

  async function load(options) {
    options = options || {};
    const fetchImpl = options.fetchImpl || (typeof fetch !== 'undefined' ? fetch.bind(null) : null);
    if (!fetchImpl) throw new Error('Fetch is unavailable');
    const controller = new AbortController();
    const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
    const timer = setTimeout(function () { controller.abort(); }, timeoutMs);
    try {
      const url = DATASET_URL + (options.force ? '?refresh=1' : '');
      const response = await fetchImpl(url, { cache: 'no-store', signal: controller.signal });
      if (!response.ok) throw new Error('Live PR/PO service returned ' + response.status);
      const dataset = await response.json();
      if (!dataset || !dataset.revision || !dataset.pr || !dataset.po || !Array.isArray(dataset.pr.rows) || !Array.isArray(dataset.po.rows)) {
        throw new Error('Live PR/PO service returned an invalid dataset');
      }
      const result = {
        pr: dataset.pr.rows,
        po: dataset.po.rows,
        fetchedAt: dataset.generatedAt,
        revision: dataset.revision,
        sourceState: dataset.sourceState || 'LIVE',
        freshness: dataset.freshness || null,
        counts: { prHeaders: dataset.pr.count, poHeaders: dataset.po.count, poOpen: dataset.po.openCount },
        clockCounts: dataset.po.clockCounts || null
      };
      saveCache({ ...result, savedAt: new Date().toISOString() });
      return result;
    } catch (error) {
      const cached = readCache();
      if (cached) return { ...cached, sourceState: 'STALE', stale: true, refreshError: error.message };
      if (error && error.name === 'AbortError') throw new Error('Live PR/PO read timed out after ' + Math.round(timeoutMs / 1000) + ' seconds');
      throw error;
    } finally {
      clearTimeout(timer);
    }
  }

  return {
    ORIGIN: ORIGIN,
    DATASET_URL: DATASET_URL,
    parseLedgerDimension: parseLedgerDimension,
    newestDataDate: newestDataDate,
    workingDaysOld: workingDaysOld,
    load: load,
    readCache: readCache
  };
});
