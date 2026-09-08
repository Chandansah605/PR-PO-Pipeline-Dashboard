'use strict';

const fs = require('node:fs');
const fsp = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = process.argv[2] || 'http://127.0.0.1:43991/';
const outputDir = path.resolve(__dirname);

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function waitForPort(profileDir) {
  const marker = path.join(profileDir, 'DevToolsActivePort');
  for (let attempt = 0; attempt < 100; attempt += 1) {
    if (fs.existsSync(marker)) return Number((await fsp.readFile(marker, 'utf8')).split(/\r?\n/)[0]);
    await delay(100);
  }
  throw new Error('Chrome DevTools port did not become available.');
}

async function waitForPageTarget(port) {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then(response => response.json());
    const page = targets.find(target => target.type === 'page' && target.url.startsWith(targetUrl));
    if (page) return page;
    await delay(100);
  }
  throw new Error(`QA page target not found for ${targetUrl}.`);
}

function connect(url) {
  const socket = new WebSocket(url);
  let id = 0;
  const pending = new Map();
  const listeners = new Map();
  socket.onmessage = event => {
    const message = JSON.parse(event.data);
    if (message.id) {
      const waiter = pending.get(message.id);
      if (!waiter) return;
      pending.delete(message.id);
      if (message.error) waiter.reject(new Error(message.error.message));
      else waiter.resolve(message.result);
      return;
    }
    for (const listener of listeners.get(message.method) || []) listener(message.params);
  };
  return {
    ready: new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; }),
    send(method, params = {}) {
      id += 1;
      const requestId = id;
      socket.send(JSON.stringify({ id: requestId, method, params }));
      return new Promise((resolve, reject) => pending.set(requestId, { resolve, reject }));
    },
    on(method, listener) {
      if (!listeners.has(method)) listeners.set(method, []);
      listeners.get(method).push(listener);
    },
    close() { socket.close(); }
  };
}

function runProcess(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: 'inherit', windowsHide: true });
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}`)));
  });
}

async function main() {
  await fsp.mkdir(outputDir, { recursive: true });
  const profileDir = await fsp.mkdtemp(path.join(os.tmpdir(), 'prpo-empty-straight-chrome-'));
  const frameDir = await fsp.mkdtemp(path.join(os.tmpdir(), 'prpo-empty-straight-frames-'));
  const chrome = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=0',
    '--remote-allow-origins=*',
    '--disable-extensions',
    '--hide-scrollbars',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=' + profileDir,
    targetUrl
  ], { stdio: 'ignore', windowsHide: true });

  try {
    const port = await waitForPort(profileDir);
    const page = await waitForPageTarget(port);
    const cdp = connect(page.webSocketDebuggerUrl);
    await cdp.ready;
    await cdp.send('Page.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
    await cdp.send('Page.reload', { ignoreCache: true });

    for (let attempt = 0; attempt < 100; attempt += 1) {
      const ready = await cdp.send('Runtime.evaluate', { expression: 'Boolean(window.__lightsOutSignin)', returnByValue: true });
      if (ready.result.value) break;
      if (attempt === 99) throw new Error('Sign-in scene did not initialise.');
      await delay(50);
    }

    const frames = [];
    cdp.on('Page.screencastFrame', frame => {
      frames.push({ data: frame.data, timestamp: frame.metadata.timestamp });
      void cdp.send('Page.screencastFrameAck', { sessionId: frame.sessionId });
    });
    await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 78, maxWidth: 960, maxHeight: 540, everyNthFrame: 2 });

    const expression = `(async()=>{
      const cv=document.getElementById('loginWorld'),scratch=document.createElement('canvas');
      scratch.width=64;scratch.height=36;const sampleCtx=scratch.getContext('2d',{willReadFrequently:true});
      const samples=[],labels=new Set();let lastSample=-Infinity;
      const started=performance.now();window.__lightsOutSignin.run();
      await new Promise(resolve=>{
        function sample(now){
          labels.add(document.getElementById('loginButtonText').textContent);
          const elapsed=now-started;
          if(now-lastSample>=100){
            lastSample=now;sampleCtx.drawImage(cv,0,0,64,36);
            const pixels=sampleCtx.getImageData(0,0,64,36).data;let total=0,red=0;
            for(let i=0;i<pixels.length;i+=4){const r=pixels[i],g=pixels[i+1],b=pixels[i+2];total+=(.2126*r+.7152*g+.0722*b)/255*100;if(r>180&&r>g*1.5&&r>b*1.3)red++}
            samples.push({t:elapsed,luma:total/(pixels.length/4),brightRedPixels:red});
          }
          if(elapsed<7000)requestAnimationFrame(sample);else resolve();
        }
        requestAnimationFrame(sample);
      });
      const resting=samples.filter(sample=>sample.t<800).reduce((sum,sample)=>sum+sample.luma,0)/samples.filter(sample=>sample.t<800).length;
      const maximum=Math.max(...samples.map(sample=>sample.luma));
      const nearest=t=>samples.reduce((best,sample)=>Math.abs(sample.t-t)<Math.abs(best.t-t)?sample:best,samples[0]);
      return {restingBrightness:resting,maximumBrightness:maximum,brightnessRise:maximum-resting,brightnessRisePercent:(maximum-resting)/resting*100,redPixels:{rest:nearest(400),mid:nearest(3300),lightsOut:nearest(5600)},buttonLabels:[...labels],state:window.__lightsOutSignin.getState()};
    })()`;
    const measured = cdp.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });

    const captures = [
      { wait: 400, name: 'rest.jpg' },
      { wait: 2900, name: 'mid-transition.jpg' },
      { wait: 2300, name: 'lights-out.jpg' }
    ];
    for (const capture of captures) {
      await delay(capture.wait);
      const shot = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 90, fromSurface: true });
      await fsp.writeFile(path.join(outputDir, capture.name), Buffer.from(shot.data, 'base64'));
    }

    const sequenceResult = await measured;
    await cdp.send('Page.stopScreencast');
    await delay(200);
    const firstTimestamp = frames[0]?.timestamp || 0;
    const selected = frames.filter((_, index) => index === 0 || index === frames.length - 1 || index % 2 === 0);
    for (let index = 0; index < selected.length; index += 1) {
      const frame = selected[index];
      const elapsed = Math.max(0, frame.timestamp - firstTimestamp);
      const name = `${String(index).padStart(4, '0')}-${elapsed.toFixed(3)}.jpg`;
      await fsp.writeFile(path.join(frameDir, name), Buffer.from(frame.data, 'base64'));
    }
    await runProcess('python', [path.join(outputDir, 'render-capture.py'), frameDir, path.join(outputDir, 'full-sequence.webp')]);

    await cdp.send('Page.reload', { ignoreCache: true });
    for (let attempt = 0; attempt < 100; attempt += 1) {
      const ready = await cdp.send('Runtime.evaluate', { expression: 'Boolean(window.__lightsOutSignin)', returnByValue: true });
      if (ready.result.value) break;
      if (attempt === 99) throw new Error('Sign-in scene did not reinitialise for the isolated performance run.');
      await delay(50);
    }
    await delay(500);
    const performance = await cdp.send('Runtime.evaluate', {
      expression: `(async()=>{
        const deltas=[];let prior=0;const started=performance.now();window.__lightsOutSignin.run();
        await new Promise(resolve=>{function sample(now){if(prior)deltas.push(now-prior);prior=now;if(now-started<7000)requestAnimationFrame(sample);else resolve()}requestAnimationFrame(sample)});
        const sorted=deltas.slice().sort((a,b)=>a-b),sum=deltas.reduce((a,b)=>a+b,0),pick=q=>sorted[Math.min(sorted.length-1,Math.floor(sorted.length*q))];
        return {frames:deltas.length,durationMs:sum,fps:1000*deltas.length/sum,p50Ms:pick(.5),p95Ms:pick(.95),maxMs:sorted.at(-1),over20Ms:deltas.filter(value=>value>20).length,state:window.__lightsOutSignin.getState()};
      })()`,
      awaitPromise: true,
      returnByValue: true
    });

    await cdp.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
    await cdp.send('Page.reload', { ignoreCache: true });
    await delay(500);
    const reduced = await cdp.send('Runtime.evaluate', { expression: `({state:window.__lightsOutSignin.getState(),doneSectors:document.querySelectorAll('#loginSectors .done').length,button:document.getElementById('loginButtonText').textContent})`, returnByValue: true });

    await cdp.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'no-preference' }] });
    await cdp.send('Page.reload', { ignoreCache: true });
    await delay(500);
    await cdp.send('Runtime.evaluate', { expression: `window.__visibilityQa=[];document.addEventListener('visibilitychange',()=>window.__visibilityQa.push({hidden:document.hidden,state:window.__lightsOutSignin.getState()}))` });
    await cdp.send('Page.setWebLifecycleState', { state: 'frozen' });
    await delay(300);
    await cdp.send('Page.setWebLifecycleState', { state: 'active' });
    await delay(300);
    const visibility = await cdp.send('Runtime.evaluate', { expression: 'window.__visibilityQa', returnByValue: true });

    const report = {
      performance1920x1080: performance.result.value,
      sequenceBrightnessAndLampSamples: sequenceResult.result.value,
      capturedScreencastFrames: frames.length,
      encodedFrames: selected.length,
      reducedMotion: reduced.result.value,
      visibilityPause: visibility.result.value
    };
    await fsp.writeFile(path.join(outputDir, 'metrics.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report, null, 2));
    cdp.close();
  } finally {
    chrome.kill();
    await delay(500);
    for (const tempDir of [profileDir, frameDir]) {
      const resolved = path.resolve(tempDir);
      if (!resolved.startsWith(path.resolve(os.tmpdir()) + path.sep) || !path.basename(resolved).startsWith('prpo-empty-straight-')) {
        throw new Error(`Refusing to remove unexpected temporary path: ${resolved}`);
      }
      await fsp.rm(resolved, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    }
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
