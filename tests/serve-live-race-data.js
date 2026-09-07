'use strict';

const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const live = require('../dataverse-live.js');
const race = require('../race-control.js');
const prStepMap = require('../stepMap.json');
const poStepMap = require('../poStepMap.json');
const prWorkflow = require('../pr_steps.json');

function embeddedRows(name) {
  const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const match = html.match(new RegExp('const ' + name + ' = (\\[[\\s\\S]*?\\]);\\r?\\n'));
  if (!match) throw new Error(name + ' was not found in index.html');
  return JSON.parse(match[1]);
}

function workbookRows(fileName) {
  const script = [
    'import datetime,json,openpyxl,sys',
    'ws=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=True).active',
    'rows=ws.iter_rows(values_only=True)',
    'headers=[str(x) if x is not None else "" for x in next(rows)]',
    'def enc(x):',
    '  return x.isoformat() if isinstance(x,(datetime.date,datetime.datetime)) else x',
    'print(json.dumps([{headers[i]:enc(v) for i,v in enumerate(row) if headers[i]} for row in rows]))'
  ].join('\n');
  return JSON.parse(execFileSync('python', ['-c', script, path.join(__dirname, '..', fileName)], {
    encoding: 'utf8', maxBuffer: 64 * 1024 * 1024
  }));
}

function poWorkflowLookup(rows) {
  const result = {};
  for (const row of rows) {
    const number = String(row['Purchase order'] || '').trim();
    if (!number) continue;
    const value = {
      step: row['Step name'] || null,
      stepDate: row['Step date and time'] || null,
      pendingUser: row['Pending Approver/User'] || null
    };
    const vendorAccount = String(row['Vendor account'] || '').trim().toLowerCase();
    const vendorName = String(row['Vendor name'] || '').trim().toLowerCase();
    if (vendorAccount) result[number + '|' + vendorAccount] = value;
    if (vendorName) result[number + '|' + vendorName] = value;
    if (!vendorAccount && !vendorName) result[number] = value;
  }
  return result;
}

(async function main() {
  const token = process.env.PRPO_DATAVERSE_TEST_TOKEN;
  if (!token) throw new Error('PRPO_DATAVERSE_TEST_TOKEN is required');
  const filePO = workbookRows('po.xlsx');
  const tracker = race.createLineTracker(fetch);
  const result = await live.load({
    accessToken: token,
    timeoutMs: 120000,
    fetchImpl: tracker.fetch,
    prStepMap,
    poStepMap,
    prWorkflowLookup: prWorkflow,
    poWorkflowLookup: poWorkflowLookup(filePO.length ? filePO : embeddedRows('PO_DATA'))
  });
  result.pr.forEach(row => { row._hasLiveLine = tracker.hasDocument(row['Purchase requisition']); });
  const payload = JSON.stringify({ pr: result.pr, po: result.po, counts: result.counts });
  const port = Number(process.argv[2] || 8766);
  http.createServer((request, response) => {
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Cache-Control', 'no-store');
    response.setHeader('Content-Type', 'application/json');
    response.end(payload);
  }).listen(port, '127.0.0.1', () => {
    console.log(`Read-only live Race Control payload ready on 127.0.0.1:${port}`);
  });
})().catch(error => {
  console.error(error.message || error);
  process.exitCode = 1;
});
