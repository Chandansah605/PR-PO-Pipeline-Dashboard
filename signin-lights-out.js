(function(){
  'use strict';

  const overlay=document.getElementById('loginOverlay');
  const cv=document.getElementById('loginWorld');
  const ui=document.getElementById('loginUi');
  const callout=document.getElementById('loginCallout');
  const btn=document.getElementById('loginSignInButton');
  const btnText=document.getElementById('loginButtonText');
  const replayButton=document.getElementById('loginReplay');
  const motionButton=document.getElementById('loginMotion');
  const clock=document.getElementById('loginClock');
  const raceSessionLap=document.getElementById('loginRaceSessionLap');
  const sectors=Array.from(document.querySelectorAll('#loginSectors .login-sector'));
  const ctx=cv&&cv.getContext&&cv.getContext('2d');

  if(!ctx||sessionStorage.getItem('strive_auth')==='true'||overlay.classList.contains('hidden')){
    document.body.classList.remove('login-active');
    return;
  }

  let stopped=false;
  let motion=!window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let frameId=0,adaptivePaused=false,slowFrames=0;
  let clockId=0;
  let W=0,H=0,DPR=1,last=performance.now();
  let z=0,speed=0,targetSpeed=0,phase='hold',lit=0,shake=0,flash=0,mx=0,my=0,lap=0;
  let passed=[false,false,false,false,false];
  let sequenceTimers=[];
  let sayTimer=0;
  let carX=0;

  const STAGES=['PR RAISED','SOURCING','APPROVALS','PURCHASE ORDER','RECEIPT POSTED'];
  const GAP=300;
  const FIRST=520;
  const gantryZ=i=>FIRST+i*GAP;
  const LAPLEN=FIRST+5*GAP+200;
  const stars=Array.from({length:120},()=>({x:Math.random(),y:Math.random()*.55,s:Math.random()*1.4+.3,a:Math.random()}));
  const rain=Array.from({length:55},()=>({x:Math.random(),y:Math.random(),v:.3+Math.random()*.7}));
  const noise=document.createElement('canvas');
  const skyline=[];
  const crowd=Array.from({length:900},()=>({a:Math.random()}));
  let flashes=[];

  function overlayIsVisible(){
    return !stopped&&!document.hidden&&overlay&&!overlay.classList.contains('hidden');
  }

  function clearSequence(){
    sequenceTimers.forEach(clearTimeout);
    sequenceTimers=[];
    clearTimeout(sayTimer);
    sayTimer=0;
  }

  function tick(){
    if(!overlayIsVisible()) return;
    const d=new Date(new Date().toLocaleString('en-US',{timeZone:'Asia/Dubai'}));
    const p=n=>String(n).padStart(2,'0');
    clock.textContent=p(d.getHours())+':'+p(d.getMinutes())+':'+p(d.getSeconds());
    const session=Math.ceil((d.getDate()+new Date(d.getFullYear(),d.getMonth(),1).getDay())/7);
    raceSessionLap.textContent='Dubai · Race '+(d.getMonth()+1)+' · Session '+session+' · Lap '+d.getDate();
  }

  function startClock(){
    if(clockId||!overlayIsVisible()) return;
    tick();
    clockId=window.setInterval(tick,1000);
  }

  function stopClock(){
    if(clockId) window.clearInterval(clockId);
    clockId=0;
  }

  function resize(){
    if(stopped||!ctx) return;
    const area=window.innerWidth*window.innerHeight;
    const deviceDpr=Math.min(2,window.devicePixelRatio||1);
    DPR=Math.min(deviceDpr,Math.sqrt(500000/Math.max(1,area)));
    W=Math.max(1,cv.clientWidth);
    H=Math.max(1,cv.clientHeight);
    cv.width=Math.round(W*DPR);
    cv.height=Math.round(H*DPR);
    ctx.setTransform(DPR,0,0,DPR,0,0);
    if(!motion||adaptivePaused) drawScene(performance.now(),0);
  }

  const cam={h:46};
  const ROADW=110, KERB=22, VERGE=90, WALL=14;
  let vpX=0,vpY=0,projectionScale=1;
  function VP(){return {x:vpX,y:vpY}}
  function project(x,y,zz){const f=Math.max(1,zz),s=projectionScale/f;return {x:vpX+x*s,y:vpY+(cam.h-y)*s,s}}
  function quad(p0,p1,p2,p3,fill){ctx.fillStyle=fill;ctx.beginPath();ctx.moveTo(p0.x,p0.y);ctx.lineTo(p1.x,p1.y);ctx.lineTo(p2.x,p2.y);ctx.lineTo(p3.x,p3.y);ctx.closePath();ctx.fill()}
  function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath()}

  function buildTextures(){
    noise.width=noise.height=256;
    const nc=noise.getContext('2d');
    const id=nc.createImageData(256,256);
    for(let i=0;i<id.data.length;i+=4){const v=118+Math.random()*30;id.data[i]=v*.55;id.data[i+1]=v*.66;id.data[i+2]=v*.85;id.data[i+3]=255}
    nc.putImageData(id,0,0);
    let x=0,i=0;
    while(x<2200){const w=22+((i*37)%48),h=18+((i*53)%110);skyline.push({x,w,h,spire:i%9===4});x+=w+6;i++}
  }

  function drawSky(now){
    const v=VP();
    const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#030A14');g.addColorStop(.45,'#071A2E');g.addColorStop(.58,'#123A5F');g.addColorStop(.6,'#07182B');g.addColorStop(1,'#020609');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    const mxp=W*.78,myp=H*.16;const mg=ctx.createRadialGradient(mxp,myp,4,mxp,myp,140);mg.addColorStop(0,'rgba(220,232,243,.9)');mg.addColorStop(.06,'rgba(220,232,243,.8)');mg.addColorStop(.12,'rgba(156,192,224,.18)');mg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=mg;ctx.fillRect(0,0,W,H);
    stars.forEach(s=>{const tw=.5+.5*Math.sin(now/700+s.a*10);ctx.fillStyle='rgba(200,220,240,'+(.2+.5*tw)+')';ctx.fillRect(s.x*W,s.y*H*.9,s.s,s.s)});
    const rg=ctx.createRadialGradient(v.x,v.y,10,v.x,v.y,W*.55);rg.addColorStop(0,'rgba(120,170,215,.6)');rg.addColorStop(.25,'rgba(20,90,149,.22)');rg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=rg;ctx.fillRect(0,0,W,H);
    const off=-mx*40;
    skyline.forEach(b=>{const x=b.x*W/2200+off;const hh=b.h*(H/900);ctx.fillStyle='#061422';ctx.fillRect(x,v.y-hh,b.w*W/2200,hh);if(b.spire){ctx.beginPath();ctx.moveTo(x+b.w*W/4400,v.y-hh-hh*.9);ctx.lineTo(x+b.w*W/2200*.35,v.y-hh);ctx.lineTo(x+b.w*W/2200*.65,v.y-hh);ctx.closePath();ctx.fill()}ctx.fillStyle='rgba(156,192,224,.22)';for(let k=6;k<hh-4;k+=7){for(let c=3;c<b.w*W/2200-3;c+=6){if(((k*7+c*13+b.x)%11)<4)ctx.fillRect(x+c,v.y-hh+k,2,2)}}});
    const hz=ctx.createLinearGradient(0,v.y-40,0,v.y+2);hz.addColorStop(0,'rgba(18,58,95,0)');hz.addColorStop(1,'rgba(18,58,95,.55)');ctx.fillStyle=hz;ctx.fillRect(0,v.y-40,W,42);
  }

  function drawGround(){
    const v=VP();
    const gl=project(-(ROADW+KERB+VERGE),0,30),gr=project(ROADW+KERB+VERGE,0,30),fl=project(-(ROADW+KERB+VERGE),0,2200),fr=project(ROADW+KERB+VERGE,0,2200);
    ctx.fillStyle='#07131F';ctx.fillRect(0,v.y,W,H-v.y);quad(gl,gr,fr,fl,'#0B1C2C');
    const a=project(-ROADW,0,30),b=project(ROADW,0,30),c=project(ROADW,0,2200),d=project(-ROADW,0,2200);
    const rg=ctx.createLinearGradient(0,a.y,0,c.y);rg.addColorStop(0,'#141F2E');rg.addColorStop(.6,'#0E1A29');rg.addColorStop(1,'#0A1727');quad(a,b,c,d,rg);
    ctx.save();ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.lineTo(c.x,c.y);ctx.lineTo(d.x,d.y);ctx.closePath();ctx.clip();ctx.globalAlpha=.16;ctx.fillStyle=ctx.createPattern(noise,'repeat');ctx.translate(0,(z*.7)%256);ctx.fillRect(-256,-512,W+512,H+1024);ctx.globalAlpha=1;ctx.restore();
    ctx.save();ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.lineTo(c.x,c.y);ctx.lineTo(d.x,d.y);ctx.closePath();ctx.clip();[[-70,-40],[40,70]].forEach(([x0,x1])=>{const p0=project(x0,0,30),p1=project(x1,0,30),p2=project(x1*.6,0,2200),p3=project(x0*.6,0,2200);const lg=ctx.createLinearGradient(0,p0.y,0,p2.y);lg.addColorStop(0,'rgba(0,0,0,.35)');lg.addColorStop(1,'rgba(0,0,0,0)');quad(p0,p1,p2,p3,lg)});ctx.restore();
    const seg=55,startZ=Math.floor(z/seg)*seg,far=z+2200;
    for(let zz=startZ;zz<far;zz+=seg){const rel0=zz-z,rel1=zz+seg-z;if(rel1<30)continue;const r0=Math.max(30,rel0),stripe=Math.floor(zz/seg)%2===0,fade=Math.max(0,1-rel0/2600);
      [-1,1].forEach(side=>{
        const k0=project(side*ROADW,0,r0),k1=project(side*(ROADW+KERB),0,r0),k2=project(side*(ROADW+KERB),0,rel1),k3=project(side*ROADW,0,rel1);quad(k0,k1,k2,k3,stripe?'rgba(228,56,48,'+(.55+.4*fade)+')':'rgba(236,241,247,'+(.6+.35*fade)+')');
        const l0=project(side*ROADW,0,r0),l1=project(side*(ROADW+3),1.5,r0),l2=project(side*(ROADW+3),1.5,rel1),l3=project(side*ROADW,0,rel1);quad(l0,l1,l2,l3,'rgba(0,0,0,.35)');
        const e0=project(side*(ROADW-6),0,r0),e1=project(side*(ROADW-2),0,r0),e2=project(side*(ROADW-2),0,rel1),e3=project(side*(ROADW-6),0,rel1);quad(e0,e1,e2,e3,'rgba(230,236,244,'+(.5+.3*fade)+')');
        const w0=project(side*(ROADW+KERB+VERGE),0,r0),w1=project(side*(ROADW+KERB+VERGE),WALL,r0),w2=project(side*(ROADW+KERB+VERGE),WALL,rel1),w3=project(side*(ROADW+KERB+VERGE),0,rel1);quad(w0,w1,w2,w3,stripe?'rgba(160,178,200,'+(.35+.4*fade)+')':'rgba(97,143,180,'+(.35+.4*fade)+')');
        const t0=project(side*(ROADW+KERB+VERGE),WALL,r0),t1=project(side*(ROADW+KERB+VERGE+6),WALL,r0),t2=project(side*(ROADW+KERB+VERGE+6),WALL,rel1),t3=project(side*(ROADW+KERB+VERGE),WALL,rel1);quad(t0,t1,t2,t3,'rgba(200,214,230,'+(.25+.3*fade)+')');
        if(Math.floor(zz/(seg*4))%3!==1){const g0=project(side*(ROADW+KERB+VERGE+30),0,r0),g1=project(side*(ROADW+KERB+VERGE+30),60,r0),g2=project(side*(ROADW+KERB+VERGE+30),60,rel1),g3=project(side*(ROADW+KERB+VERGE+30),0,rel1);quad(g0,g1,g2,g3,'rgba(10,26,44,'+(.7+.3*fade)+')');for(let r=1;r<=3;r++){for(let c2=0;c2<4;c2++){const yy=r*15,zz2=r0+(rel1-r0)*(c2+.5)/4,q=project(side*(ROADW+KERB+VERGE+30),yy,zz2),idx=(Math.floor(zz/seg)*7+r*3+c2)%crowd.length,cr=crowd[idx];ctx.fillStyle='rgba('+(120+cr.a*100)+','+(140+cr.a*80)+','+(170+cr.a*60)+','+(.35+.5*fade)+')';ctx.fillRect(q.x-q.s*2,q.y-q.s*2,Math.max(1,q.s*4),Math.max(1,q.s*4))}}}
      });
      if(stripe){const q0=project(-4,0,r0),q1=project(4,0,r0),q2=project(4,0,rel1),q3=project(-4,0,rel1);quad(q0,q1,q2,q3,'rgba(156,192,224,'+(.25+.25*fade)+')')}
    }
    const fz=LAPLEN*(lap+1)-z-60;if(fz>30&&fz<2600){for(let i=0;i<12;i++){for(let j=0;j<2;j++){const x0=-ROADW+i*(ROADW*2/12),x1=x0+ROADW*2/12;quad(project(x0,0,fz+j*12),project(x1,0,fz+j*12),project(x1,0,fz+(j+1)*12),project(x0,0,fz+(j+1)*12),(i+j)%2?'#EEF4FA':'#0A1523')}}}
    for(let zz=startZ;zz<far;zz+=seg*6){const rel=zz-z;if(rel<30)continue;[-1,1].forEach(side=>{const p=project(side*(ROADW+KERB+VERGE-10),0,rel),q=project(side*(ROADW+KERB+VERGE-10),90,rel),arm=project(side*(ROADW+KERB+20),90,rel);ctx.strokeStyle='rgba(120,150,180,'+Math.min(.7,80/rel)+')';ctx.lineWidth=Math.max(.6,q.s*3);ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.lineTo(arm.x,arm.y);ctx.stroke();const pool=project(side*(ROADW*.5),0,rel),pr=Math.max(4,pool.s*90),lg=ctx.createRadialGradient(pool.x,pool.y,0,pool.x,pool.y,pr);lg.addColorStop(0,'rgba(200,225,250,.16)');lg.addColorStop(1,'rgba(200,225,250,0)');ctx.fillStyle=lg;ctx.save();ctx.translate(pool.x,pool.y);ctx.scale(1,.35);ctx.translate(-pool.x,-pool.y);ctx.fillRect(pool.x-pr,pool.y-pr,pr*2,pr*2);ctx.restore();ctx.fillStyle='#EAF3FF';ctx.beginPath();ctx.arc(arm.x,arm.y,Math.max(.8,arm.s*2),0,7);ctx.fill()})}
  }

  function stageState(i){if(phase==='hold'||phase==='lights')return i<lit?'red':'idle';return passed[i]?'green':'next'}

  function drawGantries(){
    for(let L=lap;L<=lap+1;L++){for(let i=4;i>=0;i--){const zz=L*LAPLEN+gantryZ(i),rel=zz-z;if(rel<4||rel>2200)continue;const alpha=Math.min(1,Math.max(0,(2200-rel)/1000)),X=ROADW+KERB+30,y1=112,y2=130;ctx.globalAlpha=alpha;
      [-1,1].forEach(side=>{const p=project(side*X,0,rel),q=project(side*X,y2,rel),pw=Math.max(1.5,p.s*10);ctx.strokeStyle='#1A3352';ctx.lineWidth=pw;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();ctx.strokeStyle='#3D6390';ctx.lineWidth=pw*.35;ctx.beginPath();ctx.moveTo(p.x-pw*.25,p.y);ctx.lineTo(q.x-pw*.25,q.y);ctx.stroke();const f=project(side*X,0,rel);ctx.fillStyle='#22406A';ctx.fillRect(f.x-pw*.9,f.y-pw*.3,pw*1.8,pw*.6)});
      const bl=project(-X,y1,rel),br=project(X,y1,rel),tl=project(-X,y2,rel),tr=project(X,y2,rel);quad(bl,br,tr,tl,'#0F2238');ctx.strokeStyle='rgba(97,143,180,.9)';ctx.lineWidth=Math.max(.6,bl.s*1.2);ctx.beginPath();ctx.moveTo(bl.x,bl.y);ctx.lineTo(br.x,br.y);ctx.lineTo(tr.x,tr.y);ctx.lineTo(tl.x,tl.y);ctx.closePath();ctx.stroke();const ul=project(-X,y1,rel+8),ur=project(X,y1,rel+8);quad(bl,br,ur,ul,'rgba(156,192,224,.25)');ctx.strokeStyle='rgba(97,143,180,.5)';ctx.lineWidth=Math.max(.4,bl.s*.6);for(let k=0;k<10;k++){const xa=-X+2*X*(k/10),xb=-X+2*X*((k+1)/10),a1=project(xa,y1,rel),a2=project(xb,y2,rel);ctx.beginPath();ctx.moveTo(a1.x,a1.y);ctx.lineTo(a2.x,a2.y);ctx.stroke()}
      const sw=ROADW*1.7,sh=40,s0=project(-sw/2,y1-sh-2,rel),s1=project(sw/2,y1-2,rel),w=s1.x-s0.x,h=s0.y-s1.y;
      if(w>10){const state=L===lap?stageState(i):'idle',col=state==='red'?'#FF5A4F':state==='green'?'#3DDC84':state==='next'?'#9CC0E0':'#618FB4';ctx.shadowColor=col;ctx.shadowBlur=state==='idle'?h*.1:h*.35;const pg=ctx.createLinearGradient(0,s1.y,0,s1.y+h);pg.addColorStop(0,'#12263F');pg.addColorStop(1,'#08172A');ctx.fillStyle=pg;roundRect(s0.x,s1.y,w,h,Math.min(8,h*.15));ctx.fill();ctx.shadowBlur=0;ctx.strokeStyle=col;ctx.lineWidth=Math.max(.7,h*.035);ctx.stroke();ctx.strokeStyle='rgba(255,255,255,.12)';ctx.lineWidth=Math.max(.4,h*.015);roundRect(s0.x+h*.06,s1.y+h*.06,w-h*.12,h-h*.12,Math.min(6,h*.1));ctx.stroke();const lr=h*.17,lx=s0.x+w*.12,ly=s1.y+h*.5;ctx.fillStyle='#0B1220';ctx.beginPath();ctx.arc(lx,ly,lr*1.35,0,7);ctx.fill();const lamp=state==='red'?'#FF5A4F':state==='green'?'#3DDC84':state==='next'?'#DCE8F3':'#1C1418';if(state!=='idle'){ctx.shadowColor=lamp;ctx.shadowBlur=lr*3}const lgd=ctx.createRadialGradient(lx-lr*.3,ly-lr*.3,lr*.1,lx,ly,lr);lgd.addColorStop(0,state==='idle'?'#2A1E23':'#fff');lgd.addColorStop(.35,lamp);lgd.addColorStop(1,state==='idle'?'#0E0A0C':lamp);ctx.fillStyle=lgd;ctx.beginPath();ctx.arc(lx,ly,lr,0,7);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#EEF4FA';ctx.textBaseline='middle';ctx.textAlign='left';ctx.font='800 '+Math.max(4,h*.34)+'px Montserrat, Segoe UI, sans-serif';ctx.fillText(STAGES[i],s0.x+w*.22,s1.y+h*.48);ctx.fillStyle='rgba(147,169,194,.9)';ctx.font='600 '+Math.max(3,h*.16)+'px Titillium Web, Segoe UI, sans-serif';ctx.fillText('S'+(i+1)+'  ·  STAGE '+(i+1)+' OF 5',s0.x+w*.22,s1.y+h*.82);const v=VP(),ry=v.y+(v.y-(s1.y+h/2))*.9;ctx.save();ctx.globalAlpha=alpha*.18;ctx.fillStyle=col;ctx.fillRect(s0.x,ry-h*.2,w,h*.4);ctx.restore()}
      ctx.globalAlpha=1;
    }}
  }

  function drawCar(now){
    const rel=250+Math.sin(now/1300)*10,carSway=Math.sin(now/900)*18+Math.sin(now/2300)*10;carX+=(carSway-carX)*.05;const P=(x,y,dz)=>project(carX+x,y,rel+(dz||0)),s=P(0,0).s,shadow=P(0,0);ctx.fillStyle='rgba(0,0,0,.55)';ctx.save();ctx.translate(shadow.x,shadow.y);ctx.scale(1,.28);ctx.beginPath();ctx.arc(0,0,30*s,0,7);ctx.fill();ctx.restore();
    if(speed>3){ctx.fillStyle='rgba(180,205,230,.10)';for(let i=0;i<8;i++){const q=P((Math.random()-.5)*70,Math.random()*12,-(4+Math.random()*30));ctx.beginPath();ctx.arc(q.x,q.y,Math.max(1,q.s*(3+Math.random()*6)),0,7);ctx.fill()}}
    [-1,1].forEach(side=>{const t=P(side*30,0),tt=P(side*30,16),tw=14*s,th=t.y-tt.y;ctx.fillStyle='#0B0F14';roundRect(t.x-tw/2,tt.y,tw,th,tw*.45);ctx.fill();const rim=ctx.createRadialGradient(t.x,tt.y+th*.5,0,t.x,tt.y+th*.5,tw*.34);rim.addColorStop(0,'#3A4654');rim.addColorStop(1,'#141A22');ctx.fillStyle=rim;ctx.beginPath();ctx.arc(t.x,tt.y+th*.5,tw*.32,0,7);ctx.fill()});
    quad(P(-26,0),P(26,0),P(22,6),P(-22,6),'#0A121C');const b0=P(-16,6),b1=P(16,6),b2=P(9,22),b3=P(-9,22),bg=ctx.createLinearGradient(b3.x,b3.y,b0.x,b0.y);bg.addColorStop(0,'#2C74B5');bg.addColorStop(.5,'#145A95');bg.addColorStop(1,'#0E3F6E');quad(b0,b1,b2,b3,bg);quad(P(-3,6),P(3,6),P(2,22),P(-2,22),'rgba(238,244,250,.85)');quad(P(-6,22),P(6,22),P(3,30),P(-3,30),'#1F466B');const r0=P(-34,20),r1=P(34,20),r2=P(34,26),r3=P(-34,26);quad(r0,r1,r2,r3,'#0D1B2C');ctx.strokeStyle='#618FB4';ctx.lineWidth=Math.max(.6,s*1.2);ctx.beginPath();ctx.moveTo(r0.x,r0.y);ctx.lineTo(r1.x,r1.y);ctx.stroke();const rl=P(0,9);ctx.fillStyle=Math.floor(now/160)%2?'#FF3B30':'#7A1410';ctx.shadowColor='#FF3B30';ctx.shadowBlur=s*10;ctx.fillRect(rl.x-s*4,rl.y-s*2,s*8,s*4);ctx.shadowBlur=0;ctx.fillStyle='#EEF4FA';ctx.font='800 '+Math.max(3,s*3.6)+'px Montserrat, sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('STRIVE',P(0,23).x,P(0,23).y);
  }

  function drawSpeed(){
    const k=speed/9;if(k<.15)return;const v=VP();ctx.save();ctx.globalAlpha=Math.min(.5,(k-.15)*.9);ctx.strokeStyle='#9CC0E0';ctx.lineWidth=1;for(let i=0;i<40;i++){const a=i/40*Math.PI*2+z*.002,r0=Math.max(W,H)*(.24+(i*7%10)/40),r1=r0+60+k*180;ctx.beginPath();ctx.moveTo(v.x+Math.cos(a)*r0,v.y+Math.sin(a)*r0);ctx.lineTo(v.x+Math.cos(a)*r1,v.y+Math.sin(a)*r1);ctx.stroke()}ctx.restore();const vg=ctx.createRadialGradient(v.x,v.y,H*.25,v.x,v.y,Math.max(W,H)*.8);vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,'+Math.min(.6,k*.55)+')');ctx.fillStyle=vg;ctx.fillRect(0,0,W,H);
  }

  function drawRain(dt){ctx.strokeStyle='rgba(156,192,224,.20)';ctx.lineWidth=1;rain.forEach(r=>{if(motion){r.y+=r.v*dt*.0006*(1+speed/8);if(r.y>1){r.y=-.05;r.x=Math.random()}}const x=r.x*W,y=r.y*H;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-speed*.6,y+10+speed*1.2);ctx.stroke()})}
  function drawFlashes(now){if(motion&&Math.random()<.03)flashes.push({x:Math.random()<.5?Math.random()*W*.28:W*.72+Math.random()*W*.28,y:VP().y-10-Math.random()*90,t:now});flashes=flashes.filter(f=>now-f.t<180);flashes.forEach(f=>{const a=1-(now-f.t)/180;ctx.fillStyle='rgba(255,255,255,'+a*.9+')';ctx.beginPath();ctx.arc(f.x,f.y,1.5+a*2.5,0,7);ctx.fill()})}

  function drawScene(now,dt){
    if(!ctx||!W||!H) return;
    vpX=W*.36+mx*24;vpY=H*.58+my*14;projectionScale=H*.95;
    ctx.save();
    if(shake>0){ctx.translate((Math.random()-.5)*10*shake,(Math.random()-.5)*6*shake);shake=Math.max(0,shake-dt*.004)}
    drawSky(now);drawGround();drawGantries();drawCar(now);drawFlashes(now);drawRain(dt);drawSpeed();
    if(flash>0){ctx.fillStyle='rgba(156,192,224,'+flash*.35+')';ctx.fillRect(0,0,W,H);flash=Math.max(0,flash-dt*.006)}
    ctx.restore();
  }

  function frame(now){
    frameId=0;
    if(!overlayIsVisible()||!motion) return;
    const frameStarted=performance.now();
    const dt=Math.min(50,now-last);last=now;
    speed+=(targetSpeed-speed)*Math.min(1,dt*.0025);
    z+=speed*dt*.06;
    if(phase==='race'){
      for(let i=0;i<5;i++){const zz=lap*LAPLEN+gantryZ(i);if(!passed[i]&&z>zz){passed[i]=true;flash=1;shake=1;sectors[i].classList.add('hit');sequenceTimers.push(setTimeout(()=>{if(stopped)return;sectors[i].classList.remove('hit');sectors[i].classList.add('done')},420));if(i===4){say('Lap complete','green',1400);sequenceTimers.push(setTimeout(()=>{targetSpeed=2.5},900))}}}
      if(z>(lap+1)*LAPLEN){lap++;passed=[false,false,false,false,false];sectors.forEach(s=>s.classList.remove('done','hit'))}
    }
    drawScene(now,dt);
    const drawCost=performance.now()-frameStarted;
    slowFrames=drawCost>32?slowFrames+1:Math.max(0,slowFrames-1);
    if(slowFrames>=2){adaptivePaused=true;return}
    frameId=requestAnimationFrame(frame);
  }

  function startRendering(){
    if(frameId||adaptivePaused||!motion||!overlayIsVisible()) return;
    last=performance.now();
    frameId=requestAnimationFrame(frame);
  }

  function pauseRendering(){
    if(frameId) cancelAnimationFrame(frameId);
    frameId=0;
  }

  function say(text,colour,duration){
    callout.textContent=text;
    callout.className='login-callout show '+(colour||'');
    clearTimeout(sayTimer);
    if(duration)sayTimer=setTimeout(()=>callout.classList.remove('show'),duration);
  }

  function showLightsOutState(){
    phase='race';lit=0;passed=[true,true,true,true,true];sectors.forEach(s=>s.classList.add('done'));btn.classList.add('go');btnText.textContent='Lights out · Sign in';say('Lights out','green',0);
  }

  function redrawAdaptive(){
    if(adaptivePaused&&overlayIsVisible()) drawScene(performance.now(),0);
  }

  function run(){
    if(stopped) return;
    clearSequence();adaptivePaused=false;slowFrames=0;z=0;speed=0;targetSpeed=0;lit=0;lap=0;passed=[false,false,false,false,false];phase='hold';sectors.forEach(s=>s.classList.remove('done','hit'));btn.classList.remove('go');btnText.textContent='Sign in with Microsoft';callout.className='login-callout';callout.textContent='';
    if(!motion){showLightsOutState();drawScene(performance.now(),0);return}
    targetSpeed=.7;
    sequenceTimers.push(setTimeout(()=>{phase='lights';redrawAdaptive()},900));
    for(let i=1;i<=5;i++)sequenceTimers.push(setTimeout(()=>{lit=i;say(i===5?'5 lights':i+' light'+(i>1?'s':''),'red',600);redrawAdaptive()},900+i*720));
    sequenceTimers.push(setTimeout(()=>{phase='race';lit=0;targetSpeed=9;flash=1;shake=1.2;say('Lights out','green',1100);btn.classList.add('go');btnText.textContent='Lights out · Sign in';redrawAdaptive()},900+5*720+650+Math.random()*400));
    startRendering();
  }

  function handleMotionClick(){
    motion=!motion;
    motionButton.textContent=motion?'◎ Motion on':'◎ Motion off';
    ui.classList.toggle('still',!motion);
    if(motion)startRendering();else pauseRendering();
    run();
  }

  function handlePointerMove(event){
    if(!motion||!overlayIsVisible()) return;
    mx=event.clientX/W-.5;
    my=event.clientY/H-.5;
  }

  function handleVisibility(){
    if(document.hidden){pauseRendering();stopClock();return}
    if(overlayIsVisible()){startClock();if(motion)startRendering();else drawScene(performance.now(),0)}
  }

  function stop(){
    if(stopped) return;
    stopped=true;
    document.body.classList.remove('login-active');
    clearSequence();pauseRendering();stopClock();
    window.removeEventListener('resize',resize);
    window.removeEventListener('pointermove',handlePointerMove);
    document.removeEventListener('visibilitychange',handleVisibility);
    replayButton.removeEventListener('click',run);
    motionButton.removeEventListener('click',handleMotionClick);
    cv.width=1;cv.height=1;
  }

  window.stopLightsOutSignin=stop;
  window.__lightsOutSignin={getState:()=>({motion,phase,lit,stopped,adaptivePaused,frameActive:Boolean(frameId),clockActive:Boolean(clockId),dpr:DPR}),run,stop};

  buildTextures();
  replayButton.addEventListener('click',run);
  motionButton.addEventListener('click',handleMotionClick);
  window.addEventListener('resize',resize);
  window.addEventListener('pointermove',handlePointerMove,{passive:true});
  document.addEventListener('visibilitychange',handleVisibility);
  ui.classList.toggle('still',!motion);
  motionButton.textContent=motion?'◎ Motion on':'◎ Motion off';
  resize();startClock();run();
})();
