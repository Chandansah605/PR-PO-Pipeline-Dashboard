(function () {
  'use strict';

  const esc = value => String(value == null ? '' : value).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
  const one = value => value == null ? '—' : Number(value).toFixed(1);
  const whole = value => value == null ? '—' : Number(value).toLocaleString('en-US');
  const delta = (value, suffix, goodWhenNegative) => {
    const direction = value < 0 ? '▼' : value > 0 ? '▲' : '＝';
    const good = value === 0 ? 'flat' : (value < 0) === goodWhenNegative ? 'good' : 'bad';
    return `<span class="${good}">${direction} ${value === 0 ? '' : Math.abs(value)}${suffix || ''}</span>`;
  };
  const severity = days => days <= 3 ? 'var(--green)' : days <= 10 ? 'var(--amber)' : 'var(--red)';

  const wall = document.querySelector('.wall');
  const stage = document.createElement('div');
  stage.id = 'stage';
  wall.parentNode.insertBefore(stage, wall);
  stage.appendChild(wall);
  const scaleStyle = document.createElement('style');
  scaleStyle.textContent = 'html,body{width:100%;height:100%;overflow:hidden}#stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:top left}';
  document.head.appendChild(scaleStyle);
  function fit() {
    const scale = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `translate(${(innerWidth - 1920 * scale) / 2}px,${(innerHeight - 1080 * scale) / 2}px) scale(${scale})`;
  }
  addEventListener('resize', fit);
  fit();

  const tabs = document.querySelectorAll('.hdr .tab');
  tabs[0].textContent = '1 · JOURNEY BOARD';
  tabs[0].classList.remove('on');
  tabs[1].textContent = '2 · LIVE RACE & QUEUES';
  tabs[1].classList.add('on');
  tabs.forEach(tab => tab.style.cursor = 'pointer');
  tabs[0].addEventListener('click', () => parent.postMessage('journey-page-1', '*'));
  tabs[1].addEventListener('click', () => {});

  const gateNumber = gate => ({'PR Review':2,'RFQ to Suppliers':3,'Quotation Received':4,'Ops Confirmation':5,'Prices Updated':6,'Mgmt Approvals':7}[gate] || 7);

  function renderRail(data) {
    const deepest = data.pitWall.deepestQueue;
    const gates = [
      {kind:'start',name:'PR Raised',type:'START'},
      {n:1,solid:true,name:'Submitted',type:'timestamped'},
      {n:2,name:'PR Review',type:'sequence only'},
      {n:3,name:'RFQ to Suppliers',type:'sequence only'},
      {n:4,name:'Quotation Received',type:'sequence only'},
      {n:5,name:'Ops Confirmation',type:'sequence only'},
      {n:6,name:'Prices Updated',type:'sequence only'},
      {n:7,name:'Mgmt Approvals',type:'sequence only'},
      {n:8,solid:true,name:'PO Created',type:'timestamped'},
      {n:9,solid:true,name:'LPO Sent',type:'timestamped'},
      {kind:'finish',name:'Received / Invoiced',type:'not measurable'},
    ];
    const host = document.getElementById('rail');
    host.innerHTML = '';
    gates.forEach(gate => {
      const critical = gate.name === deepest.gate;
      const node = document.createElement('div');
      node.className = `rk${critical ? ' crit' : ''}`;
      const icon = gate.kind === 'start' ? '<span class="g-start"></span>' : gate.kind === 'finish' ? '<span class="g-fin"></span>' : gate.solid ? `<span class="g-solid">${gate.n}</span>` : `<span class="g-holo">${gate.n}</span>`;
      const type = critical ? `${deepest.count} stuck · ${one(deepest.medianDays)}d` : gate.type;
      node.innerHTML = `<span class="ic">${icon}</span><div class="nm">${esc(gate.name)}</div><div class="tp">${esc(type)}</div>`;
      host.appendChild(node);
    });
  }

  function renderDivisions(divisions) {
    const host = document.getElementById('lrows');
    host.innerHTML = '';
    divisions.forEach(item => {
      const total = Math.max(1, item.buckets.reduce((sum, value) => sum + value, 0));
      const bars = item.buckets.map((value,index) => value ? `<div class="b${index}" style="flex:${value}">${value > total * .07 ? value : ''}</div>` : '').join('');
      const row = document.createElement('div');
      row.className = 'lrow';
      row.innerHTML = `<div class="nm">${esc(item.division)}<span class="sm">${whole(item.count)} PRs on track</span></div><div class="bar">${bars}</div><div class="fig"><b>${one(item.within10Pct)}%</b> within ${delta(item.within10Delta,' pts',false)}<br>median <b>${one(item.medianAgeWd).replace('.0','')} wd</b> ${delta(item.medianAgeDelta,' wd',true)}</div>`;
      host.appendChild(row);
    });
  }

  function rankedRows(host, items, holderMode) {
    host.innerHTML = '';
    const max = Math.max(1, ...items.map(item => item.count));
    items.slice(0,4).forEach(item => {
      const days = holderMode ? item.medianDays : item.medianDays;
      const row = document.createElement('div');
      row.className = 'grow';
      row.innerHTML = `<div class="nm">${holderMode ? '' : `<span class="g">G${gateNumber(item.gate)}</span>`}${esc(holderMode ? item.name : item.gate)}</div><div class="mini"><div style="width:${Math.max(5,item.count/max*100)}%;background:${severity(days)}"></div></div><div class="fig">${item.count} <span>PRs</span> · ${one(days)}d</div>`;
      host.appendChild(row);
    });
  }

  function oldestRows(host, items) {
    host.innerHTML = '';
    items.forEach(item => {
      const row = document.createElement('div');
      row.className = 'carrow';
      row.innerHTML = `<span class="id">${esc(item.number)}</span><span class="wh">held by <b>${esc(item.holder)}</b> · ${esc(item.project)}</span><span class="ag">${item.ageWd} <span>wd on track · ${item.dwellDays == null ? '—' : one(item.dwellDays)}d at step</span></span>`;
      host.appendChild(row);
    });
  }

  function renderTypeColumn(column, type, data) {
    const queues = data.pageTwo.queues[type];
    const holders = data.pageTwo.holders[type];
    const oldest = data.pageTwo.oldest[type];
    const summary = data.pageTwo.types.find(item => item.type === type);
    column.querySelector('.shead .t').textContent = type === 'CPR' ? 'NON-CONTRACTED REVENUE' : 'CONTRACTED / BACK OFFICE';
    column.querySelector('.shead .s').textContent = type === 'CPR' ? 'born from a CRM quote' : 'created in F&O';
    const critical = column.querySelector('.crit');
    const deepest = queues[0];
    critical.classList.remove('bad2','ok');
    critical.classList.add(deepest && deepest.medianDays > 10 ? 'bad2' : 'ok');
    critical.querySelector('.cv').textContent = deepest ? `GATE ${gateNumber(deepest.gate)} · ${deepest.gate.toUpperCase()} — ${whole(deepest.count)} PRs · ${one(deepest.medianDays)}d median wait` : 'NO ACTIVE QUEUE';
    const sections = column.querySelectorAll('[id]');
    const gateHost = Array.from(sections).find(node => node.id === (type === 'CPR' ? 'cg' : 'pg'));
    const holderHost = Array.from(sections).find(node => node.id === (type === 'CPR' ? 'cw' : 'pw'));
    const carHost = Array.from(sections).find(node => node.id === (type === 'CPR' ? 'cc' : 'pc'));
    rankedRows(gateHost, queues, false);
    rankedRows(holderHost, holders, true);
    oldestRows(carHost, oldest);
    const chips = column.querySelector('.schips');
    chips.innerHTML = `<span class="schip">median end-to-end <b>${one(summary.completedMedianWd)}d</b></span><span class="schip">wait for PO <b>${one(summary.toPoMedianWd)}d</b></span><span class="schip">after PO <b>${one(summary.afterPoMedianWd)}d</b> · p90 <b>${one(summary.afterPoP90Wd)}d</b></span>`;
    const insight = column.querySelector('.insight');
    if (type === 'CPR') {
      const top = holders.slice(0,2).reduce((sum,item) => sum + item.count, 0);
      insight.innerHTML = `The revenue lane is concentrated at <b>procurement desks</b>. The top two named holders have <b>${whole(top)} of ${whole(summary.count)}</b> live CPRs.`;
    } else {
      insight.innerHTML = `<b>${deepest ? deepest.gate : 'No gate'} is the largest contracted/back-office queue</b> — ${deepest ? `${whole(deepest.count)} PRs at ${one(deepest.medianDays)}d median dwell` : 'no active items'}.`;
    }
  }

  function applyData(data) {
    document.querySelector('.hdr h1').innerHTML = '<span class="bars"></span>RACE CONTROL — PR → PO JOURNEY BOARD';
    const benches = document.querySelectorAll('.bench');
    benches[0].textContent = `TARGET · PR → GOODS RECEIVED · ${data.targets.raisedToGoodsWd} WD`;
    benches[1].textContent = `WINDOW · ${new Date(data.meta.windowStart + 'T00:00:00').toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}).toUpperCase()} →`;
    const deepest = data.pitWall.deepestQueue;
    document.querySelector('.alert').innerHTML = `<i></i>CRITICAL · GATE ${gateNumber(deepest.gate)} ${esc(deepest.gate.toUpperCase())} · ${whole(deepest.count)} STUCK · ${one(deepest.medianDays)}D`;
    renderRail(data);

    const live = data.live;
    const kpis = document.querySelectorAll('.kpis');
    const first = kpis[0].querySelectorAll('.kpi');
    first[0].querySelector('.v').textContent = whole(live.count);
    first[0].querySelector('.d').innerHTML = delta(live.countDelta,' vs yesterday',true);
    first[1].querySelector('.v').textContent = `${one(live.within10Pct)}%`;
    first[1].querySelector('.d').innerHTML = delta(live.within10Delta,' pts',false);
    first[2].querySelector('.v').innerHTML = `${one(live.medianAgeWd).replace('.0','')} <span>wd</span>`;
    first[2].querySelector('.d').innerHTML = delta(live.medianAgeDelta,' wd',true);
    const second = kpis[1].querySelectorAll('.kpi');
    second[0].querySelector('.v').textContent = whole(data.pageTwo.finishedYesterday);
    second[1].querySelector('.v').textContent = whole(data.pageTwo.raisedYesterday);

    const typeRows = document.querySelectorAll('.tsplit .trow');
    data.pageTwo.types.forEach((item,index) => {
      typeRows[index].querySelector('.tf').innerHTML = `<b>${whole(item.count)}</b> on track · <b>${one(item.within10Pct)}%</b> within · med <b>${one(item.medianAgeWd).replace('.0','')} wd</b>`;
    });
    typeRows[0].querySelector('.tl').textContent = 'NON-CONTRACTED REVENUE · BORN FROM CRM QUOTE';
    typeRows[1].querySelector('.tl').textContent = 'CONTRACTED / BACK OFFICE · CREATED IN F&O';
    renderDivisions(data.pageTwo.divisions);

    const fmPr = data.lanes.find(item => item.label === 'FM · PR');
    const fmCpr = data.lanes.find(item => item.label === 'FM · CPR');
    document.querySelector('.wallnote').innerHTML = `🏁 <b>THE PO IS THE WALL</b> — Facilities Management runs the same race twice: <b>PR waits ${one(fmPr.sectors.submittedToPo)}wd from Submitted→PO, CPR waits ${one(fmCpr.sectors.submittedToPo)}wd</b>. Same operating division, different requisition origins.`;
    const columns = document.querySelectorAll('.scol');
    renderTypeColumn(columns[0], 'CPR', data);
    renderTypeColumn(columns[1], 'PR', data);

    const ticker = document.querySelector('.ticker');
    ticker.innerHTML = `<span style="color:#8ef0ae;font-weight:700"><i style="display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--green);box-shadow:0 0 9px var(--green);margin-right:8px;animation:pu 1.6s infinite"></i>LIVE</span>${data.pageTwo.divisions.map(item => `<span>${esc(item.division.toUpperCase())} <b>${whole(item.count)}</b></span>`).join('<span class="sep">|</span>')}<span class="sep">|</span><span style="color:#ffe1ae">PAGE 1 ← JOURNEY BOARD · PAGE 2 LIVE RACE & QUEUES</span>`;
    const stamp = new Date(data.meta.asOfTimestamp);
    document.querySelector('.foot span:first-child').innerHTML = '<b style="color:#cfe2f5">Solid gates 1·8·9</b> = timestamped · <b style="color:#cfe2f5">dashed 2–7</b> = sequence only · dwell = calendar days at current step · benchmark measured to LPO Sent · working days Mon–Fri · window: created 01 Apr 2026 →';
    document.querySelector('.foot span:last-child').textContent = `Strive Services Group · as of ${stamp.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})} ${stamp.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',hour12:false})}`;
    document.body.classList.add('data-ready');
  }

  fetch(`journey_board.json?t=${Date.now()}`)
    .then(response => {
      if (!response.ok) throw new Error(`Journey data HTTP ${response.status}`);
      return response.json();
    })
    .then(applyData)
    .catch(error => {
      const note = document.createElement('div');
      note.style.cssText = 'position:fixed;left:20px;bottom:20px;z-index:100;background:#7f1d1d;color:white;padding:10px 14px;border-radius:8px;font:600 12px sans-serif';
      note.textContent = `Journey data unavailable: ${error.message}`;
      document.body.appendChild(note);
      document.body.classList.add('data-ready');
    });
})();
