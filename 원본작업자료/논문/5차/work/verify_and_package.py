import ast,csv,hashlib,json,pathlib,shutil,zipfile,statistics
from collections import defaultdict
from pypdf import PdfReader
from docx import Document
from docx.oxml.ns import qn
from PIL import Image
import re
P=pathlib.Path;W=P('work');O=P('outputs');O.mkdir(exist_ok=True)
figures=list((W/'restyled_english').rglob('*.png'))
assert len(figures)==99,len(figures)
for f in figures:
 info=json.loads(Image.open(f).info['Description'])
 assert not any(re.search(r'[\uac00-\ud7af\u3131-\u318e]',t) for t in info['visible_text']),f
 assert all(r['angle']==90 for r in info['filter_label_rotations']),(f,info['filter_label_rotations'])
old=json.loads((W/'notebook.ipynb').read_text(encoding='utf8'))
new=json.loads((W/'ball_ok_ng_yolo_v7_reference.ipynb').read_text(encoding='utf8'))
changed=[]
for i,(a,b) in enumerate(zip(old['cells'],new['cells'][1:])):
 if a['source']!=b['source']:changed.append(i)
 if b['cell_type']=='code':ast.parse(''.join(b['source']))
assert changed==[4,22,34,46,55,61,72],changed
for f in ['reference_plot_style.py','render_saved_figures.py']:ast.parse((W/f).read_text(encoding='utf8'))
rows=list(csv.DictReader((W/'figures/ms_per_image.csv').open(encoding='utf-8-sig')))
groups=defaultdict(list)
for r in rows:groups[(r['condition'],int(r['seed']),r['method'])].append(r)
assert len(rows)==19500 and len(groups)==39
for r in csv.DictReader((W/'figures/ms_run_results.csv').open(encoding='utf-8-sig')):
 g=groups[(r['condition'],int(r['seed']),r['method'])];assert len(g)==500
 strict=100*sum(int(x['miss'])==0 and int(x['extra'])==0 for x in g)/len(g)
 acc=100*sum(int(x['match']) for x in g)/len(g)
 assert abs(strict-float(r['strict_acc']))<1e-8
 assert abs(acc-float(r['accuracy']))<1e-8
pdf=PdfReader(W/'docx_verified/paper.pdf');assert len(pdf.pages)==3
d=Document(W/'paper.docx');assert len(d.inline_shapes)==2 and not d.tables
assert d.core_properties.author==''
for s in d.sections:
 assert abs(s.page_width.mm-190)<.1 and abs(s.page_height.mm-260)<.1
 assert abs(s.left_margin.mm-20)<.1 and abs(s.right_margin.mm-20)<.1
assert len(d._element.xpath('.//w:pBdr'))==0
doc=O/'추계학술대회_3쪽논문_영문그래프.docx';shutil.copy2(W/'paper.docx',doc)
pkg=W/'delivery_package_english';pkg.mkdir(exist_ok=True)
for p in ['논문에_사용한_그림','수정_코드/fonts','실험결과_원자료','추가_그래프']:(pkg/p).mkdir(parents=True,exist_ok=True)
for n in [1,2]:shutil.copy2(W/f'restyled_english/paper_figure{n}.png',pkg/f'논문에_사용한_그림/그림{n}.png')
for f in ['reference_plot_style.py','render_saved_figures.py','ball_ok_ng_yolo_v7_reference.ipynb']:shutil.copy2(W/f,pkg/'수정_코드'/f)
for f in ['NanumGothic.ttf','NanumGothicBold.ttf']:
 shutil.copy2(P('C:/Users/PUVKID/AppData/Local/Microsoft/Windows/Fonts')/f,pkg/'수정_코드/fonts'/f)
shutil.copy2(W/'NanumGothic-LICENSE.txt',pkg/'수정_코드/fonts/LICENSE.txt')
for f in (W/'figures').glob('*.csv'):shutil.copy2(f,pkg/'실험결과_원자료'/f.name)
for f in ['results_summary.json','sweep_results.json']:shutil.copy2(W/'figures'/f,pkg/'실험결과_원자료'/f)
for f in (W/'restyled_english').rglob('*.png'):
 if f.name.startswith('paper_'):continue
 dest=pkg/'추가_그래프'/f.relative_to(W/'restyled_english');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
report={'docx_pages_rendered':3,'embedded_figures':2,'tables':0,'per_image_rows_verified':len(rows),
 'runs_verified':len(groups),'notebook_changed_original_cell_indices':changed,
 'research_results_modified':False,'training_rerun':False,'figures_rendered':len(list((W/'restyled_english').rglob('*.png'))),
 'original_notebook_sha256':hashlib.sha256((W/'notebook.ipynb').read_bytes()).hexdigest()}
(pkg/'검증결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(pkg/'읽어주세요.txt').write_text('''추계학술대회 논문 및 그래프 수정본

논문: 편집 가능한 DOCX 3쪽, 그림 2개, 표 없음, 저자·소속 공란.
DOCX를 실제 페이지로 렌더링하여 3쪽과 글자/그림 배치를 확인했습니다.
한글로 가져오면 프로그램의 조판 차이 때문에 줄바꿈이 달라질 수 있습니다.

본문 서식 (제공된 HWP 양식 기준)
용지 190×260 mm, 좌우 20 mm, 위아래 17.5 mm, 2단 간격 8 mm.
국문 제목 휴먼명조 17 pt / 영문 제목 HY견명조 15 pt.
본문 휴먼명조 10 pt / 절 제목 휴먼고딕 11 pt / 소제목 HY중고딕 11 pt.
국문 요약 휴먼명조 9.2 pt / 영문 요약 Times New Roman 9.2 pt.
그림 설명 HY중고딕 9 pt / 참고문헌 Times New Roman 10 pt.
장평 90%, 자간은 제목 -7%, 일반 문구 -6%를 OOXML에 적용했습니다.
상용 본문 글꼴 파일은 포함하지 않았습니다. 현재 PC에 설치된 글꼴을 사용합니다.

그림 서식
첨부된 하계 노트북의 나눔고딕 Regular를 기본으로 하고 수치만 Bold를 씁니다.
기본 막대그래프는 축 제목 45 pt, 눈금 35 pt, 수치 35 pt Bold, 범례 40 pt.
그래프 안의 모든 표기는 영어이며, 필터 이름은 90도 세로 방향입니다.
긴 이름도 줄바꿈 없이 읽을 수 있도록 아래 여백과 글자 크기를 조절했습니다.
범례는 데이터 위에 겹치지 않게 바깥쪽에 배치했습니다. PNG는 150 dpi 원본입니다.
나눔고딕 Regular/Bold와 OFL 라이선스를 수정_코드/fonts에 포함했습니다.
논문에_사용한_그림의 2개 파일은 DOCX에 실제 삽입한 PNG와 동일합니다.

코드와 결과
추계 연구 노트북의 공통 막대그래프 함수와 저장 경로의 스타일 적용 부분을 수정했습니다.
종합 그림의 순위는 막대그래프로 표시합니다.
원본 코드의 학습, 데이터 분할, 모델, 판정 및 통계 계산은 유지했습니다.
이번 작업에서는 재학습하지 않고 저장된 추계 결과에서 그래프를 다시 생성했습니다.
하계 결과 JSON 수치는 추계 논문의 측정값으로 사용하지 않았습니다.
노트북의 오래된 출력 이미지는 비웠습니다. 원본은 컨테이너 code_backups에 보관했습니다.
실험결과 원자료의 39회 실행, 이미지별 19,500개 행을 재계산하여 요약값과 일치함을 확인했습니다.

그래프만 다시 생성 (학습 실행 없음)
패키지 최상위 폴더에서 아래 명령을 실행합니다.
python 수정_코드/render_saved_figures.py --results 실험결과_원자료 --output 새_그래프
필요 패키지: numpy, pandas, matplotlib. 현재 연구 컨테이너에 설치되어 있습니다.
원본 연구 전체를 실행하려면 기존 컨테이너의 데이터와 가중치 경로를 그대로 사용합니다.
노트북의 전체 실행은 원래 설정에 따라 학습을 수행할 수 있습니다.

검증의 범위
이번 문서의 수치 검증은 저장 결과의 재계산과 연구 코드 확인입니다.
새로운 학습 재현, 현장 데이터의 독립 검증, 외부 성능 검증을 했다는 의미는 아닙니다.
논문 본문에 주석 유도 OK/NG 정답, 내부 검증의 유사 영상 그룹 중복 등 한계를 명시했습니다.
''',encoding='utf-8-sig')
archive=O/'추계학술대회_영문그래프와수정코드.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in pkg.rglob('*'):
  if f.is_file():z.write(f,f.relative_to(pkg))
print(json.dumps(report,ensure_ascii=False));print('DOCX',doc.stat().st_size,'ZIP',archive.stat().st_size)
