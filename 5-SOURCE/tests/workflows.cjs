const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const script=fs.readFileSync(path.join(__dirname,'../src/app.js'),'utf8');
function boot(initial={},failSave=false){
 const nodes=new Map(),events={},storage={...initial},downloads=[];
 function node(key){if(!nodes.has(key))nodes.set(key,{id:key.startsWith('#')?key.slice(1):'',innerHTML:'',textContent:'',value:'',dataset:{},files:[],open:false,classList:{add(){},remove(){},toggle(){},contains(){return false}},setAttribute(){},addEventListener(k,f){this[k]=f},showModal(){this.open=true},close(){this.open=false},click(){downloads.push(this)},reset(){for(const f of Object.values(this.elements||{})){f.value='';f.checked=false}},getAttribute(k){return this[k]}});return nodes.get(key)}
 const fields=['id','title','channel','date','role','caption','asset','cover','stage','url','facts','rights'];
 node('#post-form').elements=Object.fromEntries(fields.map(k=>[k,{value:'',checked:false}]));
 node('#approval-form').elements=Object.fromEntries(['id','person','decision','evidence'].map(k=>[k,{value:''}]));
 class FormData{constructor(form){this.form=form}*[Symbol.iterator](){for(const [k,v] of Object.entries(this.form.elements))if(!['facts','rights'].includes(k))yield[k,v.value]}}
 const sandbox={console,Date,Blob,FormData,URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},confirm:()=>true,setTimeout:()=>1,clearTimeout(){},location:{hash:''},localStorage:{getItem:k=>storage[k]??null,setItem(k,v){if(failSave)throw Error('storage full');storage[k]=v}},document:{querySelector:s=>s==='dialog[open]'?[...nodes.values()].find(n=>n.open)||null:node(s),addEventListener:(k,f)=>events[k]=f,createElement:()=>node('download')},addEventListener:(k,f)=>events[k]=f};
 vm.createContext(sandbox);vm.runInContext(script,sandbox);
 function click(dataset={},attrs=[],id=''){const b={id,dataset,classList:{contains:()=>false},hasAttribute:k=>attrs.includes(k)};events.click({target:{closest:()=>b}})}
 function fill(sel,values){for(const [k,v] of Object.entries(values))node(sel).elements[k].value=v}
 function submit(sel){node(sel).submit({preventDefault(){},target:node(sel)})}
 const saved=()=>JSON.parse(storage['brief-approved-studio-v2']);
 return{node,events,storage,sandbox,click,fill,submit,saved,downloads};
}
const a=boot();
// Calendar date -> editor -> save -> calendar render -> reload.
a.sandbox.location.hash='#calendar';a.events.hashchange();a.click({addDate:'2026-11-17'});
assert.equal(a.node('#post-form').elements.date.value,'2026-11-17');assert(a.node('#editor').open);
a.fill('#post-form',{title:'New calendar item',caption:'A clear caption',asset:'client-photo.jpg',channel:'Instagram',role:'Explain',cover:'soup',stage:'Draft'});
a.submit('#post-form');let item=a.saved().posts.find(p=>p.title==='New calendar item');assert(item);assert.equal(item.date,'2026-11-17');assert.equal(item.version,1);assert.equal(item.facts,false);assert(a.node('#main').innerHTML.includes('New calendar item'));assert(!a.node('#editor').open);
const reloaded=boot(a.storage);assert(reloaded.node('#main').innerHTML.includes('Your one next step'));
// Approval gate -> checks -> approval -> scheduling -> revision clears approval.
a.click({approve:item.id});assert(!a.node('#approval').open);
a.click({edit:item.id});a.node('#post-form').elements.facts.checked=true;a.node('#post-form').elements.rights.checked=true;a.submit('#post-form');
a.click({approve:item.id});assert(a.node('#approval').open);
a.fill('#approval-form',{decision:'Approved',person:'Client',evidence:'Email reference'});a.submit('#approval-form');item=a.saved().posts.find(p=>p.id===item.id);assert.equal(item.approvedVersion,1);
a.click({stage:'Scheduled',id:item.id});assert.equal(a.saved().posts.find(p=>p.id===item.id).stage,'Scheduled');
a.click({edit:item.id});a.fill('#post-form',{caption:'Revised caption'});a.submit('#post-form');item=a.saved().posts.find(p=>p.id===item.id);assert.equal(item.version,2);assert.equal(item.stage,'Draft');assert.equal(item.approval,'Pending');assert.equal(item.evidence,'');
a.click({stage:'Scheduled',id:item.id});assert.equal(a.saved().posts.find(p=>p.id===item.id).stage,'Draft');
// Empty/invalid drafts cannot enter storage.
const count=a.saved().posts.length;a.click({},['data-add']);a.fill('#post-form',{date:'2026-02-30',title:'Bad date',caption:'Caption',asset:'asset'});a.submit('#post-form');assert.equal(a.saved().posts.length,count);a.node('#editor').close();
// Backdrop logic must preserve clicks inside the dialog rectangle.
const dialog={tagName:'DIALOG',open:true,getBoundingClientRect:()=>({left:10,right:100,top:10,bottom:100}),close(){this.open=false}};
a.events.click({target:dialog,clientX:30,clientY:30});assert(dialog.open);a.events.click({target:dialog,clientX:0,clientY:30});assert(!dialog.open);
// Another tab blocks writes; failed storage never claims success.
a.events.storage({key:'brief-approved-studio-v2'});const before=a.storage['brief-approved-studio-v2'];a.click({stage:'Scheduled',id:'P002'});assert.equal(a.storage['brief-approved-studio-v2'],before);
const failed=boot({},true);failed.click({stage:'Scheduled',id:'P002'});assert.match(failed.node('#toast').textContent,/memory only/);
// All routes, including secondary views, render without undefined values.
for(const route of ['overview','content','calendar','approvals','brief','assets','reports','outcomes','library','pipeline','team','settings']){reloaded.sandbox.location.hash='#'+route;reloaded.events.hashchange();assert(reloaded.node('#main').innerHTML.length>100,route);assert(!reloaded.node('#main').innerHTML.includes('undefined'),route)}
console.log('PASS: code-only workflows: dated creation, save/reload, approval gates, approval, scheduling, revision reset, invalid dates, dialog boundaries, cross-tab write protection, storage failure notice and all 12 routes.');

(async()=>{
 const b=boot();b.click({},[],'clear');assert.equal(b.saved().posts.length,0);
 b.click({},[],'restore-recovery');assert.equal(b.saved().posts.length,3);
 b.click({},['data-backup']);assert.equal(b.downloads.at(-1).download,'client-studio-backup.json');
 b.click({},['data-csv']);assert.equal(b.downloads.at(-1).download,'content-plan.csv');
 const imported=b.saved();imported.client.name='<img src=x onerror=alert(1)>';imported.posts[0].title='<script>alert(1)</script>';
 await b.node('#import-file').change({target:{files:[{size:1000,text:async()=>JSON.stringify(imported)}],value:'backup.json'}});
 assert.equal(b.saved().client.name,imported.client.name);assert(!b.node('#main').innerHTML.includes('<img src=x'));assert(!b.node('#main').innerHTML.includes('<script>alert(1)</script>'));
 const beforeBad=b.storage['brief-approved-studio-v2'];
 await b.node('#import-file').change({target:{files:[{size:1000,text:async()=>'{broken'}],value:'bad.json'}});
 assert.equal(b.storage['brief-approved-studio-v2'],beforeBad);
 const damaged=boot({'brief-approved-studio-v2':'{broken'});damaged.click({stage:'Scheduled',id:'P002'});assert.equal(damaged.storage['brief-approved-studio-v2'],'{broken');
 console.log('PASS: code-only backup export, CSV export, clear/recovery, import, escaped user text, invalid-import preservation and unreadable-data write protection.');
})().catch(error=>{console.error(error);process.exitCode=1});
