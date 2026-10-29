const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const script=fs.readFileSync(path.join(__dirname,'../src/app.js'),'utf8');
const elements=new Map(),listeners={};
function el(sel){if(!elements.has(sel))elements.set(sel,{innerHTML:'',textContent:'',value:'',files:[],dataset:{},classList:{add(){},remove(){},toggle(){}},addEventListener(type,fn){this[type]=fn},click(){},showModal(){this.open=true},close(){this.open=false}});return elements.get(sel)}
const storage={};const context={document:{querySelector:el,addEventListener:(k,f)=>listeners[k]=f,createElement:()=>el('download')},location:{hash:''},localStorage:{getItem:k=>storage[k]||null,setItem:(k,v)=>storage[k]=v},addEventListener:(k,f)=>listeners[k]=f,setTimeout:()=>1,clearTimeout(){},console,Date,URL:{createObjectURL:()=>'',revokeObjectURL(){}},Blob,confirm:()=>false};
vm.createContext(context);vm.runInContext(script,context);assert(el('#main').innerHTML.includes('Your one next step'));assert(el('#nav').innerHTML.includes('aria-current'));
for(const [route,phrase] of [['content','Search content'],['calendar','November 2026'],['approvals','Needs a decision'],['brief','brief-form'],['assets','The daily soup'],['reports','Interactions'],['library','Visual field guide'],['settings','Import backup']]){context.location.hash='#'+route;listeners.hashchange();assert(el('#main').innerHTML.includes(phrase),route)}
assert(!el('#main').innerHTML.includes('undefined'));
context.location.hash='#not-real';listeners.hashchange();assert(el('#main').innerHTML.includes('Your one next step'));
console.log('PASS: initial render, nine view routes (source app.js), navigation state and unknown-route fallback using a DOM stub. This does not verify browser layout or live browser events.');

context.document.querySelector=sel=>sel==='dialog[open]'?null:el(sel);
const workspaceBeforeFocus=storage['brief-approved-studio-v2'];
listeners.keydown({key:'f',preventDefault(){}});
assert(el('#main').innerHTML.includes('Show full dashboard'));
assert(el('#main').innerHTML.includes('Focus mode is on'));
assert.equal(JSON.parse(storage['brief-approved-ui-v5']).focus,true);
listeners.keydown({key:'f',preventDefault(){}});
assert(!el('#main').innerHTML.includes('Focus mode is on'));
assert(el('#main').innerHTML.includes('Coming Up'));
assert.equal(storage['brief-approved-studio-v2'],workspaceBeforeFocus);
console.log('PASS: focus notice, exit, saved preference and unchanged workspace data (DOM stub).');

context.location.hash='#calendar';listeners.hashchange();
assert(el('#main').innerHTML.includes('data-add>'));
assert(el('#main').innerHTML.includes('data-add-date="2026-11-02"'));
assert(el('#main').innerHTML.includes('Add content on 2026-11-02'));
console.log('PASS: Calendar exposes New content and dated add controls (DOM stub).');
