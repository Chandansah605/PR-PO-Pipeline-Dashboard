'use strict';

const fs = require('node:fs');
const fsp = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = process.argv[2] || 'http://127.0.0.1:8765/';
const outputDir = path.resolve(process.argv[3] || 'evidence');

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForPort(profileDir) {
  const marker = path.join(profileDir, 'DevToolsActivePort');
  for (let attempt = 0; attempt < 80; attempt += 1) {
    if (fs.existsSync(marker)) return Number((await fsp.readFile(marker, 'utf8')).split(/\r?\n/)[0]);
    await delay(100);
  }
  throw new Error('Chrome DevTools port did not become available.');
}

function cdpClient(url) {
  const socket = new WebSocket(url);
  let id = 0;
  const pending = new Map();
  socket.onmessage = event => {
    const message = JSON.parse(event.data);
    if (!message.id || !pending.has(message.id)) return;
    const waiter = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) waiter.reject(new Error(message.error.message));
    else waiter.resolve(message.result);
  };
  return {
    ready: new Promise((resolve, reject) => {
      socket.onopen = resolve;
      socket.onerror = () => reject(new Error('Unable to connect to Chrome DevTools.'));
    }),
    send(method, params) {
      id += 1;
      const requestId = id;
      return new Promise((resolve, reject) => {
        pending.set(requestId, { resolve, reject });
        socket.send(JSON.stringify({ id: requestId, method, params: params || {} }));
      });
    },
    close() { socket.close(); }
  };
}

async function waitForPageTarget(port) {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    const page = targets.find(target => target.type === 'page' && target.url.startsWith(targetUrl));
    if (page) return page;
    await delay(100);
  }
  throw new Error(`Chrome did not navigate to ${targetUrl}.`);
}

async function main() {
  await fsp.mkdir(outputDir, { recursive: true });
  const profileDir = await fsp.mkdtemp(path.join(os.tmpdir(), 'prpo-race-shot-'));
  const chrome = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=0',
    '--remote-allow-origins=*',
    '--disable-extensions',
    '--disable-gpu',
    '--hide-scrollbars',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=' + profileDir,
    targetUrl
  ], { stdio: 'ignore', windowsHide: true });

  try {
    const port = await waitForPort(profileDir);
    const page = await waitForPageTarget(port);
    await delay(750);
    const cdp = cdpClient(page.webSocketDebuggerUrl);
    await cdp.ready;
    for (let attempt = 0; attempt < 80; attempt += 1) {
      const loaded = await cdp.send('Runtime.evaluate', {
        expression: "typeof enterDashboard === 'function'",
        returnByValue: true
      });
      if (loaded.result.value === true) break;
      if (attempt === 79) throw new Error('Dashboard scripts did not finish loading.');
      await delay(100);
    }
    const authCall = await cdp.send('Runtime.evaluate', {
      expression: "sessionStorage.setItem('strive_auth','true');enterDashboard('Screenshot evidence')"
    });
    if (authCall.exceptionDetails) {
      throw new Error(`Unable to enter the local dashboard: ${JSON.stringify(authCall.exceptionDetails)}`);
    }
    await delay(7000);
    const ready = await cdp.send('Runtime.evaluate', {
      expression: "JSON.stringify({auth:sessionStorage.getItem('strive_auth'),race:!!document.querySelector('.rc-shell'),overlay:document.getElementById('loginOverlay').classList.contains('hidden')})",
      returnByValue: true
    });
    const state = JSON.parse(ready.result.value);
    if (state.auth !== 'true' || !state.race || !state.overlay) {
      throw new Error(`Race Control did not reach its authenticated first screen: ${JSON.stringify(state)}`);
    }

    for (const view of [{ name: 'desktop', width: 1440, height: 1000 }, { name: 'mobile', width: 412, height: 915 }]) {
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: view.width,
        height: view.height,
        deviceScaleFactor: 1,
        mobile: false
      });
      await cdp.send('Runtime.evaluate', { expression: 'scrollTo(0,0)' });
      await delay(250);
      const result = await cdp.send('Page.captureScreenshot', { format: 'png', fromSurface: true });
      const output = path.join(outputDir, `race-control-${view.name}.png`);
      await fsp.writeFile(output, Buffer.from(result.data, 'base64'));
      console.log(`${view.name}: ${view.width}x${view.height} -> ${output}`);
    }
    cdp.close();
  } finally {
    chrome.kill();
    await delay(750);
    try {
      await fsp.rm(profileDir, { recursive: true, force: true, maxRetries: 5, retryDelay: 250 });
    } catch (error) {
      console.warn(`Screenshot profile cleanup deferred: ${error.code || error.message}`);
    }
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
