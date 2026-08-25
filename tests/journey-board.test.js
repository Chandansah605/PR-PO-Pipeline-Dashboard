const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const board = JSON.parse(fs.readFileSync(path.join(root, 'journey_board.json'), 'utf8'));

assert.equal(board.meta.windowStart, '2026-04-01');
assert.equal(board.headline.completed, 698);
assert.equal(board.headline.submittedMedianWd, 0);
assert.equal(board.headline.poCreatedMedianWd, 9);
assert.equal(board.headline.lpoMedianWd, 12);
assert.equal(board.headline.p90Wd, 34);
assert.equal(board.headline.within10Pct, 43.8);
assert.equal(board.lanes.length, 5, 'Only the five approved ranked circuits belong on Page 1');
assert(!board.lanes.some(lane => lane.label === 'FACTORY · CPR'), 'Factory · CPR must not be rendered');

const lane = label => board.lanes.find(item => item.label === label);
assert.deepEqual(
  [lane('HS · CPR').medianWd, lane('HS · CPR').n, lane('HS · CPR').within10Pct],
  [6, 105, 78.1]
);
assert.deepEqual([lane('FACTORY · PR').medianWd, lane('FACTORY · PR').n], [7, 44]);
assert.deepEqual([lane('FM · PR').medianWd, lane('FM · PR').n], [13, 294]);
assert.deepEqual([lane('FITOUT · CPR').medianWd, lane('FITOUT · CPR').n], [16.5, 20]);
assert.deepEqual(
  [lane('FM · CPR').medianWd, lane('FM · CPR').n, lane('FM · CPR').sectors.submittedToPo],
  [17, 221, 15]
);
assert.deepEqual(board.trend.slice(0, 8).map(item => item.medianWd), [14, 17, 15, 24, 16.5, 9, 9, 7]);
assert.equal(board.trend.at(-1).partial, true);
assert.deepEqual([board.queues[0].gate, board.queues[0].count, board.queues[0].medianDays], ['Prices Updated', 335, 33.6]);

const python = String.raw`
import json
from datetime import datetime
from pathlib import Path
import gen_journey_board as j

assert j.working_days('2026-08-21', '2026-08-24') == 1
assert j.working_days('2026-08-24', '2026-08-31') == 5
assert j.working_days('2026-08-24', '2026-08-24') == 0
assert j.working_days('2026-08-24', '2026-08-21') == -1
assert j.working_days('2026-05-30', '2026-05-29') == 0
assert j.requisition_type('CPR-000001') == 'CPR'
assert j.requisition_type('PR-000001') == 'PR'
assert j.requisition_type('CRP-000001') == 'OTHER'
assert j.division_for('Building Services') == 'Facilities Management'
assert j.division_for('Laundry') == 'Home Services'
assert j.division_for('FitOut Services') == 'FitOut Solutions'
assert j.division_for('Surveying Services') == 'FitOut Solutions'
assert j.division_for('') == 'Factory — Head Office'
assert j.division_for('Marketing') == 'Factory — Head Office'
assert j.is_terminal_po({'Purchase order status':'RECEIVED','Step name':''})
assert j.is_terminal_po({'Purchase order status':'Open order','Step name':'LPO sent/shared with supplier'})
assert not j.is_terminal_po({'Purchase order status':'Open order','Step name':'Procurement Manager'})

prs = [
 {'Purchase requisition':'CPR-OK','Quotation reference':'Q-1','Status':'In review','Created date':'2026-04-01','Submitted date':'2026-04-02','Department':'FitOut Services','Location':'P1','Pending Approver/User':'Buyer','Step name':'Unit prices updated in PR lines','Step date and time':'2026-04-03'},
 {'Purchase requisition':'PR-PRE','Status':'In review','Created date':'2026-03-31','Submitted date':'2026-04-01'},
 {'Purchase requisition':'PR-CANCEL','Status':'Cancelled','Created date':'2026-04-01','Submitted date':'2026-04-01'},
]
pos = [
 {'Purchase order':'PO-1','Purchase requisition':'CPR-OK','Purchase order status':'Open order','Created date and time':'2026-04-03','Step name':'LPO sent/shared with supplier','Step date and time':'2026-04-06'},
 {'Purchase order':'PO-1','Purchase requisition':'CPR-OK','Purchase order status':'Invoiced','Created date and time':'2026-04-03','Step name':'','Step date and time':'2026-04-08'},
 {'Purchase order':'PO-2','Purchase requisition':'CPR-OK','Purchase order status':'Invoiced','Created date and time':'2026-04-06','Step name':'','Step date and time':'2026-04-07'},
]
synthetic = j.build_board(prs, pos, datetime(2026,4,8))
assert synthetic['meta']['eligiblePrs'] == 1
assert synthetic['headline']['completed'] == 2, 'Each exact PR-PO pair is one journey'
assert synthetic['headline']['lpoMedianWd'] == 3.5
assert synthetic['lanes'][0]['division'] == 'FitOut Solutions'

completed = [
 {'terminalAt':datetime(2026,7,1), 'e2eWd':10},
 {'terminalAt':datetime(2026,7,2), 'e2eWd':20},
 {'terminalAt':datetime(2026,7,8), 'e2eWd':7},
]
weeks, _ = j._trend(completed, datetime(2026,7,15))
values = {item['key']:item['medianWd'] for item in weeks}
assert values['2026-W27'] == 15
assert values['2026-W28'] == 7

pr_rows = j.load_xlsx(Path('pr.xlsx'))
po_rows = j.load_xlsx(Path('po.xlsx'))
actual = j.build_board(pr_rows, po_rows)
eligible_cprs = [row for row in pr_rows if (j.parse_datetime(row.get('Created date')) and j.parse_datetime(row.get('Created date')).date() >= j.WINDOW_START and j.text(row.get('Status')).lower() not in j.EXCLUDED_PR_STATUSES and j.requisition_type(row.get('Purchase requisition')) == 'CPR')]
assert all(j.text(row.get('Quotation reference')) for row in eligible_cprs)
assert actual['headline'] == json.loads(Path('journey_board.json').read_text(encoding='utf-8'))['headline']
html = Path('index.html').read_text(encoding='utf-8')
for name, expected in [('PR_DATA', pr_rows), ('PO_DATA', po_rows)]:
    match = __import__('re').search(r'^const ' + name + r' = (.+);$', html, __import__('re').MULTILINE)
    assert match
    normalised = json.loads(json.dumps(expected, default=j._json_default))
    assert json.loads(match.group(1)) == normalised, name + ' fallback differs from XLSX'
print(json.dumps({'prRows':len(pr_rows),'poRows':len(po_rows),'eligibleCprs':len(eligible_cprs)}))
`;

const result = spawnSync('python', ['-c', python], { cwd: root, encoding: 'utf8' });
assert.equal(result.status, 0, result.stderr || result.stdout);
const verified = JSON.parse(result.stdout.trim().split(/\r?\n/).at(-1));
assert.equal(verified.prRows, board.meta.prRows);
assert.equal(verified.poRows, board.meta.poRows);

const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
function embedded(name) {
  const match = html.match(new RegExp(`^const ${name} = (.+);$`, 'm'));
  assert(match, `Embedded ${name} is missing`);
  return JSON.parse(match[1]);
}
assert.equal(embedded('PR_DATA').length, board.meta.prRows, 'PR fallback is stale');
assert.equal(embedded('PO_DATA').length, board.meta.poRows, 'PO fallback is stale');
assert(html.includes('src="journey-board.html"'), 'Analysis tab does not load the Journey Board');
assert(!html.includes('Procurement Action Centre'), 'Rejected Analysis UI is still bundled');
assert(!html.includes('Slowest laps'), 'Rejected slowest-laps UI is still bundled');
assert(fs.readFileSync(path.join(root, 'journey-board-live.js'), 'utf8').includes('fetch(`journey_board.json'));
assert(fs.readFileSync(path.join(root, 'journey-live-data.js'), 'utf8').includes('fetch(`journey_board.json'));

console.log('Journey Board tests passed', {
  completed: board.headline.completed,
  medianWd: board.headline.lpoMedianWd,
  live: board.live.count,
  deepestQueue: `${board.queues[0].count} @ ${board.queues[0].medianDays}d`,
});
