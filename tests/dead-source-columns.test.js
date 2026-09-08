'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const displaySources = ['index.html', 'divisions.html', 'race-control.js'];
const deadOwnerOrMetricFields = [
  'Submission Status',
  'Accepted By/Assign To',
  'Request for quotation case',
  'Purchase type',
  'RFQ number',
  'Created by',
  'Created By',
  'Preparer'
];

for (const file of displaySources) {
  const source = fs.readFileSync(path.join(root, file), 'utf8');
  for (const field of deadOwnerOrMetricFields) {
    assert.equal(source.includes(field), false, `${file} still reads or names dead field ${field}`);
  }
}

const index = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const analysis = index.slice(index.indexOf('function renderAnalysis(){'), index.indexOf('function raceLiveRecords('));
assert.ok(analysis.includes('No quotation recorded'));
assert.ok(analysis.includes('Quotation referenced'));
assert.ok(analysis.includes('PR-to-PO conversion is withheld because lineage is incomplete.'));
assert.equal(analysis.includes('No RFQ issued'), false);
assert.equal(analysis.includes('RFQ issued'), false);
assert.equal(analysis.includes('PO created'), false);

console.log('Dead source column display tests passed');
