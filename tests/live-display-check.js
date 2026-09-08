'use strict';

const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const vm = require('node:vm');

const DATASET_URL = 'https://ssg-prpo-proxy-h4cvfegaduftedhz.uaenorth-01.azurewebsites.net/api/dataset';

function dashboardCore(html) {
  const start = html.indexOf('const PR_DATA = []');
  const end = html.indexOf('let _t=null;');
  if (start < 0 || end < start) throw new Error('Dashboard core markers were not found');
  return html.slice(start, end);
}

function evaluate(html, dataset) {
  const context = vm.createContext({ console, window: {}, setTimeout, clearTimeout, addEventListener: function () {} });
  vm.runInContext(dashboardCore(html), context, { filename: 'index-dashboard-core.js' });
  context.__dataset = dataset;
  return vm.runInContext(`(() => {
    PR_DATA.push(...__dataset.pr.rows);
    PO_DATA.push(...__dataset.po.rows);
    const prs=buildPRRecords(PR_DATA), pos=buildPORecords(PO_DATA);
    const prLive=prs.filter(r=>r._isOpenPipeline&&!r._isUnmapped&&!['Rejected','Cancelled'].includes(r.status));
    const poLive=pos.filter(r=>!r._isUnmapped&&!r._isPORejected&&!r._isPOCanceled&&!r._isInvoiced);
    const stages=rows=>rows.reduce((out,row)=>{const key=row.hdrBucket||row.bucket||'unmapped';out[key]=(out[key]||0)+1;return out;},{});
    const amount=rows=>Math.round(rows.reduce((sum,row)=>sum+(row.amount||0),0)*100)/100;
    const owners=prLive.concat(poLive).map(r=>String(r.pendingUser||'').trim());
    const noQuotation=prLive.filter(r=>['Procurement','Sourcing','Priced — awaiting approval'].includes(r.hdrBucket)&&!String(r.quotationRef||'').trim()&&(r.aging||0)>7);
    const stepNotReported=prLive.filter(r=>r._isStepUnreported);
    return {
      stable:{prRows:prs.length,poRows:pos.length,prLive:prLive.length,poLive:poLive.length,prAmount:amount(prs),poAmount:amount(pos),prLiveAmount:amount(prLive),poLiveAmount:amount(poLive),prStages:stages(prLive),poStages:stages(poLive)},
      owners:{blank:owners.filter(v=>!v).length,zero:owners.filter(v=>v==='000000').length,numeric:owners.filter(v=>/^\\d+$/.test(v)).length,notRecorded:owners.filter(v=>v==='not recorded').length},
      noQuotation:{count:noQuotation.length,amount:amount(noQuotation)},
      stepNotReported:{count:stepNotReported.length,amount:amount(stepNotReported)},
      revision:__dataset.revision,
      generatedAt:__dataset.generatedAt
    };
  })()`, context);
}

(async function main() {
  let dataset;
  if (process.env.PRPO_DATASET_JSON) dataset = JSON.parse(fs.readFileSync(process.env.PRPO_DATASET_JSON, 'utf8'));
  else {
    const response = await fetch(DATASET_URL, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Live dataset returned ${response.status}`);
    dataset = await response.json();
  }
  const current = evaluate(fs.readFileSync('index.html', 'utf8'), dataset);
  const baselineHtml = execFileSync('git', ['show', `${process.env.BASELINE_REF || 'HEAD'}:index.html`], { encoding: 'utf8', maxBuffer: 4 * 1024 * 1024 });
  const baseline = evaluate(baselineHtml, dataset);
  assert.equal(current.stable.prRows, baseline.stable.prRows);
  assert.equal(current.stable.poRows, baseline.stable.poRows);
  assert.equal(current.stable.prAmount, baseline.stable.prAmount);
  assert.equal(current.stable.poAmount, baseline.stable.poAmount);
  assert.equal(current.stable.poLive, baseline.stable.poLive);
  assert.equal(current.stable.poLiveAmount, baseline.stable.poLiveAmount);
  assert.equal(current.stable.prLive - baseline.stable.prLive, current.stepNotReported.count);
  assert.equal(Math.round((current.stable.prLiveAmount - baseline.stable.prLiveAmount) * 100) / 100, current.stepNotReported.amount);
  assert.equal(current.owners.blank, 0);
  assert.equal(current.owners.zero, 0);
  assert.equal(current.owners.numeric, 0);
  console.log(JSON.stringify({ baseline: baseline.stable, current }, null, 2));
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
