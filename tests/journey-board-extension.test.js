const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const board = fs.readFileSync(path.join(root, 'journey-board.html'), 'utf8');
const preview = fs.readFileSync(path.join(root, 'journey-preview.html'), 'utf8');
const builder = fs.readFileSync(path.join(root, 'scripts', 'build_journey_preview.mjs'), 'utf8');

function snapshotOf(source) {
  const match = source.match(/\/\* JOURNEY_SNAPSHOT_START \*\/window\.__JOURNEY_SNAPSHOT__=(.*?);\/\* JOURNEY_SNAPSHOT_END \*\//s);
  assert.ok(match, 'embedded journey snapshot exists');
  return JSON.parse(match[1]);
}

test('offline preview is self-contained, explicitly frozen, and below 16 MB', () => {
  assert.ok(Buffer.byteLength(preview) < 16 * 1024 * 1024);
  assert.doesNotMatch(preview, /<script[^>]+src=/i);
  assert.doesNotMatch(preview, /<link[^>]+href=/i);
  assert.match(preview, /window\.__JOURNEY_PREVIEW__=true/);
  assert.match(preview, /SNAPSHOT — DATA FROZEN AT/);
  assert.match(preview, /NOT LIVE/);
});

test('CRM backfill uses exact requisition identity and removes the legacy exclusion', () => {
  const snapshot = snapshotOf(preview);
  assert.equal(snapshot.backfill.legacyExclusion, 831);
  assert.equal(snapshot.backfill.recovered + snapshot.backfill.unresolved, snapshot.backfill.openCrmBorn);
  assert.equal(snapshot.backfill.preAprilRecovered + snapshot.backfill.preAprilUnresolved, snapshot.backfill.preAprilOpen);
  assert.match(builder, /ssg_prnumber eq/);
  assert.match(board, /matched an exact quote/);
  assert.doesNotMatch(board, /until then they are excluded from this board/i);
});

test('store circuit is W001 and reconciles every lifecycle state', () => {
  const snapshot = snapshotOf(preview);
  assert.equal(snapshot.store.warehouse, 'W001');
  assert.equal(snapshot.store.open + snapshot.store.received + snapshot.store.invoiced + snapshot.store.cancelled, snapshot.store.total);
  const store = snapshot.circuits.find(row => row.kind === 'store');
  assert.ok(store);
  assert.equal(store.count, snapshot.store.total);
  assert.ok(store.departments.length > 0);
});

test('every division opens to departments on one shared scale', () => {
  const snapshot = snapshotOf(preview);
  const divisions = snapshot.circuits.filter(row => row.kind === 'division');
  assert.ok(divisions.length >= 4);
  divisions.forEach(row => {
    assert.equal(row.legs.length, 3);
    assert.ok(row.departments.length > 0);
    row.departments.forEach(department => assert.equal(department.legs.length, 3));
  });
  assert.match(board, /DEPARTMENTS · SAME SHARED SCALE · TAP FOR RECORDS/);
  assert.match(board, /sharedScale/);
});

test('record drill has seven actionable fields and no blank or numeric owner', () => {
  const snapshot = snapshotOf(preview);
  assert.ok(snapshot.records.length > 0);
  snapshot.records.forEach(row => {
    ['id', 'what', 'gate', 'holder', 'nextAction'].forEach(field => assert.ok(String(row[field] || '').trim(), `${row.id} ${field}`));
    assert.ok(row.waitedDays == null || Number.isFinite(row.waitedDays));
    assert.ok(Number.isFinite(row.value));
    assert.doesNotMatch(row.holder, /^\d+$/);
  });
  const headers = ['DOCUMENT NUMBER', 'WHAT IT IS', 'GATE', 'HOLDER', 'WAITED', 'VALUE EXCL. VAT', 'NEXT ACTION'];
  headers.forEach(header => assert.match(board, new RegExp(header.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))));
  assert.match(board, /not recorded/);
  assert.doesNotMatch(board, />000000</);
});

test('honesty and customer-clock boundaries are visible, with conversion withheld', () => {
  const snapshot = snapshotOf(preview);
  assert.deepEqual(snapshot.lineage.audited, { joined: 743, total: 983, multipleOrderNumbers: 11 });
  assert.deepEqual(snapshot.clocks, { captureSince: '2026-08-07', pollMinutes: 3, missingStart: 67, placeholder1900: 35 });
  assert.match(board, /F&amp;O has no step, step date or holder/);
  assert.match(board, /If capture stops, middle gates go dark/);
  assert.match(board, /approval — unmapped/);
  assert.match(board, /orders have no start/);
  assert.match(board, /carry 01 Jan 1900/);
  assert.match(board, /LINE LINK · NO CONVERSION/);
  assert.match(board, /PROCUREMENT CLOCK/);
  assert.match(board, /price back to CRM/);
  assert.match(board, /CUSTOMER CLOCK/);
  assert.match(board, /Contracted work has no customer quote/);
});

test('board and record filters are wired', () => {
  assert.match(board, /id="circuitDivision"/);
  assert.match(board, /id="circuitType"/);
  assert.match(board, /id="recordKind"/);
  assert.match(board, /id="recordGate"/);
  assert.match(board, /id="recordSearch"/);
  assert.match(board, /addEventListener\('change',filterCircuits\)/);
  assert.match(board, /addEventListener\('input',renderRecordList\)/);
});
