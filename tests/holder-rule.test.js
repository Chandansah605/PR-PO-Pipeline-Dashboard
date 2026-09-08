'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const race = require('../race-control.js');

const html = fs.readFileSync('index.html', 'utf8');
const divisions = fs.readFileSync('divisions.html', 'utf8');
const rule = JSON.parse(fs.readFileSync('holder-rule.json', 'utf8'));
const literal = html.match(/const HOLDER_RULE = (\{.*\});/);
assert.ok(literal, 'dashboard HOLDER_RULE literal not found');
assert.deepEqual(JSON.parse(literal[1]), rule, 'dashboard and workbook holder rules drifted');
const divisionLiteral = divisions.match(/const HOLDER_RULE = (\{.*\});/);
assert.ok(divisionLiteral, 'division dashboard HOLDER_RULE literal not found');
assert.deepEqual(JSON.parse(divisionLiteral[1]), rule, 'division dashboard and workbook holder rules drifted');
assert.deepEqual(race.OWNER_ALIASES, rule.ownerAliases, 'Race Control owner aliases drifted');
const divisionScript = divisions.match(/<script>\s*([\s\S]*?)<\/script>\s*<\/body>/);
assert.ok(divisionScript, 'division dashboard script not found');
new Function(divisionScript[1]);

const start = html.indexOf('const PR_DATA = []');
const end = html.indexOf('let _t=null;');
assert.ok(start >= 0 && end > start, 'dashboard core markers not found');
const context = vm.createContext({ console, window: {}, setTimeout, clearTimeout, addEventListener() {} });
vm.runInContext(html.slice(start, end), context, { filename: 'index-dashboard-core.js' });

function build(overrides) {
  const row = {
    'Purchase requisition': 'PR-NEW-LIVE',
    'Status': 'In review',
    'Step name': 'Sourcing',
    'Pending Approver/User': 'Adnan.Ullah',
    'Department': 'Building Services',
    'Created date': '2026-09-08T12:00:00Z',
    'Total amount': 100,
    ...overrides
  };
  context.__row = row;
  return vm.runInContext('buildPRRecords([__row])[0]', context);
}

assert.deepEqual(Array.from(build({ 'Pending Approver/User': 'Adnan.Ullah, adnan.ullah, Layusha.cleatus' }).holders), ['Adnan.Ullah', 'Layusha.cleatus']);
assert.deepEqual(Array.from(build({ 'Pending Approver/User': 'Aparna.Pauly' }).holders), ['Aparna.Pauly']);
assert.deepEqual(Array.from(build({ 'Pending Approver/User': '' }).holders), ['not recorded']);

const unreported = build({ 'Step name': '', 'Pending Approver/User': 'roderick.red' });
assert.equal(unreported.hdrBucket, 'Step not reported by F&O');
assert.equal(unreported.subBucket, 'Step not reported by F&O');
assert.equal(unreported._isOpenPipeline, true);
assert.equal(unreported._isUnmapped, false);

const priced = build({ 'Step name': 'Priced — awaiting approval', 'Pending Approver/User': 'Adnan.Ullah' });
assert.equal(priced.hdrBucket, 'Operations to Confirm');
assert.deepEqual(Array.from(priced.holders), ['dinesh.laxman']);
assert.deepEqual(Array.from(build({ 'Step name': 'Priced — awaiting approval', 'Department': 'Surveying Services', 'Pending Approver/User': 'Aparna.Pauly' }).holders), ['Aparna.Pauly']);

console.log('Holder rule tests passed');
