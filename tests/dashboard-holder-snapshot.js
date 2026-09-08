'use strict';

const fs = require('node:fs');
const vm = require('node:vm');

const dataset = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const html = fs.readFileSync('index.html', 'utf8');
const start = html.indexOf('const PR_DATA = []');
const end = html.indexOf('let _t=null;');
if (start < 0 || end < start) throw new Error('dashboard core markers not found');
const context = vm.createContext({ console, window: {}, setTimeout, clearTimeout, addEventListener() {} });
vm.runInContext(html.slice(start, end), context, { filename: 'index-dashboard-core.js' });
context.__dataset = dataset;
const result = vm.runInContext(`(() => {
  PR_DATA.push(...__dataset.pr.rows); PO_DATA.push(...__dataset.po.rows);
  const rows=buildPRRecords(PR_DATA).filter(r=>r._isOpenPipeline&&!['Rejected','Cancelled'].includes(r.status));
  const buyers=['adnan.ullah','aparna.pauly','layusha.cleatus','roderick.red'];
  const holderCounts=Object.fromEntries(buyers.map(name=>[name,rows.filter(r=>r.holders.some(h=>_rnorm(h)===name)).length]));
  const core=buildJourneyCore(); const gates={};core.prLive.forEach(r=>{const gate=core.gateOf(r);gates[gate]=(gates[gate]||0)+1;});
  return {
    revision:__dataset.revision,
    actionableDocuments:rows.length,
    amountExVat:Math.round(rows.reduce((sum,r)=>sum+r.amount,0)*100)/100,
    holderCounts,
    operationsConfirmation:rows.filter(r=>r.hdrBucket==='Operations to Confirm').length,
    stepNotReported:rows.filter(r=>r._isStepUnreported).length,
    commaJoinedLabels:rows.filter(r=>holderDisplay(r).includes(',')).length,
    gates
  };
})()`, context);
process.stdout.write(JSON.stringify(result));
