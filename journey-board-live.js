(function () {
  'use strict';

  const esc = value => String(value == null ? '' : value).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
  const one = value => value == null ? '—' : Number(value).toFixed(1);
  const whole = value => value == null ? '—' : Number(value).toLocaleString('en-US');
  const evidenceMode = new URLSearchParams(location.search).has('evidence');
  const trendColour = value => value <= 10 ? ['#8ef0ae','linear-gradient(180deg,#34d873,#1f9b52)'] : value <= 15 ? ['#ffd9a1','linear-gradient(180deg,#f5b942,#c78a1b)'] : ['#ff9d9d','linear-gradient(180deg,#f4726a,#c2413a)'];

  function showPage(page) {
    const live = document.getElementById('livePage');
    live.style.display = page === 2 ? 'block' : 'none';
  }

  document.querySelectorAll('.hdr .tabs .tab').forEach((tab, index) => {
    tab.style.cursor = 'pointer';
    tab.addEventListener('click', () => showPage(index + 1));
  });
  addEventListener('message', event => {
    if (event.data === 'journey-page-1') showPage(1);
  });

  function renderTrend(data) {
    const host = document.getElementById('tw');
    const values = data.trend.filter(item => item.medianWd != null).map(item => item.medianWd);
    const max = Math.max(26, ...values, 1);
    host.innerHTML = `<div class="tgt" style="bottom:${10 / max * 100 * 0.78 + 18}px"><span>TARGET 10</span></div>`;
    data.trend.forEach(item => {
      const value = item.medianWd;
      const [ink, fill] = trendColour(value == null ? 99 : value);
      const bar = document.createElement('div');
      bar.className = `tb2${item.partial ? ' dim' : ''}`;
      bar.innerHTML = `<span class="wv" style="color:${ink}">${value == null ? '—' : one(value).replace('.0','')}</span><div class="bar2" style="height:${value == null ? 6 : Math.max(6, value / max * 100 * .78)}px;background:${fill}"></div><span class="wl">${esc(item.label)}${item.partial ? '·partial' : ''}</span>`;
      host.appendChild(bar);
    });
    const full = data.trend.filter(item => !item.partial && item.medianWd != null);
    let streak = 0;
    for (let index = full.length - 1; index >= 0 && full[index].medianWd <= 10; index--) streak++;
    const delta = data.trendDeltaWd;
    const direction = delta < 0 ? '▼' : delta > 0 ? '▲' : '＝';
    const chip = document.querySelector('.hero .panel .ttl .chip');
    chip.textContent = `${direction} ${Math.abs(delta || 0)} WD vs LAST WEEK · ${streak} STRAIGHT WEEK${streak === 1 ? '' : 'S'} AT / UNDER TARGET`;
  }

  function renderJourney(data) {
    const root = document.getElementById('jl');
    root.innerHTML = '';
    const NS = 'http://www.w3.org/2000/svg';
    const width = 1830, height = 182, y = 88;
    root.setAttribute('viewBox', `0 0 ${width} ${height}`);
    const make = (tag, attrs) => {
      const node = document.createElementNS(NS, tag);
      Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
      root.appendChild(node);
      return node;
    };
    const head = data.headline;
    const sectors = [
      {wd: head.submittedMedianWd, colour: '#22c55e'},
      {wd: head.poCreatedMedianWd - head.submittedMedianWd, colour: '#ef4444', critical: true},
      {wd: head.lpoMedianWd - head.poCreatedMedianWd, colour: '#f59e0b'},
    ];
    const ghost = [150, 130], minimum = 80, multiplier = 95;
    const total = sectors.reduce((sum, sector) => sum + Math.max(minimum, sector.wd * multiplier), 0) + ghost[0] + ghost[1];
    const scale = (width - 130) / total;
    let x = 64;
    const points = [x];
    sectors.forEach(sector => {
      const section = Math.max(minimum, sector.wd * multiplier) * scale;
      make('line', {x1:x,y1:y,x2:x+section,y2:y,stroke:sector.colour,'stroke-width':14,'stroke-linecap':'butt',style:sector.critical?'filter:drop-shadow(0 0 12px rgba(239,68,68,.7))':''});
      const flow = make('line', {x1:x,y1:y,x2:x+section,y2:y,stroke:'rgba(255,255,255,.5)','stroke-width':3,'stroke-dasharray':'9 24'});
      flow.innerHTML = '<animate attributeName="stroke-dashoffset" from="33" to="0" dur="1.1s" repeatCount="indefinite"/>';
      if (sector.critical) {
        const label = make('text', {x:x+section/2,y:y-42,'text-anchor':'middle','class':'seglab'});
        label.textContent = `PRIMARY CONSTRAINT · SUBMITTED → PO · ${one(sector.wd)} WD`;
      }
      x += section;
      points.push(x);
    });
    ghost.forEach(length => {
      make('line', {x1:x,y1:y,x2:x+length*scale,y2:y,stroke:'var(--ghost)','stroke-width':9,'stroke-dasharray':'5 11'});
      x += length * scale;
      points.push(x);
    });
    const nodes = [
      ['PR RAISED','0.0 WD','#22c55e'],
      ['SUBMITTED',`${one(head.submittedMedianWd)} WD`,'#22c55e'],
      ['PO CREATED',`${one(head.poCreatedMedianWd)} WD`,'#ef4444'],
      ['LPO SENT',`${one(head.lpoMedianWd)} WD`,'#f59e0b'],
      ['GOODS RECEIVED','TARGET ≤ 10 WD · NO TIMESTAMP','#42618a',true],
      ['INVOICE RECEIVED','TARGET + 2 DAYS · NO TIMESTAMP','#42618a',true],
    ];
    nodes.forEach((node, index) => {
      const px = points[index], up = index % 2 === 0 ? -1 : 1;
      if (node[3]) make('circle', {cx:px,cy:y,r:18,fill:'none',stroke:'#42618a','stroke-width':2.6,'stroke-dasharray':'4 5'});
      else {
        make('circle', {cx:px,cy:y,r:20,fill:'#0b1d38',stroke:node[2],'stroke-width':3.6,style:`filter:drop-shadow(0 0 10px ${node[2]})`});
        make('circle', {cx:px,cy:y,r:7.5,fill:node[2]});
      }
      const anchor = index === nodes.length - 1 ? 'end' : 'middle';
      const ax = index === nodes.length - 1 ? px + 20 : px;
      make('line', {x1:px,y1:y+(up<0?-24:24),x2:px,y2:y+(up<0?-48:48),stroke:'#31527d','stroke-width':2});
      const label = make('text', {x:ax,y:y+(up<0?-60:66),'text-anchor':anchor,'class':'nlab'});
      label.textContent = node[0];
      const value = make('text', {x:ax,y:y+(up<0?-80:86),'text-anchor':anchor,'class':node[3]?'nnote':'nsub'});
      value.textContent = node[1];
      if (!node[3]) value.setAttribute('fill', node[2]);
    });
  }

  function drawerRow(left, right) {
    return `<div class="dr"><span class="a">${esc(left)}</span><span class="b">${right}</span></div>`;
  }

  function renderCircuits(data) {
    const cards = Array.from(document.querySelectorAll('.crow'));
    data.lanes.forEach((lane, index) => {
      const card = cards[index];
      if (!card) return;
      const row = ROWS[index];
      const oldKey = row.key;
      const dynamic = {
        pos: `P${index + 1}`,
        cls: index === 0 ? 'p1' : index === data.lanes.length - 1 ? 'last' : '',
        team: lane.division === 'Facilities Management' ? 'FACILITIES MGMT' : lane.division.toUpperCase(),
        ty: lane.type,
        tot: one(lane.medianWd),
        p90: Math.round(lane.p90Wd),
        n: lane.n,
        within: one(lane.within10Pct),
        legs: [lane.sectors.raisedToSubmitted, lane.sectors.submittedToPo, lane.sectors.poToLpo],
      };
      Object.assign(row, dynamic);
      card.classList.remove('p1','last');
      if (dynamic.cls) card.classList.add(dynamic.cls);
      card.querySelector('.pos').textContent = dynamic.pos;
      card.querySelector('.tn').textContent = dynamic.team;
      const badge = card.querySelector('.tb');
      badge.textContent = dynamic.ty;
      badge.className = `tb ${dynamic.ty === 'PR' ? 'tbpr' : 'tbcpr'}`;
      card.querySelector('.r2 .m').innerHTML = `${dynamic.tot}<span> WD MEDIAN</span>`;
      card.querySelector('.r3').innerHTML = `p90 <b>${dynamic.p90} wd</b> · n=<b>${dynamic.n}</b> · within target <b>${dynamic.within}%</b> · on track <b>${lane.liveCount}</b>`;
      const projects = lane.drill.projects.map(item => drawerRow(item.name, `${one(item.medianWd)}wd <span>n=${item.n}</span>`)).join('');
      const departments = lane.drill.departments.map(item => drawerRow(item.name, `${one(item.medianWd)}wd <span>n=${item.n}</span>`)).join('');
      const holders = lane.drill.holders.map(item => drawerRow(item.name, `${item.count} PRs <span>· ${one(item.medianAgeWd)}wd</span>`)).join('');
      const oldest = lane.drill.oldest.map(item => drawerRow(`${item.number} · ${item.project}`, `${item.ageWd}wd`)).join('');
      card.querySelector('.drawer').innerHTML = `<div><div class="dh">SLOWEST PROJECTS</div>${projects}</div><div><div class="dh">SLOWEST DEPARTMENTS</div>${departments}</div><div><div class="dh">WHO HOLDS NOW</div>${holders}</div><div><div class="dh">OLDEST ON TRACK</div>${oldest}</div>`;
      const drill = DRILL[oldKey];
      Object.assign(drill, {
        live: lane.liveCount,
        proj: lane.drill.projects.map(item => [item.name,item.medianWd,item.n]),
        dept: lane.drill.departments.map(item => [item.name,item.medianWd,item.n]),
        hold: lane.drill.holders.map(item => [item.name,item.count,item.medianAgeWd]),
        old: lane.drill.oldest.map(item => [item.ageWd,item.number,item.holder,item.project,null]),
      });
      drawLane(card.querySelector('svg'), row);
    });
  }

  function countUp(target) {
    const element = document.querySelector('.hn .n');
    if (evidenceMode) {
      element.innerHTML = `${one(target)}<span> WD</span>`;
      const force = () => {
        if (element.childNodes[0] && element.childNodes[0].textContent !== one(target)) element.childNodes[0].textContent = one(target);
      };
      new MutationObserver(force).observe(element, {subtree:true,childList:true,characterData:true});
      return;
    }
    element.innerHTML = `0.0<span> WD</span>`;
    let start;
    function frame(timestamp) {
      start = start || timestamp;
      const progress = Math.min(1, (timestamp - start) / 1100);
      element.childNodes[0].textContent = (target * (1 - Math.pow(1 - progress, 3))).toFixed(1);
      if (progress < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function applyData(data) {
    const head = data.headline, target = data.targets.raisedToGoodsWd;
    countUp(head.lpoMedianWd);
    document.querySelector('.hn .sub .behind').textContent = `${head.lpoMedianWd >= target ? '+' : '−'}${one(Math.abs(head.lpoMedianWd - target))} WD vs TARGET`;
    document.querySelector('.hn .sub .t:last-child').textContent = `n=${whole(head.completed)} · ${one(head.within10Pct)}% WITHIN · P90 ${Math.round(head.p90Wd)}`;
    const liveValues = document.querySelectorAll('.lm .lmk .v');
    liveValues[0].textContent = whole(data.live.count);
    liveValues[1].innerHTML = `${one(data.live.within10Pct)}% <i class="${data.live.within10Delta < 0 ? 'bad' : 'good'}">${data.live.within10Delta < 0 ? '▼' : '▲'}${Math.abs(data.live.within10Delta)}</i>`;
    liveValues[2].innerHTML = `${one(data.live.medianAgeWd).replace('.0','')} wd <i class="${data.live.medianAgeDelta > 0 ? 'bad' : 'good'}">${data.live.medianAgeDelta > 0 ? '▲' : '▼'}${Math.abs(data.live.medianAgeDelta)}</i>`;
    liveValues[3].textContent = `${data.live.finishedToday} · ${data.live.raisedToday}`;
    renderTrend(data);
    renderJourney(data);
    renderCircuits(data);

    const pitCards = document.querySelectorAll('.pit .pc');
    const gateNames = {raisedToSubmitted:'RAISED → SUBMITTED',submittedToPo:'SUBMITTED → PO',poToLpo:'PO → LPO'};
    pitCards[0].querySelector('.v').textContent = `${data.pitWall.slowestGate.lane} · ${gateNames[data.pitWall.slowestGate.sector]}`;
    pitCards[0].querySelector('.n').innerHTML = `${one(data.pitWall.slowestGate.medianWd).replace('.0','')} <span>WD</span>`;
    const queue = data.pitWall.deepestQueue;
    pitCards[1].querySelector('.v').textContent = queue.gate.toUpperCase();
    pitCards[1].querySelector('.n').innerHTML = `${whole(queue.count)} <span>PRs · ${one(queue.medianDays)}d dwell</span>`;
    pitCards[1].querySelector('small').innerHTML = `desks: ${queue.holders.slice(0,2).map(item => `<b>${esc(item.name)}</b> ${item.count}`).join(' · ')}`;
    const project = data.pitWall.slowestProject;
    pitCards[2].querySelector('.v').textContent = project.name.toUpperCase();
    pitCards[2].querySelector('.n').innerHTML = `${one(project.medianWd)} <span>WD · n=${project.n}</span>`;
    pitCards[3].querySelector('small').innerHTML = `<b>${whole(data.pitWall.legacy.count)} pre-April CPRs</b> arrived from CRM without department / location (integration gap, fixed ~Apr 2026). Backfill from CRM quotes; until then they are excluded from this board.`;
    const topTwo = queue.holders.slice(0,2).reduce((sum,item) => sum + item.count, 0);
    document.querySelector('.next .v').textContent = `CLEAR THE ${queue.gate.toUpperCase()} QUEUE`;
    document.querySelector('.next .d').innerHTML = `<b>${whole(queue.count)} PRs at one step</b> — the deepest live queue and the engine of the Submitted→PO constraint. The top two desks hold ${whole(topTwo)} of this queue.`;
    const stamp = new Date(data.meta.asOfTimestamp);
    document.querySelector('.liveclk').innerHTML = `<i></i>LIVE · ${stamp.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}).toUpperCase()} · ${stamp.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',hour12:false})}`;
    if (evidenceMode) {
      document.getElementById('stage').classList.add('on');
      document.querySelectorAll('.rv0').forEach(node => { node.style.opacity = '1'; node.style.transform = 'none'; });
      document.querySelectorAll('.bar2').forEach(node => node.style.transform = 'scaleY(1)');
      document.getElementById('jl').style.clipPath = 'none';
    }
    document.getElementById('stage').classList.add('data-ready');
  }

  fetch(`journey_board.json?t=${Date.now()}`)
    .then(response => {
      if (!response.ok) throw new Error(`Journey data HTTP ${response.status}`);
      return response.json();
    })
    .then(applyData)
    .catch(error => {
      const note = document.createElement('div');
      note.style.cssText = 'position:fixed;left:20px;bottom:20px;z-index:100;background:#7f1d1d;color:white;padding:10px 14px;border-radius:8px;font:600 12px Montserrat';
      note.textContent = `Journey data unavailable: ${error.message}`;
      document.body.appendChild(note);
    });
})();
