import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/package/2006/relationships'}
checks = []
def check(ok, detail):
    checks.append({'pass':bool(ok),'detail':detail})
    if not ok:
        raise AssertionError(detail)
def read_json(p):
    return json.loads(p.read_text(encoding='utf-8'))
try:
    source = read_json(ROOT/'evidence/content_sources.json')
    for item in source['sources']:
        check(hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'], '입력 원본 해시 보존: '+Path(item['path']).name)
    content = read_json(ROOT/'work/content.json')
    data = read_json(ROOT/'work/data.json')
    chart_manifest = read_json(ROOT/'evidence/chart_data.json')
    raw_path = Path(source['sources'][0]['path']).parent
    raw = read_json(raw_path/'results_summary.json')
    sweep = read_json(raw_path/'sweep_results.json')
    originals = [raw['baseline']] + raw['round1']
    combos = [raw['baseline']] + raw['round2']
    check(data['single']==[{k:x[k] for k in ['name','map50_95','strict_acc']} for x in originals], '단일 필터 11개 데이터 원정밀도 보존')
    check(data['combo']==[{k:x[k] for k in ['name','map50_95','strict_acc']} for x in combos], '조합과 기준 6개 데이터 원정밀도 보존')
    expected_noise=[[x['map50_95'],sweep['grid']['40'][i]['map50_95'],sweep['grid']['80'][i]['map50_95']] for i,x in enumerate(originals)]
    check(data['noise']==expected_noise,'잡음 히트맵 33개 수치 원정밀도 보존')
    expected_values=[
        [[x['map50_95'] for x in originals]],
        [[x['map50_95'] for x in combos], [next(x['map50_95'] for x in originals if x['name']==n) for n in ['Original','CLAHE (max)','Gaussian Blur (max)','Sobel Edges','Histogram Equalization','Sobel Edges']]],
        [[next(x[m] for x in originals+combos if x['name']==n) for n in ['Original','Gamma 0.3','CLAHE (max)','Invert+CLAHE']] for m in ['map50_95','strict_acc']],
        [[x['strict_acc'] for x in data['repeat']['normal/'+n]] for n in ['Original','Invert+CLAHE']],
        [[x['map50_95'] for x in data['repeat'][next(k for k in data['repeat'] if '80' in k and k.endswith('/'+n))]] for n in ['Original','Gaussian Blur (max)']]
    ]
    for expected_chart, actual_chart in zip(expected_values,chart_manifest):
        for ex, ac in zip(expected_chart,actual_chart['series']):
            check(ac['values']==[float(format(x,'.15g')) for x in ex], '워크북 15유효자리 표현과 원자료 대조')
            check(all(abs(x-y)<=1e-12 and f'{x:.1f}'==f'{y:.1f}' and f'{x:.2f}'==f'{y:.2f}' for x,y in zip(ex,ac['values'])), '모든 차트 수치의 오차 한도와 1·2자리 표시 보존')
    deck = ROOT/'결과/추계학술대회_10분발표.pptx'
    check(deck.exists(), '최종 PPTX 존재')
    check(sum(x['duration_seconds'] for x in content['slides'][:12])==600, '본발표 12장 목표 시간 합계 600초')
    check(all(x['duration_seconds']==0 for x in content['slides'][12:]), '부록은 본발표 10분에서 제외')
    script = (ROOT/'결과/10분_발표대본.txt').read_text(encoding='utf-8',errors='strict')
    check('\ufffd' not in script, 'UTF-8 대본 대체 문자 없음')
    check(2500 <= sum('\uac00'<=c<='\ud7a3' for x in content['slides'][:12] for c in x['spoken_script']) <= 3300, '한국어 발화 분량 2500–3300음절')
    with zipfile.ZipFile(deck) as z:
        slide_names = sorted([x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)],key=lambda x:int(re.search(r'(\d+)\.xml',x).group(1)))
        check(len(slide_names)==15, '전체 15장')
        text_all = ''
        for i,name in enumerate(slide_names,1):
            root=ET.fromstring(z.read(name))
            text_all+='\n'.join(x.text or '' for x in root.findall('.//a:t',NS))
            check(content['slides'][i-1]['title'] in '\n'.join(x.text or '' for x in root.findall('.//a:t',NS)), f'{i}장 제목 전체 보존')
            note=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
            note_text='\n'.join(x.text or '' for x in note.findall('.//a:t',NS))
            expected=content['slides'][i-1]['spoken_script']
            check(expected in note_text and expected in script, f'{i}장 발화문: 노트·별도 대본 일치')
            text_all+=note_text
            for run in root.findall('.//a:r',NS):
                if not ''.join(run.itertext()).strip(): continue
                rp=run.find('a:rPr',NS)
                check(rp is not None and rp.get('b')=='1',f'{i}장 텍스트 Bold')
                check(rp.find('a:latin',NS).get('typeface')=='NanumGothic',f'{i}장 NanumGothic 서체')
        check(not any(x in text_all for x in ['EfficientNet','비식별화','의료 영상']), '하계 연구의 무관한 내용 없음')
        check('\ufffd' not in text_all, 'PPTX 텍스트 대체 문자 없음')
        chart_files=sorted([x for x in z.namelist() if re.fullmatch(r'ppt/slides/charts/chart\d+\.xml',x)],key=lambda x:int(re.search(r'(\d+)\.xml',x).group(1)))
        check(len(chart_files)==5,'편집 가능한 네이티브 차트 5개')
        for cfile,expected in zip(chart_files,chart_manifest):
            cr=ET.fromstring(z.read(cfile));series=cr.findall('.//c:ser',NS)
            check(len(series)==len(expected['series']),'차트 시리즈 수 보존')
            for se,ex in zip(series,expected['series']):
                values=[float(v.text) for v in se.findall('c:val//c:pt/c:v',NS)]
                check(values==ex['values'],'PPT 차트 데이터와 생성 계약 동일')
            if expected['slide'] in [6,7,8]:
                va=cr.find('.//c:valAx',NS)
                check(va.find('c:scaling/c:min',NS).get('val')=='0' and va.find('c:scaling/c:max',NS).get('val')=='100','막대차트 0–100축')
            check(cr.find('c:externalData',NS) is not None,'차트 데이터 편집용 워크북 연결')
        raw_single=[data['single'][i]['map50_95'] for i in range(11)]
        displayed_chart=chart_manifest[0]['series'][0]['values']
        check(all(f'{x:.2f}'==f'{y:.2f}' for x,y in zip(raw_single,displayed_chart)),'원정밀도와 차트 표시값 2자리 동일')
        check(all(abs(x-y)<1e-11 for x,y in zip(raw_single,displayed_chart)),'차트 워크북 정밀도 변환 오차 범위')
        hroot=ET.fromstring(z.read('ppt/slides/slide9.xml'))
        rows=hroot.findall('.//a:tbl/a:tr',NS)
        check(len(rows)==12,'히트맵 헤더와 전체 단일 필터 11행')
        for r in range(11):
            cells=rows[r+1].findall('a:tc',NS)
            for c in range(3):
                actual=''.join(t.text or '' for t in cells[c+1].findall('.//a:t',NS))
                check(actual==f'{data["noise"][r][c]:.1f}',f'히트맵 {r+1}행 {c+1}열 원정밀도 1회 반올림')
        check(source['rounding_corrected']=={'Otsu Threshold/noise80':'76.6','Histogram Equalization/noise40':'88.1','Sobel Edges/noise80':'71.1'},'기존 이중 반올림 3칸 교정')
        check(len([x for x in z.namelist() if x.endswith('.xlsx')])==5,'차트별 데이터 워크북 5개')
        # 원본 마크와 실험 입력 이미지를 바이트 단위로 대조합니다.
        media_hashes={hashlib.sha256(z.read(x)).hexdigest() for x in z.namelist() if '/media/' in x}
        for src in [ROOT/'work/brand/kyonggi_signature.png',Path(r'D:\2026\추계학술대회\DataSet\images\train\1001.png')]:
            check(hashlib.sha256(src.read_bytes()).hexdigest() in media_hashes, '원본 이미지 바이트 보존: '+src.name)
    check(len(list((ROOT/'work/render').glob('slide-??.png')))==15,'슬라이드 15장 렌더 존재')
    receipt=read_json(ROOT/'evidence/finalizer.validation.json')
    check(receipt.get('packageIntegrity',{}).get('status')=='pass' and receipt.get('firstPartyImport',{}).get('passed') is True and receipt.get('nativeChartValidation',{}).get('passed') is True,'공식 finalizer 통과')
    report={'ok':True,'check_count':len(checks),'checks':checks,'limitations':['실제 발표 소요 시간은 리허설 미실시','Microsoft PowerPoint에서 실제 편집·재저장 동작은 미검사'],'pptx_sha256':hashlib.sha256(deck.read_bytes()).hexdigest()}
    (ROOT/'evidence/build_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'ok':True,'check_count':len(checks),'pptx_sha256':report['pptx_sha256']},ensure_ascii=False))
except Exception as e:
    (ROOT/'evidence/build_checks.json').write_text(json.dumps({'ok':False,'error':str(e),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'ok':False,'error':str(e),'completed_check_count':len(checks)},ensure_ascii=False))
    sys.exit(1)
