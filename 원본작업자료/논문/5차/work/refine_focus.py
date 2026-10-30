from pathlib import Path
import json
p=Path('work/content_v2.json');c=json.loads(p.read_text(encoding='utf8'))
for col in c['columns']:
 for i,(k,s) in enumerate(col):
  s=s.replace('반전 후 CLAHE는 단일 시드의 엄격 정확도가 98.0%였으나 반복 실험에서 이득이 유지되지 않았다.','모든 조합의 mAP는 더 나은 구성 필터를 넘지 못했고, 반전 후 CLAHE의 단일 시드 엄격 정확도 이득도 반복 실험에서 유지되지 않았다.')
  s=s.replace('Inversion followed by CLAHE reaches 98.0% strict image-level detection accuracy in one seed, but its gain is not retained across repeated runs.','No combination exceeds its better component in mAP. The strict-accuracy gain of inversion followed by CLAHE in one seed is not retained across repeated runs.')
  s=s.replace('해당 후보를 다중 시드로 반복하지 않아','일반 영상의 감마 보정을 다중 시드로 반복하지 않아')
  s=s.replace('언샤프 마스크이다.','언샤프 마스크(US)이다.').replace('히스토그램 평활화, CLAHE','히스토그램 평활화(HE), CLAHE')
  s=s.replace('주요 후보는 시드 42·43·44로 반복하고, 잡음 40과 학습량 25%의 복합 조건도 분석하였다.','주요 후보는 시드 42·43·44로 반복하였다.')
  col[i]=[k,s]
col=c['columns'][5]
col[:]=[[k,s] for k,s in col if not s.startswith('잡음 40과 학습량 25%에서')]
for i,(k,s) in enumerate(col):
 if s.startswith('엠보싱은'):
  col[i]=[k,'엠보싱은 일반 영상 96.06%에서 잡음 40·80의 0.87%·0.08%로 감소하여 입력 변화에 민감했다. 잡음 80의 반복 mAP는 블러 82.86±0.08%, 원영상 79.60±0.26%로 세 시드 모두 블러가 높았다.']
 if s.startswith('시험한 설정에서'):
  col[i]=[k,'일반 영상의 단일 필터 mAP는 감마 보정, 잡음 영상에서는 가우시안 블러가 가장 높았다. 모든 조합이 더 나은 구성 필터의 mAP를 넘지 못했다. 입력 조건과 지표에 따른 선택이 필요하다.']
 if s.startswith('본 비교는 조건별'):
  col[i]=[k,'조건별 재학습 결과이므로 고정 모델의 미지 현장 적응성을 검증한 것은 아니다. 복합 필터의 잡음 평가와 전체 후보의 반복 실험이 필요하다. 내부 학습·검증 간 9~20개 유사 그룹의 중복도 해소하고 촬영 로트별 독립 자료로 검증해야 한다.']
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
p=Path('work/paper_filter_figures.py');s=p.read_text(encoding='utf8').replace('figsize=(11,12)','figsize=(11,10)').replace("[label(n) for n in df.Filter]","[label(n).replace('Solarize','Solar.') for n in df.Filter]");p.write_text(s,encoding='utf8')
# The main results-only renderer also produces the final paper's detection figures.
p=Path('work/render_saved_figures.py');s=p.read_text(encoding='utf8');a=s.index(' # Compact, readable figures');b=s.index(' # Track exact source files',a)
s=s[:a]+" from paper_filter_figures import make_paper_filter_figures\n make_paper_filter_figures(R,O)\n"+s[b:];p.write_text(s,encoding='utf8')
