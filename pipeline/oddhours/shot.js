const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:1});
await p.goto('file://'+process.cwd()+'/frame.html');
await p.locator('svg').screenshot({path:'full.png'});
await p.setViewportSize({width:540,height:960});
await p.locator('svg').evaluate(s=>{s.setAttribute('viewBox','80 220 380 200');s.parentElement.style.aspectRatio='19/10';s.parentElement.style.width='1140px'});
await p.setViewportSize({width:1200,height:700});
await p.locator('svg').screenshot({path:'faces.png'});
await b.close();})();
