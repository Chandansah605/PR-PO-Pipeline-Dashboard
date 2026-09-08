'use strict';

const assert = require('node:assert/strict');
const race = require('../race-control.js');

function row(documentNumber, owner, age, stage, amount, raw) {
  return {
    docNumber: documentNumber,
    pendingUser: owner,
    aging: age,
    hdrBucket: stage,
    bucket: stage,
    amount: amount,
    raw: raw || {}
  };
}

const pr = [
  row('PR-KEEP-1', 'Dinesh Laxman Laxman', 4, 'Operations to Confirm', 100, { _hasLiveLine: true }),
  row('PR-KEEP-2', 'dinesh.laxman', 10, 'Dep Managers', 200, { _hasLiveLine: true }),
  row('PR-STUCK', 'dinesh.laxman', 40, 'Dep Managers', 500, { _hasLiveLine: false }),
  row('PR-AUTO', 'Gokul.Krishna', 20, 'Dep Managers', 300, { _hasLiveLine: false }),
  row('PR-CEO', 'Patrick.Smith', 2, 'CEO', 900, { _hasLiveLine: true })
];
const po = [
  row('PO-REVIEW', 'Aparna.Pauly', 3, 'Procurement', 0, { 'Approval status': 'In review', 'Total amount': '1,250.50' }),
  row('PO-SENT', 'Vendor', 12, 'Sent to supplier', 80, { 'Approval status': 'Confirmed' }),
  row('PO-SETTLED', 'Layusha.cleatus', 8, 'Procurement', 70, { 'Approval status': 'Confirmed' })
];
const stuckConfig = [{ documentNumber: 'PR-STUCK', reason: 'Known issue', reportedBy: 'IT', reportedDate: '2026-08-13' }];

const model = race.buildModel({
  prLive: pr,
  poLive: po,
  stuckItems: stuckConfig,
  source: 'Test source',
  currentDate: '2026-09-07',
  weeklySnapshots: {
    weeks: {
      '2026-08-30': { raceControl: { overall: { items: 9, medianDays: 6 }, holders: [], stages: [] } },
      '2026-09-06': { PR: [], PO: [] }
    }
  }
});

assert.equal(model.stuck.length, 2);
assert.deepEqual(model.stuck.map(item => item.documentNumber).sort(), ['PR-AUTO', 'PR-STUCK']);
assert.equal(model.excludedCount, 2);
assert.equal(model.automaticLineCheck, true);
assert.equal(model.overall.items, 6);
assert.equal(model.overall.value, 2600.5);
assert.equal(model.overall.averageDays, 6.5);
assert.equal(model.overall.medianDays, 6);

const dinesh = model.holders.find(holder => holder.key === 'dinesh.laxman');
assert.ok(dinesh);
assert.equal(dinesh.items, 2);
assert.equal(dinesh.value, 300);
assert.equal(dinesh.oldestDays, 10);
assert.equal(dinesh.medianDays, 7);
assert.equal(dinesh.over7, 1);
assert.equal(model.holders.some(holder => holder.key === 'patrick.smith'), false);
assert.equal(model.holders.some(holder => holder.key === 'layusha.cleatus'), false);
assert.equal(model.history[0].key, '2026-08-30');
assert.equal(model.history[0].data.overall.items, 9);
assert.equal(model.history[1].key, '2026-09-06');
assert.equal(model.history[1].data, null);

assert.equal(race.canonicalOwner('Gokul Krishna Pillai'), 'Gokul.Krishna');
assert.equal(race.canonicalOwner(''), 'not recorded');
assert.equal(race.canonicalOwner('000000'), 'not recorded');
assert.equal(race.canonicalOwner('310032'), 'not recorded');
assert.equal(race.personOwner(row('PO-DRAFT', '', 1, 'Procurement', 0, { 'Approval status': 'Draft', 'Created by': 'guessed.owner' }), 'PO'), 'not recorded');
assert.deepEqual(race.holderNames(row('PR-SHARED', 'Adnan.Ullah, adnan.ullah, Layusha.cleatus', 1, 'Procurement', 10)), ['Adnan.Ullah', 'Layusha.cleatus']);
assert.equal(race.median([7, 1, 3, 9]), 5);
assert.deepEqual(race.metric([row('PR-NO-DATE', 'Owner', null, 'Procurement', 10)]), {
  items: 1, value: 10, averageDays: null, medianDays: null, oldestDays: null, over7: 0
});

(async function testLineTracker() {
  const response = new Response(JSON.stringify({ value: [
    { mserp_requisitionnumber: 'PR-ONE' },
    { mserp_requisitionnumber: 'PR-TWO' }
  ] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  const tracker = race.createLineTracker(async () => response);
  const returned = await tracker.fetch('https://example/api/data/v9.2/mserp_purchaserequisitionlinev2entities?$select=mserp_requisitionnumber', {});
  assert.equal(returned, response);
  assert.equal(tracker.hasDocument('pr-one'), true);
  assert.equal(tracker.hasDocument('PR-MISSING'), false);
  assert.equal(tracker.size(), 2);
  console.log('Race Control tests passed');
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
