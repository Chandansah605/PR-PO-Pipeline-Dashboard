'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const race = require('../race-control.js');

const html = fs.readFileSync('index.html', 'utf8');
const divisions = fs.readFileSync('divisions.html', 'utf8');
const rule = JSON.parse(fs.readFileSync('holder-rule.json', 'utf8'));
const workRule = JSON.parse(fs.readFileSync('work-class-rule.json', 'utf8'));
const employeeMap = JSON.parse(fs.readFileSync('employee-holder-map.json', 'utf8'));
const inactive = JSON.parse(fs.readFileSync('inactive-usernames.json', 'utf8')).inactiveUsernames.map(value => value.toLowerCase());
const literal = html.match(/const HOLDER_RULE = (\{.*\});/);
assert.ok(literal, 'dashboard HOLDER_RULE literal not found');
assert.deepEqual(JSON.parse(literal[1]), rule, 'dashboard and workbook holder rules drifted');
const divisionLiteral = divisions.match(/const HOLDER_RULE = (\{.*\});/);
assert.ok(divisionLiteral, 'division dashboard HOLDER_RULE literal not found');
assert.deepEqual(JSON.parse(divisionLiteral[1]), rule, 'division dashboard and workbook holder rules drifted');
const workLiteral = html.match(/const WORK_CLASS_RULE = (\{.*\});/);
const employeeLiteral = html.match(/const EMPLOYEE_HOLDER_MAP = (\{.*\});/);
assert.ok(workLiteral, 'dashboard WORK_CLASS_RULE literal not found');
assert.ok(employeeLiteral, 'dashboard EMPLOYEE_HOLDER_MAP literal not found');
assert.deepEqual(JSON.parse(workLiteral[1]), workRule, 'dashboard and workbook class rules drifted');
assert.deepEqual(JSON.parse(employeeLiteral[1]), employeeMap, 'dashboard and workbook employee maps drifted');
const inactiveLiteral = html.match(/const INACTIVE_USERNAMES = new Set\((\[.*\])\);/);
assert.ok(inactiveLiteral, 'dashboard inactive-user literal not found');
assert.deepEqual(JSON.parse(inactiveLiteral[1]), inactive, 'dashboard inactive-user list drifted');
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
    'Stage reason code': 'ACTIVE_LINES_NOT_FULLY_PRICED',
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
const shared = build({ 'Pending Approver/User': 'Adnan.Ullah, Layusha.cleatus, roderick.red' });
assert.equal(shared.sourceShared, true);
assert.deepEqual(Array.from(shared.liveBuyers), ['Adnan.Ullah', 'roderick.red']);
assert.doesNotMatch(shared.sharedLabel, /Layusha/i);
assert.deepEqual(Array.from(build({ 'Pending Approver/User': 'Aparna.Pauly' }).holders), ['Aparna.Pauly']);
assert.deepEqual(Array.from(build({ 'Pending Approver/User': '' }).holders), ['not recorded']);

const unreported = build({ 'Step name': '', 'Stage reason code': 'UNMAPPED_ELEMENT', 'Pending Approver/User': 'roderick.red' });
assert.equal(unreported.hdrBucket, 'Step not reported by F&O');
assert.equal(unreported.subBucket, 'Step not reported by F&O');
assert.equal(unreported._isOpenPipeline, true);
assert.equal(unreported._isUnmapped, false);

const priced = build({ 'Step name': 'Priced — awaiting approval', 'Stage reason code': 'ACTIVE_LINES_PRICED', 'Pending Approver/User': 'Adnan.Ullah' });
assert.equal(priced.hdrBucket, 'Operations to Confirm');
assert.deepEqual(Array.from(priced.holders), ['dinesh.laxman']);
assert.deepEqual(Array.from(build({ 'Step name': 'Priced — awaiting approval', 'Stage reason code': 'ACTIVE_LINES_PRICED', 'Department': 'Surveying Services', 'Pending Approver/User': 'Aparna.Pauly' }).holders), ['No named owner — no operations person mapped for Surveying Services']);

const mappedEmployee = build({ 'Step name': '', 'Stage reason code': 'NO_CURRENT_WORK_ITEM', 'Preparer': '310523', 'Pending Approver/User': '' });
assert.deepEqual(Array.from(mappedEmployee.holders), ['dinesh.laxman']);
assert.notEqual(mappedEmployee.pendingUser, 'not recorded');
const missingEmployee = build({ 'Step name': '', 'Stage reason code': 'NO_CURRENT_WORK_ITEM', 'Preparer': '999999', 'Pending Approver/User': '' });
assert.deepEqual(Array.from(missingEmployee.holders), ['employee number 999999 — name not resolved']);
const systemEmployee = build({ 'Step name': '', 'Stage reason code': 'NO_CURRENT_WORK_ITEM', 'Preparer': '000000', 'Pending Approver/User': '' });
assert.deepEqual(Array.from(systemEmployee.holders), ['No named owner — D365CRM ADMIN']);

for(const [code, cfg] of Object.entries(workRule.classes)){
  const rec = build({ 'Stage reason code': code, 'Step name': code==='ACTIVE_LINES_PRICED'?'Priced — awaiting approval':'', 'Preparer':'310523' });
  assert.equal(rec.classCode, code);
  assert.equal(rec.workClass, cfg.label);
  assert.equal(rec.workAction, cfg.action);
}
assert.equal(vm.runInContext('ageBand(7)', context), '0–7');
assert.equal(vm.runInContext('ageBand(8)', context), '8–30');
assert.equal(vm.runInContext('ageBand(31)', context), '31–60');
assert.equal(vm.runInContext('ageBand(61)', context), '61–90');
assert.equal(vm.runInContext('ageBand(91)', context), 'Over 90');
const raisedClock = build({ 'Created date': '2026-09-01T00:00:00Z', 'Step date and time': '2026-09-01T00:00:00Z' });
assert.equal(raisedClock.ageBasis, 'Raised');
assert.match(raisedClock.ageLabel, /^Raised \d+d ago$/);
const stepClock = build({ 'Created date': '2026-08-01T00:00:00Z', 'Step date and time': '2026-09-05T00:00:00Z' });
assert.equal(stepClock.ageBasis, 'Current step');
assert.match(stepClock.ageLabel, /^Current step \d+d$/);

console.log('Holder rule tests passed');
