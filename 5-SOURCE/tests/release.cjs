const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.PW_CHROMIUM||undefined});
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true,reducedMotion:'reduce'});
 const errors=[];const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 const url='file://'+path.resolve(__dirname,'../../1-SELL-THIS/Brief-to-Approved.html');
 const shots=path.resolve(__dirname,'../test-results');fs.mkdirSync(shots,{recursive:true});
 await page.goto(url);await page.waitForTimeout(300);
 // single file: no external requests
 const html=fs.readFileSync(path.resolve(__dirname,'../../1-SELL-THIS/Brief-to-Approved.html'),'utf8');
 assert.ok(!/(src|href)="https?:\/\//.test(html)&&!/url\(https?:/.test(html),'no remote assets');
 // all routes
 const routes=['overview','content','calendar','approvals','brief','assets','reports','library','settings'];
 for(const r of routes){await page.evaluate(x=>location.hash='#'+x,r);await page.waitForTimeout(60);assert.ok(await page.locator('#nav a.active[href="#'+r+'"]').count(),r);assert.ok((await page.locator('#main').innerText()).length>40,r+' empty')}
 // Focus mode: visible recovery after reload, with workspace data unchanged.
 await page.evaluate(()=>location.hash='#overview');await page.waitForTimeout(60);
 const workspaceBeforeFocus=await page.evaluate(()=>localStorage.getItem('brief-approved-studio-v2'));
 await page.keyboard.press('f');
 assert.ok(await page.locator('.focus-notice').isVisible());
 assert.equal(await page.locator('.trio').isVisible(),false);
 await page.reload();await page.waitForTimeout(300);
 assert.ok(await page.locator('.focus-notice').isVisible());
 await page.locator('.focus-notice [data-focus]').click();
 assert.ok(await page.locator('.trio').isVisible());
 assert.ok(await page.locator('.duo').isVisible());
 assert.equal(await page.locator('.focus-notice').count(),0);
 assert.equal(await page.evaluate(()=>localStorage.getItem('brief-approved-studio-v2')),workspaceBeforeFocus);
 // escaped input
 await page.evaluate(()=>{location.hash='#settings'});await page.waitForTimeout(60);
 await page.fill('#settings-form [name=name]','<img src=x onerror=window.__x=1><script>window.__x=1</script>');await page.click('#settings-form button[type=submit]');
 await page.evaluate(()=>{location.hash='#overview'});await page.waitForTimeout(100);
 assert.equal(await page.locator('#main img[src=x], #main script').count(),0,'html injected');assert.equal(await page.evaluate(()=>window.__x),undefined);
 await page.fill('#settings-form [name=name]','Juniper Studio').catch(()=>{});
 await page.evaluate(()=>{location.hash='#settings'});await page.waitForTimeout(60);await page.fill('#settings-form [name=name]','Juniper Studio');await page.click('#settings-form button[type=submit]');
 // create, approve, revise resets approval
 await page.keyboard.press('Escape');await page.evaluate(()=>{location.hash='#approvals'});await page.waitForTimeout(80);
 await page.click('[data-approve=P003]');await page.fill('#approval-form [name=evidence]','Email 28 Oct');await page.click('#approval-form button.btn-primary');await page.waitForTimeout(80);
 assert.match(await page.locator('#main').innerText(),/Approved v1/);
 await page.click('#main [data-edit=P003] >> nth=0');await page.fill('#f-caption','A new caption');await page.click('#post-form [type=submit]');await page.waitForTimeout(80);
 const p3=await page.evaluate(()=>JSON.parse(localStorage.getItem('brief-approved-studio-v2')).posts.find(p=>p.id==='P003'));
 assert.equal(p3.version,2);assert.equal(p3.approval,'Pending');
 // backup -> clear -> restore
 await page.evaluate(()=>{location.hash='#settings'});await page.waitForTimeout(60);
 const dl=page.waitForEvent('download');await page.click('[data-backup]');const file=await dl;const backup=JSON.parse(fs.readFileSync(await file.path(),'utf8'));assert.equal(backup.posts.length,3);
 page.once('dialog',d=>d.accept());await page.click('#clear');await page.waitForTimeout(80);
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('brief-approved-studio-v2')).posts.length),0);
 page.once('dialog',d=>d.accept());await page.setInputFiles('#import-file',{name:'b.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});await page.waitForTimeout(150);
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('brief-approved-studio-v2')).posts.length),3,'restore');
 // reload keeps data; theme applied before first paint
 await page.evaluate(()=>{localStorage.setItem('brief-approved-ui-v5',JSON.stringify({theme:'dark'}))});
 await page.reload();
 assert.equal(await page.evaluate(()=>document.documentElement.dataset.theme),'dark');
 await page.waitForTimeout(250);await page.screenshot({path:path.join(shots,'desktop-dark.png'),fullPage:true});
 await page.evaluate(()=>{localStorage.setItem('brief-approved-ui-v5',JSON.stringify({theme:'light'}))});await page.reload();await page.waitForTimeout(250);
 await page.screenshot({path:path.join(shots,'desktop-light.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});await page.waitForTimeout(200);
 for(const r of routes){await page.evaluate(x=>location.hash='#'+x,r);await page.waitForTimeout(60);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'phone overflow '+r)}
 await page.evaluate(()=>location.hash='#overview');await page.waitForTimeout(100);await page.screenshot({path:path.join(shots,'phone-light.png'),fullPage:true});
 // demo build never saves
 const demo=await context.newPage();await demo.goto('file://'+path.resolve(__dirname,'../../3-HOST-DEMO/index.html'));await demo.waitForTimeout(200);
 const before=await demo.evaluate(()=>localStorage.getItem('brief-approved-studio-v2'));
 await demo.evaluate(()=>{location.hash='#settings'});await demo.waitForTimeout(60);await demo.fill('#settings-form [name=name]','Demo edit');await demo.click('#settings-form button[type=submit]');
 assert.equal(await demo.evaluate(()=>localStorage.getItem('brief-approved-studio-v2')),before,'demo saved');assert.ok(await demo.locator('#demo-bar:not([hidden])').count(),'demo bar');
 assert.deepEqual(errors,[]);
 console.log(`PASS: single file, ${routes.length} routes, escaped input, approve + revision reset, backup/clear/restore, pre-paint theme, phone width on all routes, demo never saves, no browser errors.`);
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
