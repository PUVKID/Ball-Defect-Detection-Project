import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
previous=json.loads((ROOT.parent/'1차/work/content.json').read_text(encoding='utf-8'))
old=[x['spoken_script'] for x in previous['slides']]
titles=['YOLOv8n 기반 볼 검출을 위한\n단일 및 복합 전처리 필터의 성능 비교','현장 영상의 변화와 연구 질문','데이터와 그룹 기반 평가','단일 필터 영상 1: 반전과 이진화','단일 필터 영상 2: 밝기와 대비','단일 필터 영상 3: 평활화와 경계','단일 필터 영상 4: 음영과 선명화','순차 조합 영상 1','순차 조합 영상 2','조건별 학습과 두 평가 지표','일반 영상의 단일 필터 성능','복합 필터와 구성 필터 비교','평가 지표에 따른 순위 차이','가우시안 잡음 조건의 실제 영상','잡음 조건에 따른 성능 변화','세 시드 반복 평가','해석 범위와 후속 검증','결론','감사합니다']
durations=[25,30,45,25,25,25,20,25,20,50,55,50,35,30,50,40,30,15,5]
scripts=[
'안녕하십니까. 경기대학교 컴퓨터과학과 곽윤석입니다. YOLOv8n 기반 볼 검출을 위한 단일 및 복합 전처리 필터의 성능 비교를 발표하겠습니다. 현장에서 영상 조건이 달라질 때 필터 적용 후에도 성능이 유지되는지, 어떤 필터와 조합이 유리한지를 실제 영상과 정량 결과로 설명하겠습니다.',
'현장의 조명이나 촬영 조건에 따라 영상의 밝기, 대비, 잡음과 경계 표현이 달라질 수 있습니다. 하나의 필터가 모든 입력에 유리하다고 가정하기 어렵기 때문에, 서로 다른 변환에서 검출 성능을 비교했습니다. 연구 질문은 성능 유지 여부, 단일 필터의 상대적 성능, 그리고 조합의 구성 필터 대비 개선 여부입니다. 평가 범위는 일반 영상과 합성 가우시안 잡음이며, 현장의 모든 변화를 포괄하지는 않습니다.',
old[2],
'이제 실제 연구 코드에서 저장한 동일 영상의 변환 예시를 보시겠습니다. Original은 전처리하지 않은 입력이고, Invert는 밝기값을 반전합니다. Otsu Threshold는 히스토그램에서 자동으로 정한 임계값으로 이진화합니다. 사진은 변환 효과를 설명하는 한 장의 예시이며, 이후 성능 수치는 전체 오백 장의 평가 결과입니다.',
'Solarize는 이번 구현에서 영상의 평균 밝기보다 큰 값만 반전합니다. Histogram Equalization은 전체 밝기 분포를 변환하고, CLAHE는 영역별 대비를 조정합니다. CLAHE의 clip limit은 사십, 격자는 십육 곱하기 십육입니다. 서로 다른 영상 표현이 만들어지는 것을 확인할 수 있습니다.',
'Gamma는 밝기값을 영점 삼 제곱한 결과입니다. Gaussian Blur는 표준편차 이십 화소, 백이십일 곱하기 백이십일 커널로 평활화합니다. Sobel Edges는 경계 응답을 계산한 뒤 최댓값으로 정규화하고 제곱근을 적용합니다. 일반적인 필터 이름만이 아니라 실제 구현과 고정 파라미터를 기준으로 비교했습니다.',
'Emboss는 방향성 합성곱 응답에 gain 사를 적용하고 밝기 범위를 제한합니다. Unsharp는 표준편차 이의 평활화 영상과 원본의 차이를 여덟 배 가산합니다. 원본 사진을 함께 배치하여 변환 효과를 비교했습니다. 사진에 보이는 차이가 검출 성능의 향상을 바로 뜻하지는 않습니다.',
'복합 필터는 앞의 변환 결과에 뒤의 변환을 순차 적용합니다. Invert+CLAHE는 반전 후 지역 대비 조정, Blur+Otsu는 평활화 후 이진화, Sobel+Invert는 경계 표현 후 반전입니다. 가능한 모든 조합이나 역순을 평가한 것은 아니며, 이름에 표시한 적용 순서를 유지했습니다.',
'나머지 조합은 Histogram Equalization 뒤에 Emboss를 적용하는 HistEq+Emboss와 Unsharp 뒤에 Sobel을 적용하는 Unsharp+Sobel입니다. 원본과 비교하면 각 단계가 입력 표현을 추가로 바꾸는 것을 볼 수 있습니다. 이러한 변화의 유효성은 구성 필터 대비 성능으로 확인하겠습니다.',
old[4],old[5],old[6],old[7],
'잡음 영상도 연구 코드가 저장한 동일 원장면의 예시입니다. 위와 아래는 각각 잡음 표준편차 사십과 팔십입니다. 밝기값에 평균 영의 가우시안 잡음을 더하고 영부터 이백오십오 사이로 제한한 후 각 필터를 적용했습니다. Gaussian Blur의 평활화와 Emboss의 응답 변화를 볼 수 있습니다. 각 조건의 저장 예시이며, 정량 비교는 전체 평가 영상에서 수행했습니다.',
old[8],old[9],old[10],
'일반 영상의 단일 시드에서는 Gamma, 합성 잡음 조건에서는 Gaussian Blur가 가장 높은 mAP를 보였습니다. 평가한 다섯 조합은 더 우수한 구성 필터의 mAP를 넘지 못했습니다. 따라서 영상 조건과 평가 지표를 구분하여 필터를 선택해야 합니다.',
'이상으로 발표를 마치겠습니다. 경청해 주셔서 감사합니다.'
]
# 새 사진 설명을 위한 시간을 확보하여 정량 결과 설명의 반복을 줄입니다.
scripts[9]=scripts[9].replace('모든 전처리와 영상 조건마다 사전학습된 YOLOv8n을 별도로 학습했습니다. 같은 조건의 학습, 검증, 평가 자료에는 동일한 전처리를 적용했습니다.','모든 전처리와 영상 조건마다 YOLOv8n을 별도로 학습하고, 학습과 평가에 같은 전처리를 적용했습니다.')
scripts[10]=scripts[10].replace('이 결과는 전처리를 적용해도 대부분의 조건에서 성능을 보존할 수 있었지만, 모든 변환이 동일하게 유효하지는 않았음을 보여줍니다. 다음으로 두 필터를 함께 적용했을 때의 결과를 보겠습니다.','따라서 모든 변환에서 동일하게 성능이 유지되지는 않았습니다.')
scripts[11]=scripts[11].replace('다만 이것을 모든 조합에 대한 부정적인 결론으로 확대할 수는 없습니다. 이번에 평가한 다섯 가지 순서와 고정 파라미터에서 관찰한 결과입니다.','결론은 평가한 다섯 가지 순서와 고정 파라미터에 한정합니다.')
scripts[12]='일반 영상의 엄격 검출 정확도는 CLAHE 단독이 구십육 점 사 퍼센트로 단일 필터 중 가장 높았습니다. 반면 mAP는 Gamma가 가장 높았습니다. Invert+CLAHE의 엄격 검출 정확도는 구십팔 퍼센트로, CLAHE보다 일점 육 퍼센트포인트 높았지만 mAP는 낮았습니다. 두 지표는 대응 기준과 추론 임계값이 달라 서로 다른 정보를 제공합니다. 구십팔 퍼센트라는 단일 결과의 재현성은 뒤에서 반복 평가로 확인하겠습니다.'
scripts[14]=scripts[14].replace('잡음은 팔 비트 밝기값에 가우시안 잡음을 더하고 범위를 제한한 뒤 필터를 적용하여 구성했습니다. ','')
scripts[5]=scripts[5].replace('Gamma는 밝기값을 영점 삼 제곱한 결과입니다.', 'Gamma는 영부터 일로 정규화한 밝기값을 영점 삼 제곱한 결과입니다.')
titles[13]='가우시안 잡음 영상: Noise std=40'
titles.insert(14,'가우시안 잡음 영상: Noise std=80')
durations[13]=15
durations.insert(14,15)
for slide,seconds in {3:50,5:20,8:20,10:45,11:45,12:45,14:20,15:20,16:45,17:50,18:40}.items():durations[slide-1]=seconds
scripts[13]='표준편차 사십의 잡음을 추가한 실제 저장 예시입니다. 왼쪽은 잡음 입력, 가운데는 그 입력에 Gaussian Blur를, 오른쪽은 Emboss를 적용한 결과입니다. 사진은 동일 원장면의 시각화 예시이며, 이후 정량 수치는 전체 평가 영상에서 계산했습니다.'
scripts.insert(14,'표준편차 팔십에서는 잡음이 더 강합니다. 밝기값에 잡음을 더하고 영부터 이백오십오 사이로 제한한 뒤 필터를 적용했습니다. 평활화와 경계 응답의 차이가 보이지만, 사진의 외관만으로 성능을 판단하지 않고 전체 영상의 지표를 비교하겠습니다.')
slides=[]
elapsed=0
for number,(title,seconds,spoken) in enumerate(zip(titles,durations,scripts),1):
    slides.append({'number':number,'title':title,'duration_seconds':seconds,'start_seconds':elapsed,'end_seconds':elapsed+seconds,'spoken_script':spoken})
    elapsed+=seconds
assert elapsed==600
content={'main_duration_seconds':600,'main_slides':20,'total_slides':20,'timing_note':'목표 시간이며 실제 소요 시간은 리허설로 조정합니다. 모든 20장을 본발표에 사용합니다.','slides':slides}
(ROOT/'work/content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2),encoding='utf-8')
def clock(v):return f'{v//60:02d}:{v%60:02d}'
txt=['10분 학술대회 발표 대본','본발표 20장, 목표 10분. 실제 소요 시간은 리허설로 조정하십시오.','사진은 동일 원장면의 시각화 예시이며 성능은 전체 500장 평가 결과입니다.','']
for s in slides:
    txt+=[f'[{s["number"]:02d}] '+s['title'].replace('\n',' '),f'{clock(s["start_seconds"])}–{clock(s["end_seconds"])}, 목표 {s["duration_seconds"]}초','[발화문]',s['spoken_script'],'[전환] '+('다음 화면으로 전환합니다.' if s['number']<20 else '질문을 받습니다.'),'']
txt+=['질의응답 준비','질문: 98.0%를 얻은 조합이 가장 좋은가요?','답변: 단일 시드의 엄격 검출 정확도 결과입니다. 세 시드 반복 평균은 Original과 비슷하고 mAP는 더 낮아 안정적인 우월성을 주장하지 않습니다.','질문: 현장의 미지 영상에도 바로 적용할 수 있나요?','답변: 조건별 재학습 실험이므로 고정 모델의 미지 조건 적응성은 별도 평가가 필요합니다. 촬영 로트가 다른 독립 자료와 내부 그룹 분리가 후속 과제입니다.']
(ROOT/'결과/10분_발표대본.txt').write_text('\n'.join(txt),encoding='utf-8')

photo_pages={4:['original_example.png','invert_example.png','otsu_threshold_example.png'],5:['solarize_example.png','histogram_equalization_example.png','clahe__max_example.png'],6:['gamma_0_3_example.png','gaussian_blur__max_example.png','sobel_edges_example.png'],7:['emboss_example.png','unsharp__max_example.png','original_example.png'],8:['invert_clahe_example.png','blur_otsu_example.png','sobel_invert_example.png'],9:['histeq_emboss_example.png','unsharp_sobel_example.png','original_example.png'],14:['noise_std_40_example.png','gaussian_blur__max____noise_40_example.png','emboss___noise_40_example.png','noise_std_80_example.png','gaussian_blur__max____noise_80_example.png','emboss___noise_80_example.png']}
baseline=Image.open(ROOT/'work/source_photos/original_example.png').convert('RGB')
photo_pages[15]=photo_pages[14][3:]
photo_pages[14]=photo_pages[14][:3]
base=baseline.crop((0,60,736,588)).tobytes()
photos=[]
for slide,files in photo_pages.items():
    for name in files:
        f=ROOT/'work/source_photos'/name
        image=Image.open(f).convert('RGB')
        assert image.size==(1472,588),(name,image.size)
        noise_std=40 if slide==14 else (80 if slide==15 else 0)
        reference=base if noise_std==0 else Image.open(ROOT/f'work/source_photos/noise_std_{noise_std}_example.png').convert('RGB').crop((0,60,736,588)).tobytes()
        same=image.crop((0,60,736,588)).tobytes()==reference
        assert same, name+' 원본 패널 불일치'
        photos.append({'slide':slide,'file':name,'local_path':str(f),'container_source':'2026-2:/root/추계학술대회/yolo_filter_samples/'+name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source_size':[1472,588],'native_crop':{'left':0.5,'top':0,'right':0,'bottom':0},'same_condition_input_panel':same,'noise_std':noise_std,'original_image':'DataSet/images/train/1001.png','code_cell':32,'code_function':'save_filter_example','sample_selection_cell':36})
manifest={'photos':photos,'unique_photo_count':len(set(x['file'] for x in photos)),'source_notebook_sha256':hashlib.sha256((ROOT/'work/research_notebook.ipynb').read_bytes()).hexdigest(),'same_scene_pixel_contract':'일반 사진은 깨끗한 Original, 잡음 사진은 동일 잡음 조건의 Original 왼쪽 패널에서 상단 라벨을 제외한 y>=60 영역의 픽셀이 모두 일치합니다.','notes':'원본 PNG는 변경하지 않으며 PPT의 네이티브 이미지 자르기로 오른쪽 변환 결과를 표시합니다. 잡음 사진의 왼쪽 Original은 잡음을 추가한 입력입니다.'}
(ROOT/'evidence/photo_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
image_output=ROOT/'결과/사용이미지'
image_output.mkdir(parents=True,exist_ok=True)
for name in set(x['file'] for x in photos):shutil.copyfile(ROOT/'work/source_photos'/name,image_output/name)
(image_output/'이미지_출처.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
source=json.loads((ROOT.parent/'1차/evidence/content_sources.json').read_text(encoding='utf-8'))
source['hangul_syllables']=sum('\uac00'<=c<='\ud7a3' for s in slides for c in s['spoken_script'])
source['main_duration_seconds']=600
source['sources'].append({'path':str(ROOT/'work/research_notebook.ipynb'),'sha256':hashlib.sha256((ROOT/'work/research_notebook.ipynb').read_bytes()).hexdigest()})
(ROOT/'evidence/content_sources.json').write_text(json.dumps(source,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'main_seconds':600,'slides':20,'hangul_syllables':source['hangul_syllables'],'unique_photos':len(set(x['file'] for x in photos))},ensure_ascii=False))
