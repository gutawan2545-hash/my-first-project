const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:900}});
await p.goto('file://'+process.cwd()+'/styletest.html');await p.waitForTimeout(500);
await p.screenshot({path:'st.png',fullPage:true});await b.close();})();
