import csv
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(r'C:\Users\PUVKID\Documents\Codex\2026-10-13\x20\work\figures')
a = json.loads((RAW / 'results_summary.json').read_text(encoding='utf-8'))
b = json.loads((RAW / 'sweep_results.json').read_text(encoding='utf-8'))
single = [a['baseline']] + a['round1']
combo = [a['baseline']] + a['round2']
noise = [[x['map50_95'], b['grid']['40'][i]['map50_95'], b['grid']['80'][i]['map50_95']] for i, x in enumerate(single)]
rows = list(csv.DictReader((RAW / 'ms_run_results.csv').open(encoding='utf-8-sig')))
repeat = {}
for r in rows:
    k = r['condition'] + '/' + r['method']
    repeat.setdefault(k, []).append({key: float(r[key]) for key in ['seed', 'map50_95', 'strict_acc']})
stats = {k: {m: {'mean': statistics.mean(x[m] for x in v), 'sd': statistics.stdev(x[m] for x in v)} for m in ['map50_95', 'strict_acc']} for k,v in repeat.items()}
data = {'single': [{k:x[k] for k in ['name','map50_95','strict_acc']} for x in single], 'combo': [{k:x[k] for k in ['name','map50_95','strict_acc']} for x in combo], 'noise':noise,'repeat':repeat,'stats':stats}
(ROOT/'work/data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

# 각 문단은 발표자 노트와 별도 대본에 같은 내용으로 저장합니다.
titles = ['YOLOv8n 기반 볼 검출을 위한\n단일 및 복합 전처리 필터의 성능 비교','현장 영상의 변화와 연구 질문','데이터와 그룹 기반 평가','단일 필터와 순차 조합','조건별 학습과 두 평가 지표','일반 영상의 단일 필터 성능','복합 필터와 구성 필터 비교','평가 지표에 따른 순위 차이','잡음 조건에 따른 성능 변화','세 시드 반복 평가','해석 범위와 후속 검증','결론','부록 1. 주요 실험 파라미터','부록 2. 지표 해석과 예상 질문','부록 3. 참고문헌']
durations = [30,45,55,55,60,65,60,50,65,55,35,25,0,0,0]
scripts = [
'안녕하십니까. 경기대학교 컴퓨터과학과 곽윤석입니다. 오늘은 YOLOv8n 기반 볼 검출을 위한 단일 및 복합 전처리 필터의 성능 비교 연구를 발표하겠습니다. 본 연구는 현장의 입력 영상이 달라질 수 있다는 문제에서 출발했습니다. 여러 전처리에서 검출 성능이 유지되는지, 어떤 단일 필터와 순차 조합이 유리한지를 동일한 평가 체계에서 비교했습니다. 먼저 평가 설계를 설명하고, 일반 영상과 잡음 조건의 결과를 말씀드리겠습니다.',
'현장에서는 조명이나 촬영 조건에 따라 밝기와 대비가 달라지고, 잡음이나 경계 표현도 변할 수 있습니다. 따라서 특정 필터의 일반 영상 성능만으로 적용성을 판단하기에는 한계가 있습니다. 이번 연구에서는 필터를 적용한 뒤에도 검출 성능이 유지되는지, 단일 필터 중 어떤 조건이 높은 성능을 보이는지, 그리고 두 필터를 순차적으로 적용하면 구성 필터보다 개선되는지를 확인했습니다. 성능 비교의 대상은 볼 검출이며, 객체의 위치와 영상 전체의 검출 완전성을 함께 살펴보았습니다. 다만 실제 현장의 모든 변화를 재현한 실험은 아니므로, 결과는 일반 영상과 합성 가우시안 잡음의 범위에서 해석하겠습니다.',
'사용한 자료는 가로 이천구백사십사, 세로 이천삼백오십이 화소의 회색조 영상 오백 장과 볼 경계 상자 주석입니다. 별도로 수집한 외부 시험 자료 없이 기존 학습 및 검증 영상을 재분할했습니다. 유사 영상이 학습과 외부 평가에 동시에 들어가는 문제를 줄이기 위해, 축소 영상 사이의 평균 절대차를 기준으로 삼백육십팔 개의 그룹을 구성했습니다. 외부 평가는 이 그룹 단위의 오 겹 교차검증으로 수행했으며, 외부 평가 그룹과 나머지 자료 사이의 중복은 없었습니다. 각 영상은 자신을 학습에 사용하지 않은 모델로 평가했습니다. 다만 내부 학습과 검증 사이에는 아홉 개에서 스무 개의 그룹이 중복되어, 모델 선택 과정의 독립성에는 제한이 남습니다.',
'단일 필터는 화면에 제시한 열 종입니다. 밝기와 대비를 바꾸는 변환, 평활화, 경계 강조, 이진화를 포함하여 서로 다른 영상 표현을 비교했습니다. 각 필터의 파라미터는 실험 전체에서 고정했으며, 이름에 포함한 max는 이번 연구에서 설정한 강도를 나타냅니다. 최적값을 탐색하여 얻은 결과는 아닙니다. 복합 필터는 Invert+CLAHE 등 다섯 가지를 사용했습니다. 여기서 더하기 기호는 두 결과를 합친다는 뜻이 아니라, 앞의 필터를 적용한 영상에 뒤의 필터를 순차적으로 적용한다는 뜻입니다. 가능한 모든 조합이나 역순을 평가하지 않았으므로, 조합의 결론도 이 다섯 가지 순서에 한정합니다.',
'모든 전처리와 영상 조건마다 사전학습된 YOLOv8n을 별도로 학습했습니다. 같은 조건의 학습, 검증, 평가 자료에는 동일한 전처리를 적용했습니다. 공통 설정은 최대 삼십 에폭, 입력 크기 천이백팔십, 배치 여덟, 조기 종료 patience 십오입니다. 주 지표인 mAP50-95는 IoU 영점 오부터 영점 구오까지의 평균 정밀도를 종합하고, 외부 평가 다섯 폴드의 평균으로 보고했습니다. 보조 지표인 엄격 검출 정확도는 중심점 기반 일대일 대응에서 누락과 추가 검출이 모두 없는 영상의 비율입니다. 두 지표는 대응 기준뿐 아니라 confidence와 NMS 임계값도 다릅니다. 따라서 숫자를 같은 의미의 정확도로 비교하지 않고, 각각 위치 정밀도와 영상 단위 검출 완전성의 관점에서 해석합니다.',
'먼저 일반 영상의 단일 시드 결과입니다. 원본 영상의 mAP50-95는 구십육 점 오삼 퍼센트였으며, Gamma 0.3이 구십육 점 칠공 퍼센트로 가장 높았습니다. 그러나 차이는 영점 일칠 퍼센트포인트로 작습니다. 일반 영상의 Gamma 조건을 여러 시드로 반복하지 않았으므로, 이 결과만으로 안정적인 우월성을 단정하기는 어렵습니다. 단일 필터 열 종 중 아홉 종은 구십삼 점 삼칠 퍼센트 이상을 보였습니다. 반면 Otsu Threshold는 육십 점 사육 퍼센트에 그쳐, 이번 이진화 설정에서는 원본에 가까운 검출 성능이 유지되지 않았습니다. 이 결과는 전처리를 적용해도 대부분의 조건에서 성능을 보존할 수 있었지만, 모든 변환이 동일하게 유효하지는 않았음을 보여줍니다. 다음으로 두 필터를 함께 적용했을 때의 결과를 보겠습니다.',
'복합 필터 중 가장 높은 mAP50-95는 Invert+CLAHE의 구십오 점 칠오 퍼센트입니다. 다만 Original의 구십육 점 오삼 퍼센트보다 낮고, 구성 필터인 CLAHE 단독의 구십오 점 구팔 퍼센트에도 미치지 못했습니다. 나머지 조합도 오른쪽에 제시한 각 구성 필터의 결과와 비교했습니다. 평가한 다섯 조합 모두 더 우수한 구성 필터의 mAP를 넘지 못했습니다. 특히 Blur+Otsu는 오십구 점 오팔 퍼센트로 낮았습니다. 따라서 이번 조건에서는 두 변환을 순차적으로 적용하는 것만으로 객체 수준 성능이 개선되지는 않았습니다. 다만 이것을 모든 조합에 대한 부정적인 결론으로 확대할 수는 없습니다. 이번에 평가한 다섯 가지 순서와 고정 파라미터에서 관찰한 결과입니다.',
'보조 지표를 보면 해석이 달라집니다. 일반 영상의 엄격 검출 정확도에서 CLAHE 단독은 구십육 점 사 퍼센트로 단일 필터 중 가장 높았습니다. 반면 mAP의 단일 필터 최고값은 앞서 설명한 Gamma에서 나왔습니다. Invert+CLAHE의 엄격 검출 정확도는 단일 시드에서 구십팔 퍼센트로, CLAHE 단독보다 일점 육 퍼센트포인트 높았습니다. 그러나 같은 조합의 mAP는 CLAHE보다 낮았습니다. 이는 위치의 겹침을 평가하는 지표와 영상 전체의 누락 및 추가 검출을 평가하는 지표가 서로 다른 정보를 제공하기 때문입니다. 또한 추론 임계값도 다르므로, 하나의 정확도 순위로 합쳐서 해석하면 안 됩니다. 구십팔 퍼센트라는 단일 결과의 재현성은 잠시 뒤 반복 평가에서 확인하겠습니다.',
'화면은 일반 영상과 잡음 표준편차 사십, 팔십에서 전체 단일 필터의 mAP를 비교한 결과입니다. 각 셀의 값은 원정밀도 결과에서 한 번만 반올림했습니다. 잡음은 팔 비트 밝기값에 가우시안 잡음을 더하고 범위를 제한한 뒤 필터를 적용하여 구성했습니다. Gaussian Blur는 잡음 사십에서 팔십팔 점 칠구 퍼센트, 잡음 팔십에서 팔십이 점 구사 퍼센트로 가장 높았습니다. 일반 영상에서는 원본보다 낮았지만, 잡음이 있는 조건에서는 상대적으로 유리했습니다. 반대로 Emboss는 일반 영상에서 구십육 점 영육 퍼센트였으나, 잡음 사십과 팔십에서 각각 영점 팔칠과 영점 영팔 퍼센트로 크게 감소했습니다. 이 대비는 일반 영상에서 좋은 필터도 입력 조건이 달라지면 성능을 유지하지 못할 수 있음을 보여줍니다. 복합 필터의 잡음 조건은 이번 비교에 포함하지 않았습니다.',
'주요 후보는 시드 사십이, 사십삼, 사십사에서 반복했습니다. 화면의 각 점은 시드별 결과이며, 함께 제시한 값은 세 시드 평균과 표본 표준편차입니다. 일반 영상에서 Invert+CLAHE의 엄격 검출 정확도는 구십오 점 사칠 플러스마이너스 이점 이칠 퍼센트였습니다. Original은 구십오 점 사공 플러스마이너스 영점 오삼 퍼센트로, 평균 차이는 영점 영칠 퍼센트포인트에 그쳤습니다. 단일 시드의 구십팔 퍼센트가 일관된 향상으로 이어지지 않은 것입니다. 반면 잡음 팔십에서 Gaussian Blur의 mAP는 팔십이 점 팔육 플러스마이너스 영점 영팔 퍼센트로, Original의 칠십구 점 육공보다 세 시드 모두 높았습니다. 다만 시드마다 분할과 잡음 실현도 함께 바뀌었으므로, 변동 전체를 학습 난수 하나의 영향으로 해석하지는 않습니다.',
'결과의 해석에는 세 가지 제한이 있습니다. 우선 조건마다 모델을 다시 학습했으므로, 하나의 고정 모델이 미지의 현장 영상에 그대로 대응한다는 근거는 아닙니다. 또한 외부 평가 그룹은 분리했지만 내부 검증에는 유사 그룹의 중복이 남았습니다. 마지막으로 전체 후보의 다중 시드 반복과 복합 필터의 잡음 조건 평가는 수행하지 않았습니다. 후속 연구에서는 내부 분할도 그룹 단위로 분리하고, 촬영 로트가 다른 독립 자료로 검증할 필요가 있습니다. 이 범위를 명확히 한 상태에서 필터 선택의 기준으로 결과를 활용하고자 합니다.',
'정리하겠습니다. 일반 영상에서는 Gamma 0.3, 합성 잡음 조건에서는 Gaussian Blur가 가장 높은 mAP를 보였습니다. 평가한 다섯 조합은 더 우수한 구성 필터의 mAP를 넘지 못했습니다. 따라서 영상 조건과 목적 지표를 구분하여 필터를 선택해야 합니다. 이상으로 발표를 마치겠습니다. 경청해 주셔서 감사합니다.',
'질문이 있을 때 참고할 실험 파라미터입니다. CLAHE는 clip limit 40과 16×16 격자, Gaussian Blur는 표준편차 20 화소와 121×121 커널을 사용했습니다. 이 값들은 사전에 고정한 비교 조건이며 최적 파라미터라는 의미는 아닙니다.',
'예상 질문에 대한 답변입니다. 첫째, 98.0%가 가장 좋은 필터라는 뜻인지를 물으신다면 단일 시드의 엄격 검출 정확도에서만 해당하며, 반복 결과와 mAP에서는 안정적 우월성을 확인하지 못했다고 답변하겠습니다. 둘째, 외부 평가의 그룹 중복은 없지만 내부 학습과 검증에는 9~20개 그룹이 중복되었다고 구분하여 설명하겠습니다. 셋째, 미지 현장에서 바로 사용할 수 있는지는 촬영 로트가 다른 독립 자료와 고정 모델의 별도 검증이 필요하다고 답변하겠습니다.',
'본 연구에서 사용한 YOLOv8, CLAHE와 Kornia의 문헌입니다. 발표 본문의 데이터와 수치는 제출 논문의 원자료에 근거했습니다.'
]
scripts[4] = scripts[4].replace('각각 위치 정밀도와 영상 단위 검출 완전성', '각각 객체 수준의 검출 성능과 영상 단위 검출 완전성')
scripts[6] = scripts[6].replace('나머지 조합도 오른쪽에 제시한 각 구성 필터의 결과와 비교했습니다.', '각 조합을 더 우수한 구성 필터의 결과와 비교했습니다.')
scripts[8] = scripts[8].replace('각 셀의 값은 원정밀도 결과에서 한 번만 반올림했습니다. ', '')
slides=[]
t=0
for i,(title,duration,script) in enumerate(zip(titles,durations,scripts),1):
    slides.append({'number':i,'title':title,'duration_seconds':duration,'start_seconds':t if duration else None,'end_seconds':t+duration if duration else None,'spoken_script':script})
    t += duration
assert t == 600
content={'main_duration_seconds':t,'main_slides':12,'total_slides':15,'timing_note':'목표 시간이며 실제 소요 시간은 리허설로 조정합니다. 부록 3장은 10분에 포함하지 않습니다.','slides':slides}
(ROOT/'work/content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2),encoding='utf-8')
source_paths=[RAW/'results_summary.json',RAW/'sweep_results.json',RAW/'ms_run_results.csv',Path(r'D:\2026\추계학술대회\논문\3차\추계학술대회 논문 3차.hwp'),Path(r'C:\Users\PUVKID\Desktop\2026\하계학술대회 논문\곽윤석\발표 자료\하계학술대회 PPT.pptx')]
evidence={'sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in source_paths],'hangul_syllables':sum('\uac00'<=c<='\ud7a3' for x in slides[:12] for c in x['spoken_script']),'main_duration_seconds':600,'rounding_corrected':{'Otsu Threshold/noise80':f'{noise[2][2]:.1f}','Histogram Equalization/noise40':f'{noise[4][1]:.1f}','Sobel Edges/noise80':f'{noise[8][2]:.1f}'}}
(ROOT/'evidence/content_sources.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
def clock(s): return f'{s//60:02d}:{s%60:02d}'
out=['10분 학술대회 발표 대본','본발표 12장, 목표 10분. 실제 소요 시간은 리허설로 조정하십시오.','부록 3장은 질의응답용으로 본발표 시간에 포함하지 않습니다.','']
for x in slides:
    stamp=f"{clock(x['start_seconds'])}–{clock(x['end_seconds'])}, 목표 {x['duration_seconds']}초" if x['duration_seconds'] else '질의응답용 부록'
    out += [f"[{x['number']:02d}] {x['title'].replace(chr(10),' ')}",stamp,'[강조] '+(['연구 목적과 발표 범위','입력 조건에 따른 필터 선택','외부 평가의 그룹 분리','A+B의 적용 순서','mAP와 엄격 검출 정확도의 차이','단일 시드의 작은 차이','구성 필터 대비 개선 여부','지표를 나누어 해석','잡음에서의 순위 변화','단일 시드와 반복 결과 구분','검증 범위와 후속 과제','조건과 목적 지표에 따른 선택']+[ '질의응답 참고']*3)[x['number']-1],'[발화문]',x['spoken_script'],'[전환] '+('다음 화면으로 전환합니다.' if x['number']<12 else '질문을 받습니다.'),'']
(ROOT/'결과/10분_발표대본.txt').write_text('\n'.join(out),encoding='utf-8')
print(json.dumps(evidence,ensure_ascii=False,indent=2))
