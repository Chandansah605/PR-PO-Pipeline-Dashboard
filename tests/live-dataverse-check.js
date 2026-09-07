'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const live = require('../dataverse-live.js');
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
  const output = execFileSync('python', ['-c', script, path.join(__dirname, '..', fileName)], {
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024
  });
  return JSON.parse(output);
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

(async function () {
  const token = process.env.PRPO_DATAVERSE_TEST_TOKEN;
  if (!token) throw new Error('PRPO_DATAVERSE_TEST_TOKEN is required');
  const filePR = workbookRows('pr.xlsx');
  const filePO = workbookRows('po.xlsx');
  const result = await live.load({
    accessToken: token,
    timeoutMs: 120000,
    prStepMap,
    poStepMap,
    prWorkflowLookup: prWorkflow,
    poWorkflowLookup: poWorkflowLookup(filePO.length ? filePO : embeddedRows('PO_DATA'))
  });
  const newest = live.newestDataDate(result.pr, result.po);
  function reconciliation(fileRows, liveRows, key, keyName) {
    const keyOf = typeof key === 'function' ? key : row => String(row[key] || '').trim();
    const logicalKey = keyName || key;
    const fileById = new Map(fileRows.map(row => [keyOf(row), row]));
    const liveById = new Map(liveRows.map(row => [keyOf(row), row]));
    const common = [...fileById.keys()].filter(id => id && liveById.has(id));
    const compareFields = logicalKey === 'Purchase requisition'
      ? ['Status', 'Step name', 'Step date and time', 'Department', 'Location', 'Contract', 'Total amount']
      : ['Approval status', 'Purchase order status', 'Step name', 'Step date and time', 'Department', 'Location', 'Contract', 'Total amount', 'Purchase requisition'];
    const mismatches = {};
    const filePopulated = {};
    const populatedMismatches = {};
    const samples = {};
    const populatedSamples = {};
    for (const field of compareFields) {
      const different = common.filter(id => {
        const a = fileById.get(id)[field];
        const b = liveById.get(id)[field];
        if (field === 'Total amount') return Math.abs(Number(a || 0) - Number(b || 0)) > 0.01;
        return String(a || '').trim() !== String(b || '').trim();
      });
      mismatches[field] = different.length;
      const populated = common.filter(id => {
        const value = fileById.get(id)[field];
        return value !== null && value !== undefined && String(value).trim() !== '';
      });
      const populatedSet = new Set(populated);
      filePopulated[field] = populated.length;
      populatedMismatches[field] = different.filter(id => populatedSet.has(id)).length;
      samples[field] = different.slice(0, 3).map(id => ({ id, file: fileById.get(id)[field] || null, live: liveById.get(id)[field] || null }));
      populatedSamples[field] = different.filter(id => populatedSet.has(id)).slice(0, 3).map(id => ({
        id,
        file: fileById.get(id)[field] || null,
        live: liveById.get(id)[field] || null
      }));
    }
    const amountMatchesTaxInclusive = common.filter(id => {
      const fileAmount = Number(fileById.get(id)['Total amount'] || 0);
      const liveAmount = Number(liveById.get(id)['Total amount'] || 0);
      return Math.abs(fileAmount - liveAmount) > 0.01 && Math.abs(fileAmount - liveAmount * 1.05) <= 0.02;
    }).length;
    return {
      fileRows: fileRows.length,
      liveRows: liveRows.length,
      commonRows: common.length,
      fileOnly: fileRows.length - common.length,
      liveOnly: liveRows.length - common.length,
      mismatches,
      filePopulated,
      populatedMismatches,
      amountMatchesTaxInclusive,
      samples,
      populatedSamples
    };
  }
  console.log(JSON.stringify({
    counts: result.counts,
    mapped: { pr: result.pr.length, po: result.po.length },
    newestDataDate: newest && newest.toISOString(),
    guardedHistoricalWorkflow: {
      pr: result.pr.filter(row => row._workflowGuarded).length,
      po: result.po.filter(row => row._workflowGuarded).length
    },
    withStepDate: {
      pr: result.pr.filter(row => row['Step date and time']).length,
      po: result.po.filter(row => row['Step date and time']).length
    },
    reconciliation: {
      pr: reconciliation(filePR, result.pr, 'Purchase requisition'),
      po: reconciliation(filePO, result.po, row => {
        const number = String(row['Purchase order'] || '').trim();
        const vendor = String(row['Vendor account'] || row['Vendor name'] || '').trim().toLowerCase();
        return number + '|' + vendor;
      }, 'Purchase order')
    }
  }, null, 2));
})().catch(error => {
  console.error(error.message || error);
  process.exitCode = 1;
});
