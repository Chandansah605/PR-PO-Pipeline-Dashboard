'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

test('live approvers override the stale daily-export approver', async () => {
  const elements = {
    cacheTag: { style: {}, innerHTML: '', title: '' },
    lastRefresh: { innerText: '' }
  };
  const responses = {
    '/api/pr': {
      generatedAt: '2026-08-05T10:00:00Z',
      rows: [{
        purchaseRequisition: 'PR-000001',
        status: 'InReview',
        pendingApprovers: ['live.user', 'parallel.user'],
        pendingWorkItems: [{ userId: 'live.user' }],
        totalAmount: 100
      }]
    },
    '/api/po': { generatedAt: '2026-08-05T10:00:00Z', rows: [] },
    'pr_steps.json': {
      'PR-000001': { pendingUser: 'stale.export.user', step: 'Finance', stepDate: '2026-08-05T09:00:00Z' }
    }
  };
  let rebuilds = 0;
  const snapshots = new Map();
  const sandbox = {
    PR_DATA: [],
    PO_DATA: [],
    window: { __dashInited: true },
    document: { getElementById: id => elements[id] || null },
    fetch: async url => {
      const key = Object.keys(responses).find(candidate => url.includes(candidate));
      return { ok: true, status: 200, statusText: 'OK', json: async () => responses[key] };
    },
    rebuild: () => { rebuilds += 1; },
    showLoader: () => {},
    hideLoader: () => {},
    idbPut: async (key, value) => { snapshots.set(key, value); },
    setInterval: () => 1,
    setTimeout,
    clearInterval: () => {},
    clearTimeout,
    AbortController,
    console
  };
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync('live-data.js', 'utf8'), sandbox);
  await sandbox.window.loadLive({ silent: true });

  assert.equal(sandbox.PR_DATA[0]['Pending Approver/User'], 'live.user, parallel.user');
  assert.deepEqual(Array.from(sandbox.PR_DATA[0]['Pending Approvers']), ['live.user', 'parallel.user']);
  assert.equal(sandbox.PR_DATA[0]['Step name'], 'Finance');
  assert.equal(rebuilds, 1);
  assert.match(elements.cacheTag.innerHTML, /Live F&amp;O/);
  assert.equal(snapshots.get('__meta__').source, 'live');
  assert.equal(snapshots.get('PR')[0]['Pending Approver/User'], 'live.user, parallel.user');
});

test('a failed PO endpoint does not block live PR approvals', async () => {
  const elements = {
    cacheTag: { style: {}, innerHTML: '', title: '' },
    lastRefresh: { innerText: '' }
  };
  const sandbox = {
    PR_DATA: [{ 'Purchase requisition': 'old-pr' }],
    PO_DATA: [{ 'Purchase order': 'last-known-po' }],
    window: { __dashInited: true },
    document: { getElementById: id => elements[id] || null },
    fetch: async url => {
      if (url.includes('/api/pr')) return {
        ok: true,
        status: 200,
        statusText: 'OK',
        json: async () => ({
          generatedAt: '2026-08-05T11:00:00Z',
          rows: [{ purchaseRequisition: 'PR-LIVE', pendingApprovers: ['approver.one'] }]
        })
      };
      if (url.includes('/api/po')) return { ok: false, status: 504, statusText: 'Gateway Timeout' };
      return { ok: true, status: 200, statusText: 'OK', json: async () => ({}) };
    },
    rebuild: () => {},
    showLoader: () => {},
    hideLoader: () => {},
    setInterval: () => 1,
    setTimeout,
    clearInterval: () => {},
    clearTimeout,
    AbortController,
    console
  };
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync('live-data.js', 'utf8'), sandbox);
  const result = await sandbox.window.loadLive({ silent: true });

  assert.equal(result.partial, true);
  assert.equal(sandbox.PR_DATA[0]['Purchase requisition'], 'PR-LIVE');
  assert.equal(sandbox.PR_DATA[0]['Pending Approver/User'], 'approver.one');
  assert.equal(sandbox.PO_DATA[0]['Purchase order'], 'last-known-po');
  assert.match(elements.cacheTag.title, /PO retained from the last available snapshot/);
});
