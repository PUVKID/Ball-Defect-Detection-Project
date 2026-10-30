import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
original=(ROOT.parent/'1차/work/build_presentation.mjs').read_text(encoding='utf-8')
prefix=original[:original.index('// 표지와 본문')]
prefix=prefix.replace('i===1||i===12','i===1||i===20')
def block(number,target):
    start=re.search(r'\n\{\n\s*const s=make\('+str(number)+r'\);',original).start()+1
    end=original.index('\n}\n',start)+3
    result=original[start:end]
    result=result.replace(f'make({number})',f'make({target})').replace(f'chart(s,{number},',f'chart(s,{target},')
    if number==10:result=result.replace('},10);','},17);')
    return result
photo_helpers=r'''
const photoManifest=JSON.parse(await fs.readFile(path.join(ROOT,'evidence/photo_manifest.json'),'utf8'));
async function sourcePhoto(s,slideNo,file,label,x,y,w,h,labelY){
 const meta=photoManifest.photos.find(q=>q.slide===slideNo&&q.file===file);
 if(!meta)throw new Error('사진 출처 누락: '+file);
 const image=await fs.readFile(meta.local_path);
 s.images.add({blob:image.buffer.slice(image.byteOffset,image.byteOffset+image.byteLength),contentType:'image/png',alt:label+' 실제 저장 연구 사진',fit:'contain',crop:meta.native_crop,position:{left:x,top:y,width:w,height:h}});
 text(s,label,x,labelY,w,55,26,WHITE,'center');
 s.speakerNotes.text+='\n사진 출처: '+meta.container_source+'\nSHA-256: '+meta.sha256+'\n코드: save_filter_example(cell 32), 동일 원장면 선택 cell 36. 오른쪽 패널을 네이티브 자르기로 표시하며 PNG 원본 바이트를 보존했습니다.';
}
async function photoSlide(i,items,caption){
 const s=make(i);text(s,caption,78,149,1120,75,25,GRAY);
 for(let j=0;j<items.length;j++){
  const [file,label,param]=items[j];const x=76+390*j;
  await sourcePhoto(s,i,file,label,x,251,350,280,551);
  if(param)text(s,param,x,606,350,43,21,GRAY,'center');
 }
 s.speakerNotes.text+='\n조건: 동일 원장면 1001.png의 필터 효과를 보여주는 한 장의 예시입니다. 사진 자체는 검출 예측 결과가 아니며 정량 성능은 전체 500장 평가에 근거합니다.';
}
'''
photos=r'''
await photoSlide(4,[['original_example.png','Original','전처리 기준 입력'],['invert_example.png','Invert','1 − t'],['otsu_threshold_example.png','Otsu Threshold','자동 임계값 이진화']],'동일 원장면에서 비교한 변환 예시');
await photoSlide(5,[['solarize_example.png','Solarize','t > mean(t)일 때 반전'],['histogram_equalization_example.png','Histogram Equalization','전체 히스토그램 변환'],['clahe__max_example.png','CLAHE (max)','clip limit 40 / grid 16×16']],'밝기 분포와 대비를 바꾸는 변환');
await photoSlide(6,[['gamma_0_3_example.png','Gamma 0.3','정규화 밝기 t의 0.3제곱'],['gaussian_blur__max_example.png','Gaussian Blur (max)','σ=20 px / kernel 121×121'],['sobel_edges_example.png','Sobel Edges','정규화한 경계 응답의 제곱근']],'실제 코드의 고정 파라미터를 적용한 예시');
await photoSlide(7,[['emboss_example.png','Emboss','gain=4 / 응답 + 0.5'],['unsharp__max_example.png','Unsharp (max)','amount=8 / σ=2'],['original_example.png','Original','비교를 위한 원본 재제시']],'음영·선명화 변환과 원본 비교');
await photoSlide(8,[['invert_clahe_example.png','Invert+CLAHE','반전 후 지역 대비 조정'],['blur_otsu_example.png','Blur+Otsu','평활화 후 이진화'],['sobel_invert_example.png','Sobel+Invert','경계 응답 후 반전']],'A+B는 A의 출력 영상에 B를 순차적으로 적용');
await photoSlide(9,[['histeq_emboss_example.png','HistEq+Emboss','히스토그램 변환 후 Emboss'],['unsharp_sobel_example.png','Unsharp+Sobel','선명화 후 경계 응답'],['original_example.png','Original','비교를 위한 원본 재제시']],'역순·가능한 전체 조합은 평가 범위에 포함하지 않음');
'''
noise=r'''
await photoSlide(14,[['noise_std_40_example.png','Noise input','Noise std=40'],['gaussian_blur__max____noise_40_example.png','Gaussian Blur (max)','Noise std=40 후 필터 적용'],['emboss___noise_40_example.png','Emboss','Noise std=40 후 필터 적용']],'Noise std=40을 추가한 동일 원장면의 저장 예시');
await photoSlide(15,[['noise_std_80_example.png','Noise input','Noise std=80'],['gaussian_blur__max____noise_80_example.png','Gaussian Blur (max)','Noise std=80 후 필터 적용'],['emboss___noise_80_example.png','Emboss','Noise std=80 후 필터 적용']],'Noise std=80을 추가한 동일 원장면의 저장 예시');
'''
closing=r'''
{
const s=make(19);text(s,'영상 조건과 목적 지표에 따른 필터 선택',78,166,1120,67,39,BLUE);
line(s,'일반 영상: Gamma 0.3  /  잡음 조건: Gaussian Blur',280,WHITE,31);
line(s,'평가한 5개 조합은 더 우수한 구성 필터의 mAP를 넘지 못함',374,GRAY,28);
line(s,'독립 촬영 자료와 내부 그룹 분리를 통한 후속 검증',493,GRAY,28);
}
{
const s=p.slides.add();s.background.fill='#000000';
text(s,'감사합니다',76,199,1130,150,94,WHITE);
text(s,'질의응답',80,392,1130,65,35,BLUE);
text(s,'곽윤석 · 김남기',80,493,1050,45,27,GRAY);
await logo(s,80,574,260);footer(s,20);
s.speakerNotes.text=content.slides[19].spoken_script+'\n\n[출처]\n'+citations.brand;
}
'''
tail=original[original.index('await fs.writeFile(path.join(ROOT,\'evidence/chart_data.json\')'):]
tail=tail.replace('렌더 완료 ${i+1}/15','렌더 완료 ${i+1}/20')
tail=tail.replace('explicitTotalSlideCount:15','explicitTotalSlideCount:20').replace('requiredNativeChartOwnerSlides:[6,7,8,10]','requiredNativeChartOwnerSlides:[11,12,13,17]').replace('requiredNativeTableOwnerSlides:[9]','requiredNativeTableOwnerSlides:[16]').replace("'--require-native-table-slide','9'","'--require-native-table-slide','16'")
builder=prefix+photo_helpers+block(1,1)+block(2,2)+block(3,3)+photos+block(5,10)+block(6,11)+block(7,12)+block(8,13)+noise+block(9,16)+block(10,17)+block(11,18)+closing+tail
(ROOT/'work/build_presentation.mjs').write_text(builder,encoding='utf-8')
print('2차 20장 빌더 생성 완료')
