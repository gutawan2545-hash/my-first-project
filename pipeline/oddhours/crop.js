const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/frame.html');
await p.screenshot({path:'crop.png',clip:{x:180,y:360,width:340,height:420}});await b.close();})();
