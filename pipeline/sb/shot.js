const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1240,height:900}});
await p.goto('file://'+process.cwd()+'/storyboard.html');await p.waitForTimeout(500);
await p.screenshot({path:'sb.png',fullPage:true});await b.close();})();
