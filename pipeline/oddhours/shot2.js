const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:900}});
await p.goto('file://'+process.cwd()+'/'+(process.argv[2]||'james')+'.html');await p.screenshot({path:(process.argv[2]||'james')+'.png',fullPage:true});await b.close();})();
