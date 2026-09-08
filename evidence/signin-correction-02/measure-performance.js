const port=process.argv[2]||'43992';

async function main(){
  const targets=await fetch(`http://127.0.0.1:${port}/json/list`).then(response=>response.json());
  const target=targets.find(item=>item.type==='page'&&item.url.includes('127.0.0.1:43991'));
  if(!target)throw new Error('QA page target not found');
  const socket=new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject});
  let nextId=0;
  const pending=new Map();
  socket.onmessage=event=>{
    const message=JSON.parse(event.data);
    if(!message.id)return;
    const request=pending.get(message.id);
    if(!request)return;
    pending.delete(message.id);
    if(message.error)request.reject(new Error(message.error.message));else request.resolve(message.result);
  };
  function send(method,params={}){
    const id=++nextId;
    socket.send(JSON.stringify({id,method,params}));
    return new Promise((resolve,reject)=>pending.set(id,{resolve,reject}));
  }
  await send('Emulation.setDeviceMetricsOverride',{width:1920,height:1080,deviceScaleFactor:1,mobile:false});
  const expression=`(async()=>{
    while(!window.__lightsOutSignin)await new Promise(resolve=>setTimeout(resolve,20));
    while(window.__lightsOutSignin.getState().cssWidth!==1920||window.__lightsOutSignin.getState().cssHeight!==1080)await new Promise(resolve=>setTimeout(resolve,20));
    const deltas=[];let prior=0;
    function sample(now){if(prior)deltas.push(now-prior);prior=now;if(deltas.length<430)requestAnimationFrame(sample)}
    requestAnimationFrame(sample);window.__lightsOutSignin.run();
    await new Promise(resolve=>setTimeout(resolve,7000));
    const sorted=deltas.slice().sort((a,b)=>a-b),pick=q=>sorted[Math.min(sorted.length-1,Math.floor(sorted.length*q))];
    return {frames:deltas.length,durationMs:deltas.reduce((sum,value)=>sum+value,0),fps:1000*deltas.length/deltas.reduce((sum,value)=>sum+value,0),p50Ms:pick(.5),p95Ms:pick(.95),maxMs:sorted.at(-1),over20Ms:deltas.filter(value=>value>20).length,state:window.__lightsOutSignin.getState(),words:Array.from(document.querySelectorAll('#loginOverlay *')).map(node=>node.textContent).filter(text=>/^[1-5] LIGHTS?$/i.test(text.trim()))};
  })()`;
  const result=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});
  await send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:2,mobile:false});
  const hidpi=await send('Runtime.evaluate',{expression:`(async()=>{while(window.__lightsOutSignin.getState().dpr!==2)await new Promise(resolve=>setTimeout(resolve,20));return window.__lightsOutSignin.getState()})()`,awaitPromise:true,returnByValue:true});
  await send('Emulation.setDeviceMetricsOverride',{width:1366,height:768,deviceScaleFactor:1,mobile:false});
  const resized=await send('Runtime.evaluate',{expression:`(async()=>{while(window.__lightsOutSignin.getState().cssWidth!==1366||window.__lightsOutSignin.getState().dpr!==1)await new Promise(resolve=>setTimeout(resolve,20));return window.__lightsOutSignin.getState()})()`,awaitPromise:true,returnByValue:true});
  await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await send('Page.reload',{ignoreCache:true});
  await new Promise(resolve=>setTimeout(resolve,1000));
  const reduced=await send('Runtime.evaluate',{expression:`({state:window.__lightsOutSignin.getState(),doneSectors:document.querySelectorAll('#loginSectors .done').length,button:document.getElementById('loginButtonText').textContent})`,returnByValue:true});
  await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'no-preference'}]});
  await send('Page.reload',{ignoreCache:true});
  await new Promise(resolve=>setTimeout(resolve,1000));
  await send('Runtime.evaluate',{expression:`window.__visibilityQa=[];document.addEventListener('visibilitychange',()=>window.__visibilityQa.push({hidden:document.hidden,state:window.__lightsOutSignin.getState()}))`});
  await send('Page.setWebLifecycleState',{state:'frozen'});
  await new Promise(resolve=>setTimeout(resolve,300));
  await send('Page.setWebLifecycleState',{state:'active'});
  await new Promise(resolve=>setTimeout(resolve,300));
  const visibility=await send('Runtime.evaluate',{expression:'window.__visibilityQa',returnByValue:true});
  console.log(JSON.stringify({performance1920x1080:result.result.value,hidpi1440x900:hidpi.result.value,resized1366x768:resized.result.value,reducedMotion:reduced.result.value,visibilityPause:visibility.result.value},null,2));
  socket.close();
}

main().catch(error=>{console.error(error);process.exitCode=1});
