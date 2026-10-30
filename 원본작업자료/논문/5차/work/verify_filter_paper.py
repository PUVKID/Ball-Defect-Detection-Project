import ast,csv,hashlib,json,pathlib,re,statistics,zipfile,shutil
from collections import defaultdict
from PIL import Image
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader
P=pathlib.Path;W=P('work');R=W/'figures';O=P('outputs');O.mkdir(exist_ok=True)
def rows(f):return list(csv.DictReader((R/f).open(encoding='utf-8-sig')))
summary=json.loads((R/'results_summary.json').read_text(encoding='utf8'))
sweep=json.loads((R/'sweep_results.json').read_text(encoding='utf8'))
src={r['name']:r for r in [summary['baseline']]+summary['round1']+summary['round2']}
for f in ['table_round1.csv','table_round2.csv']:
 for r in rows(f):
  s=src[r['Filter']]
  assert abs(float(r['mAP50-95 (%)'])-float(s['map50_95']))<.00501,(f,r['Filter'])
  assert abs(float(r['Strict Acc (%)'])-float(s['strict_acc']))<.00501
base=defaultdict(list)
for r in rows('per_image_predictions.csv'):base[r['method']].append(r)
checked=[]
noise_checked=0
for level in ['40','80']:
 grid={r['name']:r for r in sweep['grid'][level]}
 for r in rows(f'table_grid_noise{level}.csv'):
  assert abs(float(r['mAP50-95 (%)'])-grid[r['Filter']]['map50_95'])<.00501
  assert abs(float(r['Strict Acc (%)'])-grid[r['Filter']]['strict_acc'])<.00501
  noise_checked+=1
for name,s in src.items():
 g=base[name];assert len(g)==500
 strict=sum(int(r['miss'])==0 and int(r['extra'])==0 for r in g)/5
 assert abs(strict-s['strict_acc'])<1e-8
 checked.append(name)
multi=defaultdict(list)
for r in rows('ms_per_image.csv'):multi[(r['condition'],int(r['seed']),r['method'])].append(r)
for r in rows('ms_run_results.csv'):
 g=multi[(r['condition'],int(r['seed']),r['method'])];assert len(g)==500
 assert abs(sum(int(x['miss'])==0 and int(x['extra'])==0 for x in g)/5-float(r['strict_acc']))<1e-8
mp=defaultdict(list)
for r in rows('ms_run_results.csv'):mp[(r['condition'],r['method'])].append(float(r['map50_95']))
repeat=[{'condition':k[0],'filter':k[1],'mean':statistics.mean(v),'sample_sd':statistics.stdev(v),'seeds':v} for k,v in mp.items()]
assert max(src.values(),key=lambda s:s['map50_95'])['name']=='Gamma 0.3'
combo=json.loads((W/'restyled_horizontal/combination_detection_comparison.json').read_text())
assert all(r['mAP50-95 (%) gain vs best component']<0 for r in combo)
for n in [1,2,3]:
 image=Image.open(W/f'restyled_horizontal/paper_figure{n}.png');meta=json.loads(image.info['Description'])
 assert not any(re.search(r'[\uac00-\ud7af]',t) for t in meta['visible_text'])
 assert all(t['angle']==0 for t in meta['filter_label_rotations'])
pdf=PdfReader(W/'docx_focus_final/paper_v2.pdf');assert len(pdf.pages)==3
d=Document(W/'paper_v2.docx');assert len(d.inline_shapes)==3 and len(d.tables)==0
assert all(abs(s.width.mm-71)<.05 for s in d.inline_shapes)
assert d.core_properties.author==''
assert [s._sectPr.find(qn('w:cols')).get(qn('w:num')) for s in d.sections]==['1','2','2','2']
old=json.loads((W/'notebook.ipynb').read_text(encoding='utf8'));new=json.loads((W/'ball_ok_ng_yolo_v7_reference.ipynb').read_text(encoding='utf8'))
changed=[]
for i,(a,b) in enumerate(zip(old['cells'],new['cells'][1:])):
 if a['source']!=b['source']:changed.append(i)
 if b['cell_type']=='code':ast.parse(''.join(b['source']))
assert changed==[4,22,34,46,55,61,72]
assert len(new['cells'])==len(old['cells'])+3
ast.parse(''.join(new['cells'][-1]['source']))
for f in ['reference_plot_style.py','render_saved_figures.py','paper_filter_figures.py']:ast.parse((W/f).read_text(encoding='utf8'))
report={'pages':3,'figures':3,'figure_width_mm':71,'body_and_figures_columns':2,'title_block_columns':1,
 'tables':0,'single_filters':10,'ordered_combinations':5,'raw_image_rows_recalculated':8000+19500,'noise_grid_summaries_checked':noise_checked,
 'single_and_combo_methods_verified':checked,'multiseed_runs_verified':39,'repeat_map':repeat,
 'training_rerun':False,'measurements_changed':False,'notebook_changed_plotting_cells':changed,
 'sources_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in R.glob('*.csv')}}
pkg=W/'filter_paper_package';pkg.mkdir(exist_ok=True)
for folder in ['그림','코드/fonts','원자료']:(pkg/folder).mkdir(parents=True,exist_ok=True)
for n in [1,2,3]:
 for ext in ['png','pdf']:shutil.copy2(W/f'restyled_horizontal/paper_figure{n}.{ext}',pkg/f'그림/Figure_{n}.{ext}')
for f in ['reference_plot_style.py','render_saved_figures.py','paper_filter_figures.py','ball_ok_ng_yolo_v7_reference.ipynb']:shutil.copy2(W/f,pkg/'코드'/f)
for f in ['NanumGothic.ttf','NanumGothicBold.ttf']:shutil.copy2(P('C:/Users/PUVKID/AppData/Local/Microsoft/Windows/Fonts')/f,pkg/'코드/fonts'/f)
shutil.copy2(W/'NanumGothic-LICENSE.txt',pkg/'코드/fonts/LICENSE.txt')
for f in R.glob('*.csv'):shutil.copy2(f,pkg/'원자료'/f.name)
for f in ['results_summary.json','sweep_results.json']:shutil.copy2(R/f,pkg/'원자료'/f)
shutil.copy2(W/'restyled_horizontal/combination_detection_comparison.json',pkg/'원자료/combination_detection_comparison.json')
(pkg/'검증기록.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(pkg/'안내.txt').write_text('''단일 필터와 복합 필터 검출 비교 논문 수정본

본문과 그림은 모두 2단이며, 학회 양식의 제목·저자 공란만 양단을 가로지릅니다.
DOCX와 PDF는 같은 조판 결과의 3쪽이며 그림 3개, 표 0개입니다.
그림 폴더의 PNG는 문서에 삽입한 파일 그대로이고 PDF는 각 그림의 벡터 원본입니다.
그림 표기는 모두 영어이며 필터 이름은 짧은 가로 표기 또는 2줄입니다.
Orig.=Original, Inv.=Invert, Hist. Eq./HE=Histogram Equalization,
Gauss.=Gaussian Blur, Emb.=Emboss, US=Unsharp. A+B는 A 후 B입니다.

제공된 하계 노트북의 NanumGothic, 흰 배경, 막대 색상, 축 45 pt와 수치 35 pt Bold를 기반으로 했습니다.
한 단 너비 71 mm에서 읽히도록 11-inch 캔버스, 최대 6개 범주/패널을 사용했습니다.
필터 눈금은 31 pt로 줄 겹침을 방지했습니다. 본문 글꼴·용지·여백은 HWP 양식을 따랐습니다.
국문 제목 휴먼명조 17 pt, 영문 제목 HY견명조 15 pt, 본문 휴먼명조 10 pt,
절 제목 휴먼고딕 11 pt, 소제목 HY중고딕 11 pt, 캡션 HY중고딕 9 pt입니다.
용지 190×260 mm, 좌우 20 mm, 위아래 17.5 mm, 단 간격 8 mm입니다.
상용 본문 글꼴은 현재 PC의 설치본을 사용하고 배포하지 않습니다. NanumGothic과 라이선스는 포함했습니다.

그래프만 재생성 (모델 학습 없음):
python 코드/paper_filter_figures.py --results 원자료 --output 새_논문그림
전체 기존 결과 그래프도 다시 생성하려면:
python 코드/render_saved_figures.py --results 원자료 --output 새_전체그림
필요 패키지: numpy, pandas, matplotlib. 연구 컨테이너에 설치되어 있습니다.
학습·데이터 분할·평가 계산과 저장된 측정값은 바꾸지 않았습니다.
재학습은 수행하지 않았으며 저장된 per-image 결과를 재계산하고 표·JSON·그림을 대조했습니다.
mAP는 저장된 평가 요약과 대조했으며 원시 예측으로 AP를 새로 산출한 것은 아닙니다.
모든 단일·복합 비교는 시드 42이고, 다중 시드 결과는 본문에서 별도로 구분했습니다.
전체 후보·모든 조합·미지 현장 조건의 우월성까지 검증했다는 의미는 아닙니다.

참고문헌 확인 경로:
[1] https://docs.ultralytics.com/models/yolov8/
[2] https://github.com/erich666/GraphicsGems/blob/master/gemsiv/clahe.c
[3] https://arxiv.org/abs/1910.02190
''',encoding='utf-8-sig')
shutil.copy2(W/'paper_v2.docx',O/'추계학술대회_필터비교_2단_3쪽.docx')
shutil.copy2(W/'docx_focus_final/paper_v2.pdf',O/'추계학술대회_필터비교_2단_3쪽.pdf')
with zipfile.ZipFile(O/'추계학술대회_필터비교_그림과코드.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in pkg.rglob('*'):
  if f.is_file():z.write(f,f.relative_to(pkg))
print(json.dumps({k:v for k,v in report.items() if k not in ['sources_sha256','repeat_map']},ensure_ascii=False))
