const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const base=path.resolve(__dirname,'../..'),source=fs.readFileSync(path.join(base,'5-SOURCE/src/app.js'),'utf8').replaceAll('__VERSION__','4.0');
for(const [name,demo] of [['1-SELL-THIS/Brief-to-Approved.html',false],['2-HOST-ONLINE/index.html',false],['3-HOST-DEMO/index.html',true]]){
 const html=fs.readFileSync(path.join(base,name),'utf8');
 assert(html.includes(source.replaceAll("'__DEMO__'",demo?"'1'":"'0'")),name+' stale source');
 assert(!/(?:src|href)=["']https?:\/\//i.test(html),name+' remote dependency');
 assert(!/url\(["']?https?:\/\//i.test(html),name+' remote CSS dependency');
 for(const match of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi))new vm.Script(match[1],{filename:name});
 assert(html.includes('data-add-date='));assert(html.includes('Show full dashboard'));
}
console.log('PASS: three built apps match current source, inline scripts parse, offline asset checks, Calendar controls and Focus recovery present.');
