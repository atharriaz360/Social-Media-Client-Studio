import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='/Users/macbook/Documents/Codex/2026-10-26/wh';
const out=root+'/outputs/Client-Studio-v2/Documents';
const wb=Workbook.create();
const names=['Start','Plan','Brief','Results','Example'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const navy='#6550A6',amber='#F7F1D0',gray='#EEE9F7';
function style(s,end,title){
 s.showGridLines=false;s.getRange('A1:'+end).format.font={name:'Arial',size:11,color:'#252332'};
 s.getRange('A1:'+end).format.rowHeight=27;
 s.getRange('A1:'+end).format.verticalAlignment='center';
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};
 s.getRange('A2').format.rowHeight=36;s.tabColor=navy;
}
function header(s,range){s.getRange(range).format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:42,horizontalAlignment:'center',verticalAlignment:'center'};}
const ph=['ID','Planned date','Channel','Role','Idea','Draft caption','Asset reference','Version','Fact check','Asset rights','Approval','Approved by','Approval evidence','Approved version','Review due','Stage','Published URL','Next action'];
function action(r){return `=IF(A${r}="","",IF(COUNTIF($A$7:$A$106,A${r})>1,"Fix duplicate ID",IF(OR(C${r}="",E${r}="",F${r}="",G${r}="",B${r}="",NOT(ISNUMBER(H${r}))),"Complete draft details",IF(OR(H${r}<1,MOD(H${r},1)<>0),"Use whole version number",IF(OR(I${r}<>"Yes",J${r}<>"Yes"),"Review facts and assets",IF(OR(K${r}<>"Approved",L${r}="",M${r}="",N${r}<>H${r}),"Request approval",IF(P${r}="Published",IF(Q${r}="","Add published URL","Published"),IF(P${r}="Scheduled","Scheduled","Ready to schedule"))))))))`;}
function plan(s,isExample=false){
 style(s,'R106',isExample?'Fictional approval practice':'Content plan and approval queue');
 s.getRange('A4').values=[['Yellow: your inputs. Lavender: formulas. Filter Next action to focus your work.']];
 s.getRange('A5').values=[['One client per file. Approval applies only to the matching version.']];
 s.getRange('A6:R6').values=[ph];header(s,'A6:R6');
 s.getRange('A7:Q106').format.fill=amber;s.getRange('R7:R106').format.fill=gray;
 const widths=[14,16,18,15,32,58,30,12,15,16,22,22,38,18,16,18,38,29];
 widths.forEach((w,i)=>s.getRangeByIndexes(0,i,106,1).format.columnWidth=w);
 s.getRange('A4:R5').format.rowHeight=26;
 s.getRange('E7:G106').format.wrapText=true;s.getRange('L7:M106').format.wrapText=true;s.getRange('Q7:R106').format.wrapText=true;
 s.getRange('A7:R106').format.rowHeight=62;
 s.getRange('B7:B106').setNumberFormat('mmm d, yyyy');s.getRange('O7:O106').setNumberFormat('mmm d, yyyy');
 for(const [range,values] of [['C7:C106',['Instagram','Facebook','LinkedIn','TikTok','YouTube','Pinterest','Other']],['D7:D106',['Explain','Show','Invite']],['I7:J106',['Yes','No']],['K7:K106',['Pending','Changes requested','Approved']],['P7:P106',['Draft','In review','Scheduled','Published']]]) s.getRange(range).dataValidation={rule:{type:'list',values}};
 s.getRange('R7:R106').formulas=Array.from({length:100},(_,i)=>[action(i+7)]);
 s.getRange('R7:R106').conditionalFormats.add('containsText',{text:'Ready to schedule',format:{fill:'#DDEBE2',font:{color:'#244A35'}}});
 s.getRange('R7:R106').conditionalFormats.add('containsText',{text:'Request approval',format:{fill:'#FCE8D9',font:{color:'#7A3B1C'}}});
 s.getRange('R7:R106').conditionalFormats.add('containsText',{text:'Fix duplicate',format:{fill:'#F7DDDB',font:{color:'#852E2B'}}});
 s.tables.add('A6:R106',true,isExample?'ExamplePosts':'ClientPosts');s.freezePanes.freezeRows(6);s.freezePanes.freezeColumns(1);
 if(isExample){
 s.getRange('A7:Q9').values=[
 ['C001',new Date('2026-11-02T12:00:00Z'),'Instagram','Explain','Daily soup explainer','Ask us about today\'s soup, served 12-3. View the menu at the counter.','Client-owned soup photo',1,'','Yes','Pending','','','',new Date('2026-10-30T12:00:00Z'),'Draft',''],
 ['C002',new Date('2026-11-04T12:00:00Z'),'Instagram','Show','Behind lunch','A little look behind lunch. Ask us what is on today, served 12-3.','Client-owned preparation photo',2,'Yes','Yes','Approved','Avery (fictional)','Fictional email, Oct 26, v2',2,new Date('2026-10-30T12:00:00Z'),'In review',''],
 ['C003',new Date('2026-11-06T12:00:00Z'),'Instagram','Invite','Menu invitation','Lunch plans? Take a look at the menu at our counter. Lunch is served 12-3.','Client-owned counter photo',1,'Yes','Yes','Approved','Avery (fictional)','Fictional email, Oct 26, v1',1,new Date('2026-10-30T12:00:00Z'),'Published','']];
 }
}
plan(sheets.Plan);plan(sheets.Example,true);
const b=sheets.Brief;style(b,'D25','Client brief');b.getRange('A4').values=[['Confirm facts with the client before drafting. Leave unknown answers blank.']];
b.getRange('A6:C6').values=[['Field','Client-confirmed answer','Confirmation / source']];header(b,'A6:C6');
const fields=['Client name','Offer / service','Primary audience','Business goal','Channel','Voice rules','Approved facts','Prohibited claims','Asset location and usage permission','Call to action','Named approver','Client timezone','Brief confirmed on','Reporting period','Metric source / extraction date','Publishing tool','Revision agreement reference'];
b.getRange('A7:A23').values=fields.map(x=>[x]);b.getRange('B7:C23').format.fill=amber;b.getRange('A7:C23').format.rowHeight=58;b.getRange('A7:C23').format.wrapText=true;
b.getRange('A:A').format.columnWidth=35;b.getRange('B:B').format.columnWidth=65;b.getRange('C:C').format.columnWidth=43;
b.getRange('B19').setNumberFormat('mmm d, yyyy');
const r=sheets.Results;style(r,'L106','Post results');
r.getRange('A4').values=[['One row per post and reporting period. Do not add post reach as unique audience.']];
r.getRange('A5').values=[['Enter zero when measured as zero; leave unavailable measures blank. Rates use reach.']];
r.getRange('A6:L6').values=[['Content ID','Period / channel','Reach','Likes','Comments','Saves','Shares','Link clicks','Interactions','Interaction rate','Click rate','Source / extracted on']];header(r,'A6:L6');
r.getRange('A7:H106').format.fill=amber;r.getRange('L7:L106').format.fill=amber;r.getRange('I7:K106').format.fill=gray;
[16,29,15,13,15,13,13,16,17,20,17,48].forEach((w,i)=>r.getRangeByIndexes(0,i,106,1).format.columnWidth=w);
r.getRange('A7:L106').format.rowHeight=38;r.getRange('L7:L106').format.wrapText=true;
r.getRange('C7:H106').dataValidation={rule:{type:'whole',operator:'greaterThanOrEqual',formula1:0}};
for(let row=7;row<=106;row++){
 r.getRange(`I${row}`).formulas=[[`=IF(OR(A${row}="",COUNT(D${row}:G${row})<4),"",SUM(D${row}:G${row}))`]];
 r.getRange(`J${row}`).formulas=[[`=IF(OR(A${row}="",NOT(ISNUMBER(C${row})),C${row}<=0,NOT(ISNUMBER(I${row}))),"",I${row}/C${row})`]];
 r.getRange(`K${row}`).formulas=[[`=IF(OR(A${row}="",NOT(ISNUMBER(C${row})),C${row}<=0,NOT(ISNUMBER(H${row}))),"",H${row}/C${row})`]];
}
r.getRange('J7:K106').setNumberFormat('0.0%');r.getRange('C7:I106').setNumberFormat('#,##0');
r.getRange('A7:H7').values=[['C001','Fictional Nov / Instagram',800,26,4,12,6,10]];
r.getRange('L7').values=[['Fictional sample data, 26 Oct 2026. Replace before client use.']];
r.tables.add('A6:L106',true,'PostResults');r.freezePanes.freezeRows(6);
const s=sheets.Start;style(s,'G19','Your client studio');
s.getRange('A5:B14').values=[['Step','Action'],['1','Duplicate this file for one client. Keep the master unchanged.'],['2','Fill in Brief and confirm the missing decisions with the client.'],['3','Use Plan for your content and approval record. Start at row 7.'],['4','Read the fictional Example tab and run the practice exercises.'],['5','Enter real post data in Results. Replace the labeled fictional row.'],['Colors','Yellow is editable. Lavender holds formulas.'],['Capacity','Plan and Results have 100 prepared rows, 7 through 106.'],['Compatibility','XLSX supplied. Google Sheets import must be checked after conversion.'],['Automation','No publishing, reminders, account integrations or AI connection.']];
header(s,'A5:B5');s.getRange('A:A').format.columnWidth=20;s.getRange('B:B').format.columnWidth=100;s.getRange('B6:B14').format.wrapText=true;s.getRange('A6:B14').format.rowHeight=48;
s.getRange('D5:E5').values=[['WORK AT A GLANCE','Posts']];header(s,'D5:E5');
s.getRange('D6:D9').values=[['Ready to schedule'],['Needs client approval'],['Needs review checks'],['Published with URL']];
s.getRange('E6:E9').formulas=[['=COUNTIF(Plan!R7:R106,"Ready to schedule")'],['=COUNTIF(Plan!R7:R106,"Request approval")'],['=COUNTIF(Plan!R7:R106,"Review facts and assets")'],['=COUNTIF(Plan!R7:R106,"Published")']];
s.getRange('D:D').format.columnWidth=30;s.getRange('E:E').format.columnWidth=13;s.getRange('D6:E9').format.rowHeight=48;s.getRange('E6:E9').format.fill='#EEE9F7';s.getRange('E6:E9').format.font={name:'Arial',size:16,color:'#6550A6'};
s.getRange('A17').values=[['Studio Edition 02 / Fictional examples are training material.']];
wb.recalculate();
function get(sheet,cell){return sheets[sheet].getRange(cell).values[0][0];}
function assert(x,msg){if(!x)throw Error(msg)}
assert(get('Example','R7')==='Review facts and assets','Review gate');
assert(get('Example','R8')==='Ready to schedule','Ready gate');
assert(get('Example','R9')==='Add published URL','Published URL gate');
sheets.Example.getRange('H8').values=[[3]];assert(get('Example','R8')==='Request approval','Version mismatch');
sheets.Example.getRange('N8').values=[[3]];assert(get('Example','R8')==='Ready to schedule','New version approval');
sheets.Example.getRange('J8').values=[['']];assert(get('Example','R8')==='Review facts and assets','Approval cannot bypass rights');
sheets.Example.getRange('J8').values=[['Yes']];sheets.Example.getRange('H8:N8').values=[[2,'Yes','Yes','Approved','Avery (fictional)','Fictional email, Oct 26, v2',2]];
sheets.Example.getRange('A10').values=[['C001']];assert(get('Example','R7')==='Fix duplicate ID','Duplicate ID gate');sheets.Example.getRange('A10').clear({applyTo:'contents'});
assert(get('Results','I7')===48,'Interactions');assert(Math.abs(get('Results','J7')-0.06)<1e-9,'Rate');assert(Math.abs(get('Results','K7')-.0125)<1e-9,'Click rate');
r.getRange('F7').clear({applyTo:'contents'});assert(get('Results','I7')==='','Missing metric blank');r.getRange('F7').values=[[12]];
r.getRange('C7').values=[[0]];assert(get('Results','J7')==='','Zero reach guard');r.getRange('C7').values=[[800]];
// Last prepared row supports the same workflow and data calculation.
sheets.Plan.getRange('A106').values=[['TEST']];assert(get('Plan','R106')==='Complete draft details','Last plan row');sheets.Plan.getRange('A106').clear({applyTo:'contents'});
r.getRange('A106:H106').values=[['TEST','Test',100,0,0,0,0,0]];assert(get('Results','I106')===0,'Measured zero');assert(get('Results','J106')===0,'Zero interaction rate');r.getRange('A106:H106').clear({applyTo:'contents'});
wb.recalculate();
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:10},summary:'Formula error scan',maxChars:2000})).ndjson);
console.log((await wb.inspect({kind:'table',range:'Example!H7:R9',include:'values,formulas',tableMaxRows:3,tableMaxCols:11,maxChars:3000})).ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(out+'/Spreadsheet-Companion.xlsx');
await fs.mkdir(root+'/work/brief-kit/v2/sheet-previews',{recursive:true});
for(const [name,range] of [['Plan','A1:H10'],['Brief','A1:C10'],['Results','A1:L9'],['Example','H1:R10'],['Start','A1:E17']]){
 const blob=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(root+'/work/brief-kit/v2/sheet-previews/'+name+'.png',new Uint8Array(await blob.arrayBuffer()));
}
await fs.writeFile(root+'/work/brief-kit/workbook-checks.txt','PASS: approval prerequisites, version mismatch, duplicate IDs, missing URL, last row, interaction totals, missing metrics, zero reach and measured zero.\nNative Excel/Google Sheets not checked.\n');
console.log('Workbook exported; behavioral checks passed; five previews saved.');
