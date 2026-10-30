import hashlib
import json
import pathlib
from collections import Counter

# 검증 결과를 제출 승인과 구별하여 기록합니다. 원본 논문이나 연구 결과를 수정하지 않습니다.
ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = pathlib.Path('C:/Users/PUVKID/Desktop/2026/추계학술대회/논문/3차/추계학술대회 논문 3차.hwp')
EXPECTED = '9328b43ab033f7fef1bc8d43fb6ba8a58b525b4b0663301e659d53697c700a27'
E = ROOT / 'work/evidence'
calc = json.loads((E / 'recalculated.json').read_text(encoding='utf-8'))
actual = json.loads((E / 'container_dataset.json').read_text(encoding='utf-8-sig'))
main = json.loads((ROOT / 'evidence/main_findings.json').read_text(encoding='utf-8'))
metric = json.loads((E / 'metric_code_checks.json').read_text(encoding='utf-8'))
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED == main['source_sha256']


def check(number, name, status, quote, finding, evidence, action, limit):
    return {'id': number, 'name': name, 'status': status, 'original_quote': quote,
            'finding': finding, 'evidence': evidence, 'recommended_action': action, 'limitation': limit}


checks = [
    check(1, '연구 질문·비교 범위·결론의 정합성', 'PASS',
          '본 연구의 영상 조건은 일반 영상과 합성 가우시안 잡음 조건으로 한정되며, 실제 현장의 모든 촬영 조건을 포괄하는 것은 아니다.',
          '제목과 초록, 서론 및 결론이 단일 필터 10종·순차 조합 5종의 볼 검출 비교를 일관되게 다룹니다. OK/NG 분류 정확도를 주 결과로 혼동하지 않았습니다. 일반 영상 전체 필터 비교와 잡음 조건의 Original·단일 필터 비교를 구별하고, 모든 필터가 항상 우수하다는 결론을 내리지 않았습니다. 조건마다 재학습한 실험이라는 한계도 2.3절과 결론에 명시되어 있습니다.',
          ['work/evidence/hwp_text.txt:009,011,016,021,023,024,048,049', '원본 notebook.ipynb 셀28·30·53·71'],
          '현재의 범위 제한 문구를 유지하십시오. 실험하지 않은 역순·모든 조합·미지 현장 적응 성능으로 결론을 넓히지 마십시오.',
          '실제 현장별 일반화 성능을 새로 측정한 검증은 아닙니다.'),
    check(2, '일반·잡음 결과의 수치와 영상별 행 재계산', 'PASS',
          'Gamma 0.3이 96.70%로 가장 높았다. ... Original과의 차이는 0.17%p였다.',
          '일반 영상 16조건×500장=8,000행에서 누락·추가 검출이 모두 0인 비율을 다시 계산해 엄격 정확도 16개를 확인했습니다. 반복 실험 39조건×500장=19,500행도 같은 방식으로 확인했습니다. 총 27,500행의 저장 결과와 요약이 일치합니다. 잡음 40·80의 22개 CSV 요약은 JSON 원정밀도와 소수 둘째 자리 허용 오차 내 일치합니다. 본문의 Original 96.53, Gamma 96.70, 차이 0.17%p, Otsu 60.46, Gaussian Blur 93.37·88.79·82.94 및 Emboss 96.06·0.87·0.08은 원자료와 일치합니다. 단일 필터 10종 중 9종이 일반 영상 mAP50-95 93.37% 이상이라는 진술도 맞습니다.',
          ['work/evidence/recalculated.json', '원자료/per_image_predictions.csv', '원자료/ms_per_image.csv', '원자료/results_summary.json', '원자료/sweep_results.json', 'work/evidence/hwp_text.txt:033,034,038,039,042,043'],
          '본문의 주요 수치는 유지할 수 있습니다. 그림의 표시 반올림 문제는 8번에서 별도로 수정하십시오.',
          'mAP는 저장된 요약과 대조했습니다. 원시 박스 예측으로 AP를 새로 적분하거나 모델 추론을 다시 실행하지 않았습니다. 저장 행의 엄격 정확도를 재집계한 검증과 AP 재평가를 혼동하지 않습니다.'),
    check(3, '세 시드 평균·표본 표준편차·반복 해석', 'PASS',
          'Invert+CLAHE의 엄격 검출 정확도는 95.47±2.27%, Original은 95.40±0.53% ... 평균 차이는 0.07%p였다.',
          '시드 42·43·44의 결과에서 표본 표준편차(n−1)를 다시 계산했습니다. 일반 영상 Invert+CLAHE의 엄격 정확도 95.4667±2.2745, Original 95.4000±0.5292, mAP50-95 95.8206±0.1088 대 96.6467±0.1524로 본문 표시가 맞습니다. 잡음 80의 Gaussian Blur mAP50-95는 82.8607±0.0824, Original은 79.5974±0.2607이며 세 시드 모두 Gaussian Blur가 높습니다. Gamma 0.3의 일반 영상 결과는 반복 평가 대상이 아니라는 설명도 실제 MS_CONDITIONS와 맞습니다.',
          ['work/evidence/recalculated.json:repeat', '원자료/ms_run_results.csv', '원본 notebook.ipynb 셀71', 'work/evidence/hwp_text.txt:028,033,040,043,048'],
          '평균±표본 표준편차 및 안정적 우월성을 단정하지 않는 현재 문구를 유지하십시오.',
          'n=3이며 시드별 분할·학습 난수·잡음 실현이 함께 변합니다. 표본 표준편차는 신뢰구간이나 유의확률이 아닙니다. 전체 후보의 통계적 최적성은 확인하지 않았습니다.'),
    check(4, '순차 조합 구성과 더 좋은 단일 구성 필터 대비 비교', 'PASS',
          '일반 영상에서 평가한 5개 복합 필터의 mAP50-95는 각각 구성 필터 중 더 우수한 단일 필터를 넘지 못하였다.',
          '원본 ROUND2_COMBOS의 A→B 순서와 본문 이름이 일치합니다. 더 좋은 구성 필터 대비 mAP 차이는 Invert+CLAHE −0.2239, Blur+Otsu −33.7884, Sobel+Invert −0.7208, HistEq+Emboss −0.8443, Unsharp+Sobel −1.7033%p로 모두 음수입니다. 엄격 정확도 차이는 순서대로 +1.6, −40.2, −2.8, +0.4, −3.8%p로 본문과 일치합니다. 지표에 따라 조합의 장단점이 달라지는 해석이 타당합니다.',
          ['work/evidence/recalculated.json:combinations', '원본 notebook.ipynb 셀26·28', 'work/evidence/hwp_text.txt:021,038,039'],
          '조합이 무조건 우수하다는 문구를 추가하지 말고 현재의 구성 필터 대비 비교를 유지하십시오.',
          '검사한 다섯 순서만 해당합니다. 역순, 세 필터 이상 조합, 조합의 잡음 조건 성능을 검증한 것은 아닙니다.'),
    check(5, '데이터 구성·교차검증·유사 영상 누출', '주의',
          '다만 내부 학습·검증 분할에서는 9~20개의 유사 영상 그룹이 중복되어, 내부 검증 자료의 그룹 수준 독립성은 완전히 확보되지 않았다.',
          '실행 중인 연구 컨테이너를 읽기만 하여 train 400장·val 100장, 모두 2944×2352화소, 볼 주석 6270개를 확인했습니다. 원본 find_dup_groups를 실제 영상에 다시 실행해 유사 쌍 154개·그룹 368개를 얻었고 과거 group_map 500키와 모두 일치했습니다. 원본 assign_folds와 fold_split을 시드 세 개×5폴드로 재실행한 결과 학습 359~361장·내부 검증 40장·외부 평가 99~101장, 외부 그룹 중복 0, 내부 그룹 중복 9~20개가 확인됩니다. 이미 본문이 이 한계를 솔직하게 기재하므로 숫자 오류는 아니지만, best.pt 선택·조기 종료에 사용되는 내부 검증의 독립성 제한은 남습니다.',
          ['work/evidence/container_dataset.json', 'work/evidence/recalculated.json:dataset,splits', '원본 notebook.ipynb 셀14·30', 'work/evidence/hwp_text.txt:019,049'],
          '이번 원고의 한계 고지는 유지하십시오. 연구를 강화하려면 내부 검증도 그룹 단위로 분리한 뒤 재학습·재평가하고, 촬영 로트별 독립 시험 자료를 추가해야 합니다.',
          '128×128 영상의 평균 절대차 기준으로 찾은 유사성만 검사했습니다. 그룹 분리만으로 모든 촬영 조건·로트·배경의 독립성이 증명되는 것은 아닙니다. 이번에는 재학습하지 않았습니다.'),
    check(6, '학습·전처리 파라미터와 실제 코드·저장 설정', 'PASS',
          '공통 학습 설정은 최대 30에폭, 입력 크기 설정 1,280, 배치 크기 8, 조기 종료 patience 15였다.',
          '본문의 YOLOv8n, 30에폭, 1280, 배치 8, patience 15와 지정 증강 다섯 값은 교차검증 학습 함수와 일치합니다. 컨테이너의 args.yaml 표본 3개에서도 직접 확인했습니다. CLAHE clip 40·16×16, Gamma 0.3, Gaussian sigma 20·kernel 121×121, Emboss gain 4, Unsharp amount 8·sigma 2가 FILTER_SPECS와 구현에 맞습니다. 잡음은 8비트 영상에 더한 뒤 [0,255]로 제한하고 필터보다 먼저 적용하며 학습·검증·평가에 같은 조건을 구성합니다. 원본의 별도 기초 학습 셀 EPOCHS=100과 논문에 사용한 교차검증 FILTER_EPOCHS=30도 구별했습니다. 오버샘플링 옵션은 켜져 있으나 이번 전체 자료 조건의 15분할에서 실제 배수가 모두 1이므로 학습 영상 수 설명과 충돌하지 않습니다.',
          ['work/evidence/notebook_cell_16.py', 'work/evidence/notebook_cell_26.py', 'work/evidence/notebook_cell_28.py', 'work/evidence/notebook_cell_30.py', 'work/evidence/notebook_cell_71.py', 'work/evidence/container_dataset.json:args_samples', '원자료/results_summary.json:environment,cv'],
          '현재 파라미터 설명을 유지할 수 있습니다. 재현성 보완을 원하면 잡음의 uint8 변환과 실제 사용한 주요 기본 증강값을 추가할 수 있습니다.',
          'args.yaml은 존재하는 305개 중 Blur+Otsu 폴드 0~2의 세 표본을 직접 열었습니다. 모든 학습 실행의 전 로그·가중치·환경을 재구축한 검증은 아닙니다. RTX 4090·라이브러리 버전은 당시 저장 환경 기록과 대조했습니다.'),
    check(7, 'mAP·엄격 검출 정확도의 정의와 구현', 'PASS',
          '주석 중심과 예측 중심 사이의 거리가 가까운 순서로 일대일 대응시키고, 허용 거리는 각 주석 상자의 긴 변 길이의 0.5배로 설정하였다.',
          '실제 ball_match_stats는 모든 중심 거리 쌍을 정렬하여 탐욕적으로 일대일 대응하고 max(width,height)×0.5 허용 거리를 적용합니다. miss=extra=0인 영상의 비율이라는 정의가 코드와 일치합니다. 정상 대응·전체 누락·중복 예측·허용 거리 경계·거리 초과·주석 없는 영상 등 여섯 사례를 실제 함수로 실행하여 모두 통과했습니다. 엄격 정확도 추론(conf 0.25/NMS IoU 0.5)과 AP 평가(conf 0.001/NMS IoU 0.7)가 다르고, 폴드별 v.box.map의 산술평균을 보고한다는 본문도 구현과 일치합니다.',
          ['work/evidence/metric_code_checks.json', 'work/evidence/check_metrics_code.py', '원본 notebook.ipynb 셀18·30', 'work/evidence/hwp_text.txt:026,027'],
          '두 지표의 단위·대응 기준·추론 임계값이 다르다는 설명을 유지하십시오.',
          '여섯 합성 경계 사례와 저장된 행을 확인했습니다. 모든 가능한 대응 배치에 대한 완전 검증 또는 AP 재평가를 의미하지 않습니다.'),
    check(8, '삽입 그림과 원자료 수치·표시 정밀도', '수정필요',
          '그림 3. 가우시안 잡음 표준편차별 단일 필터의 mAP50-95',
          '그림 3의 33칸을 원정밀도 JSON과 대조하자 세 칸에서 소수 첫째 자리 표시가 다릅니다. Otsu/noise80은 76.648855→76.6인데 그림 76.7, Histogram Equalization/noise40은 88.053190→88.1인데 그림 88.0, Sobel/noise80은 71.052420→71.1인데 그림 71.0입니다. PNG 메타데이터와 실제 픽셀의 값이 같음도 확인했습니다. 원본 results_to_df()가 두 자리로 반올림한 CSV를 만들고 논문 그림 코드가 이를 한 자리로 다시 표시하는 경로가 원인입니다. 차이는 각 0.1%p로 필터 순위나 본문의 주요 결론을 바꾸지는 않습니다. 그림 2의 여섯 막대 표시는 원정밀도 직접 반올림과 일치합니다.',
          ['work/evidence/figure_rounding.json', 'evidence/BIN0002.png.metadata.json', 'evidence/BIN0003.png.metadata.json', '원본 notebook.ipynb 셀32 results_to_df', '기존 work/paper_filter_figures.py:49~60', '원자료/sweep_results.json', 'main의 삽입 그림 픽셀 대조'],
          '그림 3의 세 값을 각각 76.6, 88.1, 71.1로 교정하십시오. 재생성 시 CSV의 반올림 수치 대신 JSON 원정밀도 값을 읽고 최종 표시 단계에서 한 번만 반올림하십시오.',
          '이번 요청은 검증이므로 기존 그래프 코드·논문·결과를 수정하지 않았습니다. 그림 1은 BMP로 변환되어 메타데이터가 없으므로 모든 숫자의 기계적 동일성을 별도로 보증하지 않습니다.'),
    check(9, '문장·국영문 초록·참고문헌·사사', '수정필요',
          'Emboss는 일반 영상 96.06%에서 잡음 40·80의 0.87%·0.08%로 감소하여 입력 변화에 민감했다. ...',
          '그림 3 직전의 상세 단락과 그림 3 직후의 짧은 단락이 Emboss와 noise80 반복 수치를 중복 서술합니다. 뒤의 짧은 단락은 삭제하는 것이 좋습니다. 서론의 입력에적합·후에도검출·조합이유리에는 띄어쓰기가 필요합니다. 첫 쪽 사사 ITTP-2024-00436954는 동일 번호를 인용한 공식 학회 원문의 IITP-2024-00436954와 기관 약어가 다릅니다. 협약서 또는 연구실 공식 문구와 대조한 뒤 정정해야 합니다. 국문·영문 초록의 후보 수, 비교 범위, 주요 수치 및 조건별 재학습 설명은 일치합니다. 참고문헌 [1]의 소프트웨어 저자·2023, [2]의 저자·1994·474~485쪽, [3]의 제목·arXiv 번호·2019는 원본·공식 자료에서 확인되었습니다.',
          ['work/evidence/hwp_text.txt:007,009,011,016,043,046,051~053', 'evidence/main_findings.json:editing_findings,references,funding_limit'],
          '그림 3 뒤의 반복 단락을 삭제하고, 입력에 적합/후에도 검출/조합이 유리로 교정하십시오. 과제 문구 확인 후 ITTP→IITP를 검토하십시오. 참고문헌 [1]에 공식 URL과 실사용 버전을 덧붙이면 재현성에 도움이 됩니다.',
          '사사 과제의 실제 수혜·연도 적정성, 저자 영문명·전자우편·ORCID 소유권은 연구진 확인이 필요합니다. RS-2020-NR049579 및 2024년 교육부 문구는 공식 학회 원문에도 있어 임의로 오류라고 단정하지 않았습니다.'),
    check(10, '표준 서식 속성·2단·그림 가독성·전체 페이지', '확인불가',
          '본문 2단, 그래프만 굵게, 제공한 표준 논문 서식 유지 요청',
          'HWP 내부 속성에서 용지 190×260mm, 좌우 약20mm·위아래 약17.5mm, 본문 2단과 제목·초록 영역 1단을 확인했습니다. 국문 제목 휴먼명조17pt, 영문 제목 한양견명조15pt, 저자 돋움11pt, 본문 휴먼명조10pt·장평90·자간−6, 캡션 한양중고딕9pt이며 문서의 비어 있지 않은 문단에서 참조하는 글자모양은 모두 일반 굵기입니다. 그림 2·3 메타데이터의 72개 텍스트는 NanumGothic Bold이고 추출 그림 자체에서 명확한 겹침은 발견하지 않았습니다. 다만 그림 1은 268×351픽셀 BMP를 약70.91×92.92mm로 삽입해 실제 약96dpi로 낮습니다. 그림 2·3은 약561·525dpi입니다. 저장된 첫 쪽 미리보기와 내장 그림만 시각적으로 확인했고 전체 HWP 페이지 렌더링 및 실제 3쪽 충족 여부는 확인하지 못했습니다.',
          ['evidence/main_findings.json:image_geometry,visual_review,document_typography', 'evidence/main_layout_details.json', 'work/first_page_preview.png', 'work/BIN0001.bmp.png', 'work/BIN0002.png.png', 'work/BIN0003.png.png'],
          '그림 1은 확대 보간한 현재 BMP 대신 고해상도 원본 PNG로 다시 삽입하십시오. 수정 후 한글의 인쇄 미리보기 또는 PDF 내보내기로 전체 쪽수를 확인하고 모든 쪽의 좌우 단·그림·캡션·바닥글 잘림과 겹침을 확인해야 합니다.',
          '현재 원본 표준양식 파일의 옛 경로는 없어 완전한 일대일 비교를 할 수 없었습니다. 확인한 HWP 속성과 기존 필수 규격에 근거했습니다. 첫 쪽 캐시·그림 단독 검사는 전체 조판·고아줄·3쪽 분량 검증을 대신하지 않습니다.'),
]

files = [E / name for name in ['hwp_text.txt', 'hwp_paragraphs.json', 'recalculated.json', 'container_dataset.json',
                              'metric_code_checks.json', 'figure_rounding.json', 'recompute_saved.py',
                              'container_readonly.py', 'check_metrics_code.py']]
files += [ROOT / 'evidence/main_findings.json', ROOT / 'evidence/main_layout_details.json',
          ROOT / 'evidence/BIN0002.png.metadata.json', ROOT / 'evidence/BIN0003.png.metadata.json',
          ROOT / 'tools/check_review.py']
assert all(path.is_file() for path in files)
manifest = {str(path.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
counts = dict(Counter(item['status'] for item in checks))
report = {'confirmed_date_kst': '2026-10-20', 'session': '01a1351a-a311-70c0-a679-69c8f5da679d',
          'task': 'paper3-final-audit-20261020', 'source_path': str(SOURCE), 'source_sha256': EXPECTED,
          'source_preserved': True, 'repair_used': 1,
          'verification_design': '동일 문서 열 번 반복이 아닌 서로 다른 근거를 이용한 10개 검증',
          'paper_ready_for_submission': False,
          'verdict': '현재 파일은 수정 및 전체 페이지 확인 후 제출 판단이 필요합니다. 주요 수치와 제한된 연구 결론은 원자료·코드와 일치하지만, 그림3 반올림 표시 3칸, 중복 단락·사사 약어 확인, 그림1 저해상도 문제를 처리하고 전체 조판을 확인해야 합니다.',
          'status_counts': counts, 'checks': checks,
          'executed_scope': {'raw_image_rows_recalculated': 27500, 'normal_methods': 16, 'multiseed_runs': 39,
                             'noise_summaries_checked': 22, 'split_recalculations': 15,
                             'actual_dataset_images_read': actual['dataset_count'], 'actual_duplicate_groups': actual['groups'],
                             'actual_duplicate_pairs': actual['similar_pairs'], 'metric_function_cases': len(metric['cases']),
                             'training_args_samples_read': len(actual['args_samples']), 'training_rerun': False,
                             'model_inference_rerun': False, 'ap_recomputed': False, 'full_hwp_pages_rendered': False},
          'evidence_sha256': manifest, 'original_data_sources_sha256': calc['sources_sha256'],
          'reference_sources': main['references'], 'funding_sources': main['editing_findings'][1]['sources'],
          'tool_validation_meaning': 'check_review.py의 종료코드0은 검증 보고서의 완결성·근거 일치·원본 보존 검사가 통과했다는 뜻입니다. 논문 자체의 제출 승인이나 무오류 보장이 아닙니다.'}
(ROOT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

lines = ['추계학술대회 논문 3차 최종 검증 보고서', '확인일: 2026-10-20 (한국 시각)',
         '대상: ' + str(SOURCE), '원본 SHA-256: ' + EXPECTED,
         '원본과 연구 코드·결과는 수정하지 않았습니다.', '', '제출 판단', report['verdict'],
         '판정 집계: PASS 6개 / 주의 1개 / 수정필요 2개 / 확인불가 1개',
         '같은 검사를 열 번 반복한 것이 아니라 아래의 서로 다른 10항목을 검증했습니다.', '',
         '우선 처리 사항',
         '1. 그림3: Otsu/noise80 76.7→76.6, HistEq/noise40 88.0→88.1, Sobel/noise80 71.0→71.1. JSON 원정밀도에서 한 번만 반올림하십시오.',
         '2. 그림3 뒤의 Emboss·noise80 결과 반복 단락을 삭제하십시오. 앞선 상세 단락은 유지합니다.',
         '3. 그림1은 약96dpi입니다. 고해상도 원본 PNG로 다시 삽입하십시오.',
         '4. 사사 ITTP는 공식 동일 과제번호 표기의 IITP와 다릅니다. 협약서·공식 사사와 대조한 뒤 정정하십시오. 서론 띄어쓰기도 교정하십시오.',
         '5. 수정본 전체를 PDF로 내보내거나 한글 인쇄 미리보기에서 실제 3쪽·2단·잘림·겹침을 확인하십시오. 이번 검증은 전체 페이지 렌더 확인을 완료하지 못했습니다.', '',
         '수치 검증의 범위',
         '저장된 영상별 27,500행 재집계, 잡음 조건 요약22개 대조, 15개 분할 재계산, 실제 영상500장의 유사그룹 재구성, 학습 args.yaml 3개 직접 확인, 지표 함수6개 경계 사례 검사를 수행했습니다.',
         '엄격 정확도는 누락·추가 검출 행에서 다시 계산했습니다. mAP는 저장된 평가 요약과 대조했으며 모델 재학습·재추론·AP 재산출은 하지 않았습니다.', '']
for item in checks:
    lines += [f"{item['id']:02}. [{item['status']}] {item['name']}", '원문/요구: ' + item['original_quote'],
              '확인 결과: ' + item['finding'], '근거: ' + '; '.join(item['evidence']),
              '수정안/유지 사항: ' + item['recommended_action'], '범위 한계: ' + item['limitation'], '']
lines += ['공식·원본 참고 경로']
for source in main['references']:
    lines += [f"[{source['id']}] {source['url']}"]
lines += ['동일 사사 과제번호의 공식 출판 표기:', *report['funding_sources'], '',
          '검사 기록과 한계',
          '원본 해시·근거 파일 해시·10항목 판정·재계산 결과는 audit.json 및 work/evidence에 기록했습니다.',
          report['tool_validation_meaning'],
          '이 보고서는 제출 전 검토 자료입니다. 원본 전체 조판 확인 및 연구진의 사사·저자 정보 확인이 남아 있습니다.', '']
(ROOT / '최종검증보고서.txt').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'checks': len(checks), 'counts': counts, 'paper_ready_for_submission': False, 'source_preserved': True}, ensure_ascii=False))
