import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PREVIOUS=ROOT.parent/'2차'

# 과거 차수는 입력으로만 읽고, 새 차수의 작업 경로를 명시적으로 갱신합니다.
for filename in ['photo_manifest.json','content_sources.json']:
    document=json.loads((PREVIOUS/'evidence'/filename).read_text(encoding='utf-8'))
    def relocate(value):
        if isinstance(value,str):return value.replace(str(PREVIOUS),str(ROOT)).replace(PREVIOUS.as_posix(),ROOT.as_posix())
        if isinstance(value,list):return [relocate(v) for v in value]
        if isinstance(value,dict):return {k:relocate(v) for k,v in value.items()}
        return value
    (ROOT/'evidence'/filename).write_text(json.dumps(relocate(document),ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copyfile(PREVIOUS/'결과/10분_발표대본.txt',ROOT/'결과/10분_발표대본.txt')
out=ROOT/'결과/사용이미지'
out.mkdir(parents=True,exist_ok=True)
photos=json.loads((ROOT/'evidence/photo_manifest.json').read_text(encoding='utf-8'))
for name in {x['file'] for x in photos['photos']}:shutil.copyfile(ROOT/'work/source_photos'/name,out/name)
(out/'이미지_출처.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2),encoding='utf-8')
preserved=json.loads((ROOT/'evidence/preserved_inputs.json').read_text(encoding='utf-8'))
for item in preserved['files']:
    if str(PREVIOUS/'work') in item['path']:
        item['path']=item['path'].replace(str(PREVIOUS/'work'),str(ROOT/'work'))
for rel in ['결과/추계학술대회_10분발표.pptx','결과/10분_발표대본.txt']:
    path=PREVIOUS/rel
    if not any(x['path']==str(path) for x in preserved['files']):
        preserved['files'].append({'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'purpose':'이전 차수 납품본 보존 확인용 읽기 전용 입력'})
(ROOT/'evidence/preserved_inputs.json').write_text(json.dumps(preserved,ensure_ascii=False,indent=2),encoding='utf-8')

source=(PREVIOUS/'work/build_presentation.mjs').read_text(encoding='utf-8')
source=source.replace("const FONT='NanumGothic',BLUE='#0A84FF',WHITE='#FFFFFF',GRAY='#BDBDC2';", "const FONT='NanumGothic',BLUE='#3B92FF',CYAN='#65D9F3',WHITE='#F7FAFF',GRAY='#AAB8CC',BG='#080D15';")
source=source.replace("s.background.fill='#000000'", "s.background.fill=BG")
source=source.replace("t.borders.assign({fill:'#000000'", "t.borders.assign({fill:BG")
source=source.replace("ce.fill='#000000'", "ce.fill=BG")
source=source.replace("fill:'#333333'", "fill:'#283545'").replace("fill:'#555555'", "fill:'#52647D'")

# 공통 좌측 기준선과 본문 서식을 모든 슬라이드에서 동일하게 유지합니다.
source=source.replace(" const q=s.shapes.add({", " if([76,78,80].includes(x))x=64;\n const q=s.shapes.add({",1)
old_footer="function footer(s,i){text(s,'2026 한국정보기술학회 추계 종합학술대회',76,673,1000,24,17,GRAY);text(s,String(i).padStart(2,'0'),1170,673,38,24,17,GRAY,'right');}"
new_footer="function footer(s,i){text(s,'경기대학교 컴퓨터과학과',64,684,1000,22,14,GRAY);text(s,String(i).padStart(2,'0'),1178,681,38,25,16,GRAY,'right');}"
assert old_footer in source
source=source.replace(old_footer,new_footer)
old_make="function make(i){const s=p.slides.add();s.background.fill=BG;if(i!==1){text(s,content.slides[i-1].title,76,54,1140,72,44);footer(s,i);}s.speakerNotes.text=content.slides[i-1].spoken_script+'\\n\\n[출처 및 조건]\\n'+citations.paper+(i===1||i===20?'\\n'+citations.brand:'');return s;}"
new_make="function make(i){const s=p.slides.add();s.background.fill=BG;if(i!==1){const section=i<=3?'연구 배경':i<=9?'전처리 설계':i<=17?'실험과 성능 비교':'결론과 후속 연구';text(s,section,64,33,1152,25,16,CYAN);text(s,content.slides[i-1].title,64,77,1152,72,46);footer(s,i);}s.speakerNotes.text=content.slides[i-1].spoken_script+'\\n\\n[출처 및 조건]\\n'+citations.paper+(i===1||i===20?'\\n'+citations.brand:'');return s;}"
assert old_make in source
source=source.replace(old_make,new_make)
source=source.replace("function line(s,v,y,color=GRAY,size=29){text(s,v,78,y,1120,72,size,color);}","function line(s,v,y,color=GRAY,size=29){text(s,v,64,y,1152,72,size,color);}")

# 사진은 원본 비율과 네이티브 자르기를 유지하고, 라벨·설명만 정렬합니다.
source=source.replace("text(s,label,x,labelY,w,55,26,WHITE,'center');", "text(s,label,x,labelY,w,52,25,WHITE,'left');")
source=source.replace("text(s,caption,78,149,1120,75,25,GRAY)","text(s,caption,64,166,1152,42,24,GRAY)")
source=source.replace("const x=76+390*j;", "const x=64+396*j;")
source=source.replace("file,label,x,251,350,280,551", "file,label,x,238,360,288,549")
source=source.replace("text(s,param,x,606,350,43,21,GRAY,'center')", "text(s,param,x,598,360,46,20,GRAY,'left')")

# 차트의 색상과 보조 축 대비를 같은 계열로 통일합니다. 수치는 변경하지 않습니다.
source=source.replace("[BLUE,'#FFFFFF','#6B6B73']", "[BLUE,CYAN,'#7D91AD']")
source=source.replace("fill:q.color??[BLUE,CYAN,'#7D91AD'][i],valuesFormatCode", "fill:q.color??[BLUE,CYAN,'#7D91AD'][i],points:slideNo===11?names.map((name,idx)=>({idx,fill:name==='Original'?'#D8E3F3':name==='Gamma 0.3'?CYAN:BLUE})):undefined,valuesFormatCode")
source=source.replace("color:'#85858C'", "color:'#7D91AD'").replace("color:'#FFFFFF'", "color:CYAN")
source=source.replace("fill:i?'#FFFFFF':BLUE", "fill:i?CYAN:BLUE")
source=source.replace("width:3},marker", "width:3.5},marker")
source=source.replace("',78,133,1110,34,23,GRAY)","',64,157,1152,34,21,GRAY)")
source=source.replace("',78,133,1120,34,23,GRAY)","',64,157,1152,34,21,GRAY)")
source=source.replace("{left:62,top:182,width:1130,height:405}","{left:50,top:206,width:1170,height:385}")
source=source.replace("{left:75,top:190,width:1135,height:381}","{left:64,top:207,width:1152,height:375}")
source=source.replace("{left:75,top:197,width:1135,height:375}","{left:64,top:207,width:1152,height:375}")
source=source.replace("',78,603,1130,40,28,BLUE)","',64,618,1152,42,27,CYAN)")
source=source.replace("',78,608,1120,40,28,BLUE)","',64,618,1152,42,27,CYAN)")
source=source.replace("',78,627,1130,39,25,BLUE)","',64,633,1152,37,24,CYAN)")
source=source.replace("left:78,top:185,width:1125,height:408,columnWidths:[465,220,220,220]", "left:64,top:198,width:1152,height:408,columnWidths:[456,232,232,232]")
source=source.replace("Math.round(10+0*v),Math.round(23+v*92),Math.round(48+v*150)","Math.round(8+v*8),Math.round(20+v*95),Math.round(40+v*147)")

# 표지와 마지막 장의 여백을 넓히고 로고는 공식 투명 자산으로만 넣습니다.
source=source.replace("text(s,'2026 FALL CONFERENCE',78,75,900,26,19,BLUE)","text(s,'2026 FALL CONFERENCE',64,64,1090,30,20,CYAN)")
source=source.replace("',76,161,1136,150,47)","',64,172,1152,153,50)")
source=source.replace("',78,334,1090,68,23,GRAY)","',64,354,1120,68,22,GRAY)")
source=source.replace("',78,470,900,42,28)","',64,499,900,42,27)")
source=source.replace("',78,523,850,32,23,GRAY)","',64,548,850,32,22,GRAY)")
source=source.replace("await logo(s,78,592,235)","await logo(s,934,548,282)")
source=source.replace("text(s,'감사합니다',76,199,1130,150,94,WHITE)","text(s,'감사합니다',64,192,1152,156,100,WHITE)")
source=source.replace("text(s,'질의응답',80,392,1130,65,35,BLUE)","text(s,'질의응답',64,389,1152,65,34,CYAN)")
source=source.replace("text(s,'곽윤석 · 김남기',80,493,1050,45,27,GRAY)","text(s,'곽윤석 · 김남기',64,540,850,45,27,GRAY)")
source=source.replace("await logo(s,80,574,260)","await logo(s,934,548,282)")
start=source.index('async function logo(')
end=source.index('\n',start)
source=source[:start]+"async function logo(s,x,y,w){const meta=JSON.parse(await fs.readFile(path.join(ROOT,'evidence/logo_asset.json'),'utf8'));const image=await fs.readFile(path.join(ROOT,meta.local_path));s.images.add({blob:image.buffer.slice(image.byteOffset,image.byteOffset+image.byteLength),contentType:'image/png',alt:'경기대학교 공식 투명 마크',fit:'contain',position:{left:x,top:y,width:w,height:w*meta.height/meta.width}});}"+source[end:]
source=source.replace("console.log(JSON.stringify(result));",r'''const logoOutput=path.join(ROOT,'결과/학교마크');await fs.mkdir(logoOutput,{recursive:true});
const logoMeta=JSON.parse(await fs.readFile(path.join(ROOT,'evidence/logo_asset.json'),'utf8'));
await fs.copyFile(path.join(ROOT,logoMeta.local_path),path.join(logoOutput,'경기대학교_투명마크.png'));
await fs.copyFile(path.join(ROOT,'work/brand/kyonggi_signature_white.svg'),path.join(logoOutput,'경기대학교_투명마크.svg'));
await fs.copyFile(path.join(ROOT,'work/brand/official_1947/logo_1947_01.ai'),path.join(logoOutput,'경기대학교_공식원본.ai'));
await fs.copyFile(path.join(ROOT,'work/brand/kyonggi_signature_official_vector.svg'),path.join(logoOutput,'경기대학교_공식원본.svg'));
await fs.writeFile(path.join(logoOutput,'마크_출처.json'),JSON.stringify(logoMeta,null,2),'utf8');
console.log(JSON.stringify(result));''')

# 모든 차수의 검사 및 납품 경로는 새 프로젝트를 기준으로 계산합니다.
(ROOT/'work/build_presentation.mjs').write_text(source,encoding='utf-8')
record={'background':'#080D15','main_accent':'#3B92FF','secondary_accent':'#65D9F3','font':'NanumGothic Bold','content_sha256':hashlib.sha256((ROOT/'work/content.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256((ROOT/'결과/10분_발표대본.txt').read_bytes()).hexdigest(),'previous_script_identical':(ROOT/'결과/10분_발표대본.txt').read_bytes()==(PREVIOUS/'결과/10분_발표대본.txt').read_bytes()}
(ROOT/'evidence/design_changes.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('3차 디자인 빌더와 작업 경로 갱신 완료')
