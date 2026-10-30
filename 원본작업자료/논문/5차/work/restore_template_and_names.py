import json,pathlib
W=pathlib.Path('work')
p=W/'content_v2.json';c=json.loads(p.read_text(encoding='utf8'))
# Preserve the recorded filter identifiers, including ordered combination names.
replacements={
 '반전 후 CLAHE':'Invert+CLAHE', '반전+CLAHE':'Invert+CLAHE', '블러+Otsu':'Blur+Otsu',
 'Sobel+반전':'Sobel+Invert', '히스토그램 평활화+엠보싱':'HistEq+Emboss','언샤프+Sobel':'Unsharp+Sobel',
 '감마 보정이':'Gamma 0.3이','감마 보정을':'Gamma 0.3을','감마 보정,':'Gamma 0.3,',
 '가우시안 블러가':'Gaussian Blur (max)가','가우시안 블러는':'Gaussian Blur (max)는',
 '엠보싱은':'Emboss는','엠보싱 gain':'Emboss gain','언샤프 amount':'Unsharp (max)의 amount',
 '감마와 Sobel':'Gamma 0.3과 Sobel Edges','CLAHE 96.4%':'CLAHE (max) 96.4%',
 'CLAHE 단독':'CLAHE (max) 단독','원영상':'Original','Otsu는':'Otsu Threshold는',
 '블러 82.86':'Gaussian Blur (max) 82.86','모두 블러가':'모두 Gaussian Blur (max)가',
 'Gamma correction yields':'Gamma 0.3 yields','Gaussian blur performs':'Gaussian Blur (max) performs',
 'inversion followed by CLAHE':'Invert+CLAHE',
}
for col in c['columns']:
 for item in col:
  s=item[1]
  if s.startswith('단일 필터는 반전,'):
   s='단일 필터는 Invert, Otsu Threshold, Solarize, Histogram Equalization, CLAHE (max), Gamma 0.3, Gaussian Blur (max), Sobel Edges, Emboss, Unsharp (max)이다. 밝기·대비·평활화·경계 강조 등 서로 다른 변환을 비교한다.'
  elif s.startswith('복합 필터는 반전→'):
   s='복합 필터는 Invert+CLAHE, Blur+Otsu, Sobel+Invert, HistEq+Emboss, Unsharp+Sobel의 5종이다. A+B는 A 후 B를 적용하며 역순과 모든 조합을 시험한 것은 아니다. 그림에는 공간에 맞춰 영어 이름을 축약하였다.'
  else:
   for a,b in replacements.items():s=s.replace(a,b)
   s=s.replace('감마 보정은 0.3','Gamma 0.3의 지수는 0.3').replace('CLAHE[2]','CLAHE (max)[2]')
  item[1]=s
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
v=(W/'verify_filter_paper_bold.py').read_text(encoding='utf8')
v=v.replace('docx_bold/','docx_graph_bold/').replace('r.bold is True','r.bold is False').replace("'all_document_text_bold':True","'all_document_text_bold':False, 'document_font_style':'original HWP template'")
v=v.replace('filter_paper_package_bold','filter_paper_package_template').replace('추계학술대회_필터비교_전체볼드_3쪽','추계학술대회_표준양식_영문필터_3쪽').replace('추계학술대회_전체볼드_그림과코드','추계학술대회_영문필터_그림과코드')
v=v.replace('본문·제목·캡션·머리말·쪽번호·참고문헌 및 모든 그래프 글씨에 Bold를 적용했습니다.','그래프 글씨만 NanumGothic Bold입니다. 문서 제목·본문·캡션·참고문헌은 HWP 표준양식의 글꼴과 굵기를 사용합니다. 필터 이름은 원본 코드의 영어 이름을 사용합니다.')
v=v.replace('본문 글꼴·용지·여백은 HWP 양식을 따르고 사용자 요청에 따라 전체 Bold를 적용했습니다.','본문 글꼴·굵기·용지·여백은 HWP 양식을 따릅니다.')
(W/'verify_filter_paper_template.py').write_text(v,encoding='utf8')
print('Restored template weights and original English filter identifiers')
