const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const helperMatch = html.match(/\/\* JOURNEY_TIME_START[\s\S]*?\*\/([\s\S]*?)\/\* JOURNEY_TIME_END \*\//);
assert(helperMatch, 'Journey calculation helpers were not found in index.html');

const context = { Date, Set, String, Number, Math, isFinite, isNaN };
vm.createContext(context);
vm.runInContext(helperMatch[1], context);

const { _jtParseDate, _jtPercentile, buildJourneyModel } = context;
assert.equal(_jtParseDate('2026-08-25').getFullYear(), 2026);
assert.equal(_jtParseDate('2026-08-25 13:45:30').getHours(), 13);
assert.equal(_jtParseDate('08-25-26').getMonth(), 7);
assert.equal(_jtParseDate('8/25/26 13:45').getHours(), 13);
assert.equal(_jtParseDate('08/25/2026').getDate(), 25);
assert.equal(_jtParseDate('25/08/2026'), null, 'Only the verified month-first workbook format is accepted');
assert.equal(_jtParseDate('not-a-date'), null);
assert.equal(_jtPercentile([1, 2, 3, 4], 0.5), 2.5);
assert.equal(_jtPercentile([1, 2, 3, 4], 0.9), 3.7);

const prs = [
  {'Purchase requisition':'PR-COMPLETE','Status':'Closed','Created date':'2026-08-01','Submitted date':'2026-08-02'},
  {'Purchase requisition':'PR-MISSING','Status':'Draft','Created date':'2026-08-01','Submitted date':null},
  {'Purchase requisition':'PR-NEGATIVE','Status':'In review','Created date':'2026-08-03','Submitted date':'2026-08-02'},
  {'Purchase requisition':'PR-REJECTED','Status':'Rejected','Created date':'2026-08-01','Submitted date':'2026-08-02'}
];
const pos = [
  {'Purchase order':'PO-COMPLETE','Purchase requisition':'PR-COMPLETE','Approval status':'Confirmed','Purchase order status':'Invoiced','Created date and time':'2026-08-04','Step name':'LPO sent/shared with supplier','Step date and time':'2026-08-07'},
  {'Purchase order':'PO-MISSING','Purchase requisition':'PR-MISSING','Approval status':'Confirmed','Purchase order status':'Received','Created date and time':'2026-08-04','Step name':'LPO sent/shared with supplier','Step date and time':null},
  {'Purchase order':'PO-REJECTED','Purchase requisition':'PR-COMPLETE','Approval status':'Rejected','Purchase order status':'Open order','Created date and time':'2026-08-05','Step name':'Procurement Manager','Step date and time':'2026-08-06'}
];
const synthetic = buildJourneyModel(prs, pos);
assert.equal(synthetic.exclusions.pr, 1);
assert.equal(synthetic.exclusions.po, 1);
assert.deepEqual(
  [synthetic.raisedToSubmitted.valid, synthetic.raisedToSubmitted.missing, synthetic.raisedToSubmitted.negative],
  [1, 1, 1]
);
assert.equal(synthetic.submittedToPO.valid, 1);
assert.equal(synthetic.submittedToPO.missing, 1);
assert.equal(synthetic.poToLastStep.valid, 1);
assert.equal(synthetic.poToLastStep.missing, 1);
assert.equal(synthetic.poToLastStep.median, 3);
assert.equal(synthetic.prToPO.median, 3);
assert.equal(synthetic.endToEnd.median, 6);

function embeddedData(name) {
  const match = html.match(new RegExp(`^const ${name} = (.+);$`, 'm'));
  assert(match, `Embedded ${name} was not found`);
  return JSON.parse(match[1]);
}

const actual = buildJourneyModel(embeddedData('PR_DATA'), embeddedData('PO_DATA'));
assert(actual.prRows.length > 3000, 'Expected the committed PR fallback data');
assert(actual.pairs.length > 700, 'Expected more than 700 exact PR-PO links in the embedded fallback');
assert(actual.endToEnd.valid > 300, 'Expected more than 300 measured fallback end-to-end journeys');
assert.equal(actual.raisedToSubmitted.valid + actual.raisedToSubmitted.missing + actual.raisedToSubmitted.negative, actual.raisedToSubmitted.total);
assert.equal(actual.endToEnd.valid + actual.endToEnd.missing + actual.endToEnd.negative, actual.endToEnd.total);

console.log('Journey time tests passed', {
  prEligible: actual.prRows.length,
  linkedPairs: actual.pairs.length,
  terminalPairs: actual.terminal.length,
  endToEndMeasured: actual.endToEnd.valid,
  medianEndToEndDays: Number(actual.endToEnd.median.toFixed(1))
});
