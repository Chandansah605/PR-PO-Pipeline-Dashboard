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

test('scene lifecycle renders at native DPR and stops all recurring work', ()=>{
  assert.match(scene, /DPR=window\.devicePixelRatio\|\|1/);
  assert.match(scene, /cv\.width=Math\.round\(W\*DPR\)/);
  assert.match(scene, /cv\.height=Math\.round\(H\*DPR\)/);
  assert.match(scene, /ctx\.imageSmoothingQuality='high'/);
  assert.match(scene, /matchMedia\('\(resolution: '\+DPR\+'dppx\)'\)/);
  assert.doesNotMatch(scene, /adaptivePaused|slowFrames|redrawAdaptive/);
  assert.match(scene, /document\.hidden/);
  assert.match(scene, /cancelAnimationFrame\(frameId\)/);
  assert.match(scene, /window\.clearInterval\(clockId\)/);
  assert.match(scene, /window\.stopLightsOutSignin=stop/);
  assert.match(html, /if\(window\.stopLightsOutSignin\) window\.stopLightsOutSignin\(\)/);
});

test('empty straight has no vehicle asset or rendering path', ()=>{
  assert.equal(fs.existsSync(path.join(root,'assets','car')),false);
  assert.doesNotMatch(scene,/assets\/car|car-rear|car-side|car-front|prepareCar|drawHeroVehicle|carTexture|carImage|carSource|carX/);
  assert.match(scene,/const ROADW=122/);
  assert.match(scene,/\[-46,46\]\.forEach\(x=>/);
});

test('five start-light panels fill left-to-right without track wording', ()=>{
  assert.match(scene, /for\(let n=0;n<5;n\+\+\)drawLamp\(start\+n\*step,lampY,radius,L===lap&&phase==='lights'&&n<lit\)/);
  assert.doesNotMatch(scene, /function say\(|'5 lights'|'1 light'|'Lights out','green'|'Lap complete'/);
  assert.doesNotMatch(html, /loginCallout|login-callout/);
});

test('stage titles are masked below the headline', ()=>{
  assert.match(scene,/headlineBottom=hero\?hero\.getBoundingClientRect\(\)\.bottom\+28/);
  assert.match(scene,/function stageTitleAlpha\(top\)/);
  assert.equal((new Function('top','headlineBottom',"return Math.max(0,Math.min(1,(top-headlineBottom)/42))"))(100,100),0);
  assert.equal((new Function('top','headlineBottom',"return Math.max(0,Math.min(1,(top-headlineBottom)/42))"))(142,100),1);
  assert.equal((scene.match(/globalAlpha=alpha\*stageTitleAlpha\(s1\.y\)/g)||[]).length,2);
});

test('transitions stay local to the track and never wash the frame', ()=>{
  assert.match(scene,/function drawTrackSweep\(\)/);
  assert.match(scene,/ctx\.clip\(\)/);
  assert.doesNotMatch(scene,/\bflash\b|if\(flash>0\)/);
  assert.match(scene,/gatePulse=Math\.max\(0,gatePulse-dt\*\.0045\)/);
});

test('lamp glass has distinct off, lit, core and bloom treatments', ()=>{
  assert.match(scene,/lens\.addColorStop\(0,on\?'#FFFFFF':'#28333E'\)/);
  assert.match(scene,/bloom\.addColorStop\(0,'rgba\(255,65,55,\.72\)'\)/);
  assert.match(scene,/ctx\.shadowBlur=radius\*3\.1/);
  assert.match(scene,/phase='race';lit=0;targetSpeed=9;gatePulse=1/);
});

test('sign-in button keeps one label for every sequence state', ()=>{
  assert.equal((html.match(/Sign in with Microsoft/g)||[]).length,1);
  assert.equal((scene.match(/Sign in with Microsoft/g)||[]).length,2);
  assert.doesNotMatch(scene,/Lights out · Sign in/);
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
  assert.match(scene, /btnText\.textContent='Sign in with Microsoft'/);
});

test('lights-out trigger remains below six seconds', ()=>{
  const maximumDelay = 900 + 5 * 720 + 650 + 400;
  assert.ok(maximumDelay < 6000, `maximum trigger delay was ${maximumDelay}ms`);
  assert.match(scene, /900\+5\*720\+650\+Math\.random\(\)\*400/);
});
