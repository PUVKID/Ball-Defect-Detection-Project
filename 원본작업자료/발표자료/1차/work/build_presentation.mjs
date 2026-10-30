import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { GlobalFonts } from '@napi-rs/canvas';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
process.env.RUNTIME_NODE_MODULES='C:/Users/PUVKID/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const SKILL='C:/Users/PUVKID/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.11052/skills/presentations';
const PY='C:/Users/PUVKID/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const {applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')));
GlobalFonts.registerFromPath('C:/Users/PUVKID/AppData/Local/Microsoft/Windows/Fonts/NanumGothicBold.ttf');
const content=JSON.parse(await fs.readFile(path.join(ROOT,'work/content.json'),'utf8'));
const data=JSON.parse(await fs.readFile(path.join(ROOT,'work/data.json'),'utf8'));
const FONT='NanumGothic',BLUE='#0A84FF',WHITE='#FFFFFF',GRAY='#BDBDC2';
const p=Presentation.create({slideSize:{width:1280,height:720}});
p.theme.defaultFont=FONT;
const citations={paper:'출처: 추계학술대회 논문 3차.hwp 및 results_summary.json, sweep_results.json, ms_run_results.csv. 조건별 재학습, 단일 시드 또는 표시한 세 시드 결과.',brand:'경기대학교 공식 로고: https://www.kyonggi.ac.kr/www/contents.do?key=5093'};
const chartEvidence=[];
const precisionEvidence=[];
function chartPayload(values){return values.map(raw=>{const shown=Number(raw.toPrecision(15));if(Math.abs(raw-shown)>1e-12||raw.toFixed(1)!==shown.toFixed(1)||raw.toFixed(2)!==shown.toFixed(2))throw new Error('원자료 대비 차트 정밀도·표시 검증 실패');precisionEvidence.push({raw,workbook:shown,absolute_error:Math.abs(raw-shown)});return shown;});}
function text(s,value,x,y,w,h,size=28,color=WHITE,align='left'){
 const q=s.shapes.add({geometry:'textbox',name:value.slice(0,32),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 q.text=value;q.text.style={typeface:FONT,fontSize:size,bold:true,color,alignment:align,verticalAlignment:'top',insets:0,wrap:'square',autoFit:'none'};return q;
}
function footer(s,i){text(s,'2026 한국정보기술학회 추계 종합학술대회',76,673,1000,24,17,GRAY);text(s,String(i).padStart(2,'0'),1170,673,38,24,17,GRAY,'right');}
function make(i){const s=p.slides.add();s.background.fill='#000000';if(i!==1){text(s,content.slides[i-1].title,76,54,1140,72,44);footer(s,i);}s.speakerNotes.text=content.slides[i-1].spoken_script+'\n\n[출처 및 조건]\n'+citations.paper+(i===1||i===12?'\n'+citations.brand:'');return s;}
function line(s,v,y,color=GRAY,size=29){text(s,v,78,y,1120,72,size,color);}
function chart(s,slideNo,names,series,pos,options={}){
 const c=s.charts.add('bar',{position:pos,categories:names,series:series.map((q,i)=>({name:q.name,values:chartPayload(q.values),fill:q.color??[BLUE,'#FFFFFF','#6B6B73'][i],valuesFormatCode:'0.00'})),barOptions:{direction:options.horizontal?'bar':'column',grouping:'clustered',gapWidth:options.gap??55},hasLegend:series.length>1,legend:{position:'bottom',overlay:false,textStyle:{fontSize:options.legendSize??19,bold:true,fill:WHITE}},chartFill:'none',plotAreaFill:'none',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0},xAxis:{visible:true,min:0,max:100,numberFormatCode:'0',textStyle:{fontSize:options.categorySize??21,bold:true,fill:WHITE},line:{fill:'#555555',width:1},majorGridlines:null},yAxis:{visible:true,min:0,max:100,majorUnit:20,numberFormatCode:'0',textStyle:{fontSize:20,bold:true,fill:WHITE},line:{fill:'none',width:0},majorGridlines:{fill:'#333333',width:1}},dataLabels:{showValue:options.labels!==false,position:'outEnd',numberFormatCode:'0.00',textStyle:{fontSize:options.labelSize??21,bold:true,fill:WHITE}}});
 applyPresentationChartFont(c,{fontFamily:FONT});chartEvidence.push({slide:slideNo,categories:names,series:series.map(x=>({name:x.name,values:chartPayload(x.values)}))});return c;
}
async function logo(s,x,y,w){const image=await fs.readFile(path.join(ROOT,'work/brand/kyonggi_signature.png'));s.shapes.add({geometry:'rect',name:'공식 마크 흰색 바탕',position:{left:x-8,top:y-5,width:w+16,height:w*168/603+10},fill:'#FFFFFF',line:{fill:'none',width:0}});s.images.add({blob:image.buffer.slice(image.byteOffset,image.byteOffset+image.byteLength),contentType:'image/png',alt:'경기대학교 공식 마크',fit:'contain',position:{left:x,top:y,width:w,height:w*168/603}});}

// 표지와 본문은 사용자가 제공한 검정·파란색·좌측 정렬 디자인을 따릅니다.
{
 const s=make(1);text(s,'2026 FALL CONFERENCE',78,75,900,26,19,BLUE);
 text(s,'YOLOv8n 기반 볼 검출을 위한\n단일 및 복합 전처리 필터의 성능 비교',76,161,1136,150,47);
 text(s,'Performance Comparison of Single and Combined Preprocessing Filters\nfor YOLOv8n-Based Ball Detection',78,334,1090,68,23,GRAY);
 text(s,'곽윤석 · 김남기 (교신저자)',78,470,900,42,28);
 text(s,'경기대학교 컴퓨터과학과',78,523,850,32,23,GRAY);
 await logo(s,78,592,235);
}
{
const s=make(2);text(s,'어떤 현장 영상이 들어올지 모르는 상황',78,170,1120,60,37,BLUE);
line(s,'밝기·대비·잡음과 경계 표현의 변화',263);
line(s,'전처리 후에도 볼 검출 성능이 유지되는가?',351,WHITE,34);
line(s,'어떤 단일 필터와 순차 조합이 유리한가?',433,WHITE,34);
text(s,'비교 범위: 일반 영상과 합성 가우시안 잡음',78,575,1110,40,24,GRAY);
}
{
const s=make(3);text(s,'500장',78,174,500,100,78,BLUE);text(s,'368개 유사 영상 그룹',78,294,580,52,34);
text(s,'2,944 × 2,352 px 회색조 영상',80,365,570,45,25,GRAY);
text(s,'외부 평가: 그룹 분리 5겹 교차검증\n폴드별 외부 평가 99–101장',78,444,590,92,27,WHITE);
text(s,'내부 학습·검증:\n유사 그룹 9–20개 중복',78,558,590,79,25,GRAY);
const sample=await fs.readFile('C:/Users/PUVKID/Desktop/2026/추계학술대회/DataSet/images/train/1001.png');s.images.add({blob:sample.buffer.slice(sample.byteOffset,sample.byteOffset+sample.byteLength),contentType:'image/png',alt:'실험 자료의 실제 입력 영상 1001.png',fit:'contain',position:{left:715,top:186,width:480,height:384}});text(s,'실제 입력 영상 예시',715,590,480,40,24,GRAY,'center');s.speakerNotes.text+='\n입력 영상 출처: DataSet/images/train/1001.png, 원본 밝기·비율 유지. 예측 결과가 아닌 원본 입력 영상.';
}
{
const s=make(4);text(s,'단일 필터 10종',78,161,550,49,33,BLUE);text(s,'순차 조합 5종',690,161,500,49,33,BLUE);
text(s,'Invert\nOtsu Threshold\nSolarize\nHistogram Equalization\nCLAHE (max)\nGamma 0.3\nGaussian Blur (max)\nSobel Edges\nEmboss\nUnsharp (max)',78,228,560,400,28,WHITE);
text(s,'Invert+CLAHE\nBlur+Otsu\nSobel+Invert\nHistEq+Emboss\nUnsharp+Sobel',690,237,500,280,31,WHITE);
text(s,'A+B: A를 적용한 결과에 B를 순차 적용\n역순·전체 조합 및 최적 파라미터 탐색 제외',690,546,510,83,22,GRAY);
}
{
const s=make(5);text(s,'조건별 YOLOv8n 재학습',78,161,1120,55,36,BLUE);line(s,'최대 30 epochs     imgsz 1280     batch 8     patience 15',242,GRAY,27);
text(s,'주 지표  mAP50-95',78,344,530,52,33);text(s,'보조 지표  엄격 검출 정확도',671,344,535,52,33);
text(s,'객체의 경계 상자 겹침 기반\n외부 5개 폴드 평균\nconfidence 0.001 / NMS IoU 0.7',78,420,540,153,27,GRAY);
text(s,'누락·추가 검출 없는 영상의 비율\n중심 거리 기반 일대일 대응\nconfidence 0.25 / NMS IoU 0.5',671,420,540,153,27,GRAY);
}
{
const s=make(6);text(s,'mAP50-95 (%)  /  Clean  /  Seed 42',78,133,1110,34,23,GRAY);
const names=['Original','Invert','Otsu Threshold','Solarize','Histogram Eq.','CLAHE (max)','Gamma 0.3','Gaussian Blur','Sobel Edges','Emboss','Unsharp (max)'];
chart(s,6,names,[{name:'mAP50-95',values:data.single.map(x=>x.map50_95)}],{left:62,top:182,width:1130,height:405},{horizontal:true,categorySize:20,labelSize:20,gap:35});
text(s,'Gamma 0.3 96.70%     Original 96.53%     차이 +0.17%p',78,603,1130,40,28,BLUE);
}
{
const s=make(7);text(s,'mAP50-95 (%)  /  Clean  /  Seed 42',78,133,1110,34,23,GRAY);
const better=['Original','CLAHE (max)','Gaussian Blur (max)','Sobel Edges','Histogram Equalization','Sobel Edges'].map(n=>data.single.find(x=>x.name===n).map50_95);
chart(s,7,['Original','Invert+\nCLAHE','Blur+\nOtsu','Sobel+\nInvert','HistEq+\nEmboss','Unsharp+\nSobel'],[{name:'Combination / baseline',values:data.combo.map(x=>x.map50_95)},{name:'Better component',values:better,color:'#85858C'}],{left:75,top:190,width:1135,height:381},{categorySize:21,labelSize:20,gap:55});
text(s,'5개 조합 모두 더 우수한 구성 필터의 mAP를 넘지 못함',78,608,1120,40,28,BLUE);
}
{
const s=make(8);text(s,'Clean / Seed 42',78,133,1110,34,23,GRAY);
const selected=['Original','Gamma 0.3','CLAHE (max)','Invert+CLAHE'].map(n=>[...data.single,...data.combo].find(x=>x.name===n));
chart(s,8,['Original','Gamma 0.3','CLAHE (max)','Invert+CLAHE'],[{name:'mAP50-95 (%)',values:selected.map(x=>x.map50_95)},{name:'Strict detection accuracy (%)',values:selected.map(x=>x.strict_acc),color:'#FFFFFF'}],{left:75,top:197,width:1135,height:375},{categorySize:23,labelSize:22,gap:70});
text(s,'대응 기준과 추론 임계값이 달라 지표별 해석이 필요',78,608,1120,40,28,BLUE);
}
{
const s=make(9);text(s,'mAP50-95 (%)  /  Seed 42',78,133,1110,34,23,GRAY);
const names=['Original','Invert','Otsu Threshold','Solarize','Histogram Equalization','CLAHE (max)','Gamma 0.3','Gaussian Blur (max)','Sobel Edges','Emboss','Unsharp (max)'];
const vals=[['Filter','Clean','Noise std=40','Noise std=80'],...names.map((n,i)=>[n,...data.noise[i].map(x=>x.toFixed(1))])];
const t=s.tables.add({rows:12,columns:4,left:78,top:185,width:1125,height:408,columnWidths:[465,220,220,220],values:vals});
t.borders.assign({fill:'#000000',width:2});
t.cells.block({row:0,column:0,rowCount:12,columnCount:4}).assign({margins:{top:0,bottom:0,left:5,right:5}});
for(let r=0;r<12;r++){t.rows[r].height=34;for(let c=0;c<4;c++){const ce=t.getCell(r,c);ce.text.style={typeface:FONT,fontSize:22,bold:true,color:WHITE,alignment:c?'center':'left',verticalAlignment:'middle',insets:3};ce.fill='#000000';if(r&&c){const v=data.noise[r-1][c-1]/100;ce.fill=`#${[Math.round(10+0*v),Math.round(23+v*92),Math.round(48+v*150)].map(x=>x.toString(16).padStart(2,'0')).join('')}`;}}}
text(s,'Gaussian Blur: 잡음 조건 최고     Emboss: 잡음에서 큰 성능 저하',78,627,1130,39,25,BLUE);
}
{
const s=make(10);text(s,'반복: Seed 42, 43, 44  /  평균 ± 표본 표준편차',78,133,1120,34,23,GRAY);
const keys=Object.keys(data.repeat);const nk=keys.find(x=>x.includes('80')&&x.endsWith('/Original')).split('/')[0];
function repeatChart(cond,metric,names,pos,slideNo){
const c=s.charts.add('line',{position:pos,categories:['Seed 42','Seed 43','Seed 44'],series:names.map((n,i)=>({name:n,values:chartPayload(data.repeat[cond+'/'+n].map(x=>x[metric])),smooth:false,line:{fill:i?'#FFFFFF':BLUE,width:3},marker:{symbol:'circle',size:9,fill:i?'#FFFFFF':BLUE},valuesFormatCode:'0.00'})),hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:20,bold:true,fill:WHITE}},chartFill:'none',plotAreaFill:'none',xAxis:{textStyle:{fontSize:20,fill:WHITE,bold:true},line:{fill:'#555555'}},yAxis:{min:metric==='strict_acc'?90:78,max:metric==='strict_acc'?100:85,majorUnit:metric==='strict_acc'?2:1,numberFormatCode:'0',textStyle:{fontSize:19,bold:true,fill:WHITE},majorGridlines:{fill:'#333333',width:1}},dataLabels:{showValue:false}});applyPresentationChartFont(c,{fontFamily:FONT});chartEvidence.push({slide:slideNo,categories:['Seed 42','Seed 43','Seed 44'],series:names.map(n=>({name:n,values:chartPayload(data.repeat[cond+'/'+n].map(x=>x[metric]))}))});}
text(s,'Clean / Strict detection accuracy (%)',78,191,550,41,23);text(s,'Noise std=80 / mAP50-95 (%)',691,191,520,41,23);
repeatChart('normal','strict_acc',['Original','Invert+CLAHE'],{left:72,top:239,width:538,height:302},10);
repeatChart(nk,'map50_95',['Original','Gaussian Blur (max)'],{left:684,top:239,width:535,height:302},10);
text(s,'Original 95.40 ± 0.53\nInvert+CLAHE 95.47 ± 2.27',78,558,550,71,25,GRAY);
text(s,'Original 79.60 ± 0.26\nGaussian Blur 82.86 ± 0.08',691,558,525,71,25,BLUE);
}
{
const s=make(11);text(s,'조건별 재학습의 비교 결과',78,167,1120,61,36,BLUE);
line(s,'고정 모델의 미지 촬영 조건 적응성은 별도 검증 필요',273,WHITE,31);
line(s,'내부 학습·검증 간 유사 그룹 중복 9–20개',365,GRAY,29);
line(s,'복합 필터의 잡음 평가와 전체 후보 반복 실험 필요',454,GRAY,29);
line(s,'후속 검증: 내부 그룹 분리와 독립 촬영 로트',558,WHITE,31);
}
{
const s=make(12);text(s,'영상 조건과 목적 지표에 따른 필터 선택',78,166,1120,67,39,BLUE);
line(s,'일반 영상: Gamma 0.3  /  잡음 조건: Gaussian Blur',280,WHITE,31);
line(s,'평가한 5개 조합은 구성 필터의 mAP를 넘지 못함',370,GRAY,29);
text(s,'경청해 주셔서 감사합니다',78,512,950,60,39);
await logo(s,78,596,200);
}
{
const s=make(13);const left=['CLAHE (max)   clip limit 40, grid 16×16','Gamma 0.3   γ=0.3','Gaussian Blur (max)   σ=20 px, kernel 121×121','Emboss   gain=4','Unsharp (max)   amount=8, σ=2'];left.forEach((x,i)=>line(s,x,165+i*77,i===2?BLUE:WHITE,28));
text(s,'고정 파라미터 비교이며 최적 파라미터 탐색 결과는 아님',78,593,1120,42,25,GRAY);
}
{
const s=make(14);text(s,'mAP50-95',78,167,550,49,34,BLUE);text(s,'엄격 검출 정확도',690,167,510,49,34,BLUE);
text(s,'IoU 0.50–0.95의 AP 평균\n경계 상자 겹침 평가\nconfidence 0.001 / NMS IoU 0.7',78,243,545,157,28,WHITE);
text(s,'누락·추가 검출 모두 없는 영상\n중심점 거리 순 일대일 대응\nconfidence 0.25 / NMS IoU 0.5',690,243,530,157,28,WHITE);
text(s,'허용 중심 거리 ≤ 주석 상자의 긴 변 × 0.5',78,448,1120,42,28,GRAY);
text(s,'98.0%는 단일 시드의 보조 지표 결과이며 반복 우월성 근거는 제한적',78,549,1120,75,28,GRAY);
}
{
const s=make(15);text(s,'[1] Jocher, Chaurasia, Qiu. Ultralytics YOLOv8. 2023.\n\n[2] Zuiderveld. Contrast Limited Adaptive Histogram Equalization.\n      Graphics Gems IV, pp. 474–485, 1994.\n\n[3] Riba et al. Kornia: an Open Source Differentiable Computer Vision\n      Library for PyTorch. arXiv:1910.02190, 2019.',78,173,1128,320,27,WHITE);
text(s,'실험 자료: 제출 논문 및 저장 실험 결과\n기관 마크: 경기대학교 공식 홈페이지',78,542,1120,77,25,GRAY);
s.speakerNotes.text+='\n공식 문헌: https://docs.ultralytics.com/models/yolov8/\nhttps://doi.org/10.1016/B978-0-12-336156-1.50061-6\nhttps://arxiv.org/abs/1910.02190\n'+citations.brand;
}
await fs.writeFile(path.join(ROOT,'evidence/chart_data.json'),JSON.stringify(chartEvidence,null,2));
await fs.writeFile(path.join(ROOT,'evidence/chart_precision.json'),JSON.stringify({precision:'15 significant digits for Excel workbook',source_precision:'원정밀도 JSON과 data.json 보존',max_absolute_error:Math.max(...precisionEvidence.map(x=>x.absolute_error)),one_and_two_decimal_displays_identical:true,values:precisionEvidence},null,2));
const renderDir=path.join(ROOT,'work/render');await fs.mkdir(renderDir,{recursive:true});
for(const [i,s] of p.slides.items.entries()){
 const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 const layout=await s.export({format:'layout'});await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.layout.json`),await layout.text());
 console.log(`렌더 완료 ${i+1}/15`);
}
const candidate=path.join(ROOT,'work/candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
const finalPath=path.join(ROOT,'결과/추계학술대회_10분발표.pptx');
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','9'],explicitTotalSlideCount:15,requiredNativeChartOwnerSlides:[6,7,8,10],requiredNativeTableOwnerSlides:[9],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'user_request',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(ROOT,'evidence/finalizer.validation.json')});
await fs.mkdir(path.join(ROOT,'결과/글꼴'),{recursive:true});
await fs.copyFile('C:/Users/PUVKID/AppData/Local/Microsoft/Windows/Fonts/NanumGothicBold.ttf',path.join(ROOT,'결과/글꼴/NanumGothicBold.ttf'));
await fs.copyFile('C:/Users/PUVKID/Documents/Codex/2026-10-13/x20/work/NanumGothic-LICENSE.txt',path.join(ROOT,'결과/글꼴/NanumGothic-LICENSE.txt'));
console.log(JSON.stringify(result));
