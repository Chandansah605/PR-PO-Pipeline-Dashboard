const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const start = html.indexOf('const MSAL_CONFIG =');
const end = html.indexOf('</script>', start);
if(start < 0 || end < 0) throw new Error('Authentication script was not found');
const authScript = html.slice(start, end);

function deferred(){
  let resolve;
  let reject;
  const promise = new Promise((res, rej)=>{ resolve = res; reject = rej; });
  return { promise, resolve, reject };
}

function createHarness(options = {}){
  const storage = new Map();
  const elements = new Map();
  const calls = { popup: 0, redirect: 0, activeAccount: null, boot: 0 };
  const redirectResult = options.redirectResult === undefined ? Promise.resolve(null) : options.redirectResult;
  const popupResult = options.popupResult === undefined
    ? Promise.resolve({ account: { name: 'Normal User', username: 'normal@striveservicesgroup.com' } })
    : options.popupResult;
  const instance = {
    handleRedirectPromise(){ return redirectResult; },
    loginPopup(){ calls.popup += 1; return popupResult; },
    loginRedirect(){ calls.redirect += 1; return Promise.resolve(); },
    setActiveAccount(account){ calls.activeAccount = account; },
    logoutPopup(){ return Promise.resolve(); }
  };
  const windowObject = {
    location: { origin: 'https://strive-services-group.github.io', pathname: '/PR-PO-Pipeline-Dashboard/' },
    opener: options.popupWindow ? {} : null,
    name: options.windowName || '',
    matchMedia(){ return { matches: Boolean(options.standalone) }; },
    __dashInited: false
  };
  windowObject.self = windowObject;
  windowObject.top = windowObject;
  const document = {
    getElementById(id){
      if(id === 'fallingLines') return null;
      if(!elements.has(id)){
        elements.set(id, {
          style: { display: '' }, innerText: '', innerHTML: '',
          classList: { add(){} }
        });
      }
      return elements.get(id);
    },
    createElement(){ return { style: {}, className: '' }; }
  };
  const context = vm.createContext({
    console: { error(){} },
    document,
    location: windowObject.location,
    window: windowObject,
    sessionStorage: {
      getItem(key){ return storage.has(key) ? storage.get(key) : null; },
      setItem(key, value){ storage.set(key, String(value)); },
      removeItem(key){ storage.delete(key); }
    },
    setTimeout(fn){ fn(); },
    msal: { PublicClientApplication: function(){ return instance; } },
    showLoader(){}, hideLoader(){}, rebuild(){}, loadLive(){ calls.boot += 1; return Promise.resolve(); }
  });
  vm.runInContext(authScript, context);
  return { calls, context, elements, storage };
}

async function flush(){
  await Promise.resolve();
  await new Promise(resolve=>setImmediate(resolve));
}

test('popup window uses redirect without attempting a nested popup', async ()=>{
  const h = createHarness({ popupWindow: true });
  await flush();
  await h.context.signIn();
  assert.equal(h.calls.popup, 0);
  assert.equal(h.calls.redirect, 1);
});

test('named and standalone windows use redirect', async ()=>{
  for(const options of [{ windowName: 'dashboard-popup' }, { standalone: true }]){
    const h = createHarness(options);
    await flush();
    await h.context.signIn();
    assert.equal(h.calls.popup, 0);
    assert.equal(h.calls.redirect, 1);
  }
});

test('normal tab keeps popup sign-in and completes the session', async ()=>{
  const h = createHarness();
  await flush();
  await h.context.signIn();
  assert.equal(h.calls.popup, 1);
  assert.equal(h.calls.redirect, 0);
  assert.equal(h.storage.get('strive_auth'), 'true');
  assert.equal(h.storage.get('strive_user'), 'normal@striveservicesgroup.com');
  assert.equal(h.calls.activeAccount.username, 'normal@striveservicesgroup.com');
});

test('popup-related MSAL failure falls back to redirect', async ()=>{
  const popupError = Object.assign(new Error('Request was blocked inside a popup because MSAL detected it was running in a popup.'), {
    errorCode: 'block_nested_popups'
  });
  const h = createHarness({ popupResult: Promise.reject(popupError) });
  await h.context.signIn();
  assert.equal(h.calls.popup, 1);
  assert.equal(h.calls.redirect, 1);
  assert.equal(h.elements.get('loginErr').style.display, 'none');
});

test('redirect response restores the same signed-in session', async ()=>{
  const result = deferred();
  const h = createHarness({ redirectResult: result.promise });
  result.resolve({ account: { name: 'Redirect User', username: 'redirect@striveservicesgroup.com' } });
  await flush();
  assert.equal(h.storage.get('strive_auth'), 'true');
  assert.equal(h.storage.get('strive_user'), 'redirect@striveservicesgroup.com');
  assert.equal(h.calls.activeAccount.username, 'redirect@striveservicesgroup.com');
  assert.equal(h.context.window.__dashInited, true);
});

test('cancelled sign-in displays plain language without MSAL internals', async ()=>{
  const h = createHarness({ popupResult: Promise.reject({ errorCode: 'user_cancelled', errorMessage: 'library details' }) });
  await h.context.signIn();
  const error = h.elements.get('loginErr');
  assert.equal(error.innerText, 'Sign-in was cancelled. Please try again.');
  assert.equal(error.style.display, 'block');
  assert.doesNotMatch(error.innerText, /user_cancelled|library details/i);
});

test('sign-in waits for redirect handling before starting interaction', async ()=>{
  const result = deferred();
  const h = createHarness({ redirectResult: result.promise });
  const signInPromise = h.context.signIn();
  await flush();
  assert.equal(h.calls.popup, 0);
  result.resolve(null);
  await signInPromise;
  assert.equal(h.calls.popup, 1);
});
