const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const scene = fs.readFileSync(path.join(root, 'signin-lights-out.js'), 'utf8');
const logo = fs.readFileSync(path.join(root, 'strive-logo.svg'), 'utf8');

function tagAttributes(markup){
  return Array.from(markup.matchAll(/<(path|rect)\b([^>]*)\/?\s*>/g), match=>{
    const attrs = {};
    for(const attr of match[2].matchAll(/([\w:-]+)="([^"]*)"/g)) attrs[attr[1]] = attr[2];
    return { tag: match[1], ...attrs };
  });
}

test('signed-out markup exposes the required auth hooks immediately', ()=>{
  const button = html.match(/<button class="login-signin-btn" id="loginSignInButton"[^>]*>/);
  assert.ok(button, 'sign-in button was not found');
  assert.match(button[0], /onclick="signIn\(\)"/);
  assert.doesNotMatch(button[0], /\bdisabled\b/);
  assert.match(html, /@keyframes login-panel-slide\{from\{transform:translateX\(40px\);opacity:\.7\}/);
  for(const id of ['loginOverlay','loginUser','loginErr']) assert.match(html, new RegExp(`id="${id}"`));
});

test('approved scene and responsive states replace the legacy decoration', ()=>{
  for(const text of ['PR RAISED','SOURCING','APPROVALS','PURCHASE ORDER','RECEIPT POSTED']) assert.match(scene, new RegExp(text));
  assert.match(html, /@media \(max-width:899px\)/);
  assert.match(html, /@media \(prefers-reduced-motion:reduce\)/);
  assert.doesNotMatch(html, /fallingLines|falling-lines|signin-tags|login-rev/);
});

test('inline logo geometry is the repository logo geometry', ()=>{
  const inlineSvg = html.match(/<svg class="strive-mark"[\s\S]*?<\/svg>/);
  assert.ok(inlineSvg, 'inline Strive logo was not found');
  assert.deepEqual(tagAttributes(inlineSvg[0]), tagAttributes(logo));
});

test('scene lifecycle caps pixel density and stops all recurring work', ()=>{
  assert.match(scene, /deviceDpr=Math\.min\(2,window\.devicePixelRatio\|\|1\)/);
  assert.match(scene, /DPR=Math\.min\(deviceDpr,Math\.sqrt\(500000\/Math\.max\(1,area\)\)\)/);
  assert.match(scene, /if\(slowFrames>=2\)\{adaptivePaused=true;return\}/);
  assert.match(scene, /function redrawAdaptive\(\)/);
  assert.match(scene, /document\.hidden/);
  assert.match(scene, /cancelAnimationFrame\(frameId\)/);
  assert.match(scene, /window\.clearInterval\(clockId\)/);
  assert.match(scene, /window\.stopLightsOutSignin=stop/);
  assert.match(html, /if\(window\.stopLightsOutSignin\) window\.stopLightsOutSignin\(\)/);
});

test('signed-out load defers dashboard-only libraries and layout', ()=>{
  for(const asset of ['plotly-2.27.0.min.js','jquery-3.7.1.min.js','xlsx.full.min.js','dataverse-live.js','race-control.js']){
    assert.doesNotMatch(html, new RegExp(`<script[^>]+src="[^"]*${asset.replaceAll('.', '\\.')}`));
  }
  assert.match(html, /function ensureDashboardAssets\(\)/);
  assert.match(html, /await ensureDashboardAssets\(\)/);
  assert.match(html, /body\.login-active>:not\(#loginOverlay\):not\(script\)/);
  assert.match(html, /function loadDashboardEvidence\(\)/);
  assert.doesNotMatch(html, /window\.addEventListener\('load', function \(\) \{\s*try \{\s*var bust/);
});

test('reduced motion is an immediate lights-out state', ()=>{
  assert.match(scene, /motion=!window\.matchMedia\('\(prefers-reduced-motion: reduce\)'\)\.matches/);
  assert.match(scene, /if\(!motion\)\{showLightsOutState\(\);drawScene\(performance\.now\(\),0\);return\}/);
  assert.match(scene, /btnText\.textContent='Lights out · Sign in'/);
});

test('lights-out trigger remains below six seconds', ()=>{
  const maximumDelay = 900 + 5 * 720 + 650 + 400;
  assert.ok(maximumDelay < 6000, `maximum trigger delay was ${maximumDelay}ms`);
  assert.match(scene, /900\+5\*720\+650\+Math\.random\(\)\*400/);
});
