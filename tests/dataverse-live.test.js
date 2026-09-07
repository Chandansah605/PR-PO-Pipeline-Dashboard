'use strict';

const assert = require('node:assert/strict');
const live = require('../dataverse-live.js');

assert.deepEqual(
  live.parseLedgerDimension('-Contracted--Building Services--THE8-Materials-Threshold-'),
  { contract: 'Contracted', department: 'Building Services', location: 'THE8' }
);
assert.equal(
  live.workingDaysOld(new Date('2026-09-04T12:00:00Z'), new Date('2026-09-08T12:00:00Z')),
  2
);
assert.match(live.DATASET_URL, /^https:\/\/ssg-prpo-proxy-.*\/api\/dataset$/);

(async function () {
  const dataset = {
    revision: 'same-revision', generatedAt: '2026-09-07T16:00:00Z', sourceState: 'LIVE',
    pr: { count: 1, rows: [{ 'Purchase requisition': 'PR-TEST', 'Step date and time': '2026-09-07T15:00:00Z' }] },
    po: { count: 1, openCount: 1, clockCounts: { liveDated: 1, seededFromFinalWorkbook: 0, notRecorded: 0 }, rows: [{ 'Purchase order': 'PO-TEST', 'Live stage': 'Receipt posted', 'Stage event date and time': '2026-09-07T16:00:00Z' }] }
  };
  let requested = null;
  const result = await live.load({
    force: true,
    fetchImpl: async url => { requested = url; return new Response(JSON.stringify(dataset), { status: 200, headers: { 'Content-Type': 'application/json' } }); }
  });
  assert.equal(requested, live.DATASET_URL + '?refresh=1');
  assert.equal(result.revision, 'same-revision');
  assert.equal(result.pr[0]['Purchase requisition'], 'PR-TEST');
  assert.equal(result.po[0]['Live stage'], 'Receipt posted');
  assert.equal(live.newestDataDate(result.pr, result.po).toISOString(), '2026-09-07T16:00:00.000Z');
  console.log('Live proxy dataset tests passed');
})().catch(error => { console.error(error); process.exitCode = 1; });
