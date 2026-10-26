import ast
import csv
import hashlib
import json
import pathlib
import statistics
from collections import defaultdict

import numpy as np

# 이 검사는 보고서의 근거와 완결성을 검증하며 논문 제출을 승인하지 않습니다.
ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = '9328b43ab033f7fef1bc8d43fb6ba8a58b525b4b0663301e659d53697c700a27'
audit = json.loads((ROOT / 'audit.json').read_text(encoding='utf-8'))
report = (ROOT / '최종검증보고서.txt').read_text(encoding='utf-8')
evidence = ROOT / 'work/evidence'
calc = json.loads((evidence / 'recalculated.json').read_text(encoding='utf-8'))
actual = json.loads((evidence / 'container_dataset.json').read_text(encoding='utf-8-sig'))
main = json.loads((ROOT / 'evidence/main_findings.json').read_text(encoding='utf-8'))
paragraphs = json.loads((evidence / 'hwp_paragraphs.json').read_text(encoding='utf-8'))
source_text = '\n'.join(paragraphs)
checks = audit['checks']
assert len(checks) == 10 and [item['id'] for item in checks] == list(range(1, 11))
assert audit['paper_ready_for_submission'] is False
assert '\ufffd' not in report and '\ufffd' not in json.dumps(audit, ensure_ascii=False)
for item in checks:
    assert item['status'] in {'PASS', '주의', '수정필요', '확인불가'}
    assert all(item[field] for field in ['name', 'original_quote', 'finding', 'evidence', 'recommended_action', 'limitation'])
    assert f"{item['id']:02}. [{item['status']}]" in report
assert hashlib.sha256(pathlib.Path(audit['source_path']).read_bytes()).hexdigest() == EXPECTED == audit['source_sha256']
for relative, expected_hash in audit['evidence_sha256'].items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected_hash, relative
for source, expected_hash in audit['original_data_sources_sha256'].items():
    assert hashlib.sha256(pathlib.Path(source).read_bytes()).hexdigest() == expected_hash, source


def rows(path):
    with pathlib.Path(path).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


data_root = pathlib.Path(next(path for path in audit['original_data_sources_sha256'] if pathlib.Path(path).name == 'results_summary.json')).parent
summary = json.loads((data_root / 'results_summary.json').read_text(encoding='utf-8'))
sweep = json.loads((data_root / 'sweep_results.json').read_text(encoding='utf-8'))
by_name = {row['name']: row for row in [summary['baseline']] + summary['round1'] + summary['round2']}
done = []

# 1. 연구 범위의 문구와 실제 실험 후보를 대조합니다.
assert len(summary['round1']) == 10 and len(summary['round2']) == 5
assert '실제 현장의 모든 촬영 조건을 포괄하는 것은 아니다' in source_text
assert '고정된 모델의 미지 촬영 조건에 대한 적응성을 검증한 것은 아니다' in source_text
done.append(1)

# 2. 영상별 누락·추가 검출에서 엄격 정확도를 다시 계산합니다.
single = defaultdict(list)
for row in rows(data_root / 'per_image_predictions.csv'):
    single[row['method']].append(row)
assert sum(map(len, single.values())) == 8000 and len(single) == 16
for name, items in single.items():
    assert len(items) == len({row['key'] for row in items}) == 500
    value = 100 * sum(int(row['miss']) == 0 and int(row['extra']) == 0 for row in items) / len(items)
    assert abs(value - by_name[name]['strict_acc']) < 1e-8
done.append(2)

# 3. 반복 결과의 표본 표준편차를 독립적으로 재계산합니다.
multi = defaultdict(list)
for row in rows(data_root / 'ms_per_image.csv'):
    multi[(row['condition'], int(row['seed']), row['method'])].append(row)
assert sum(map(len, multi.values())) == 19500 and len(multi) == 39
repeat = defaultdict(lambda: defaultdict(list))
for row in rows(data_root / 'ms_run_results.csv'):
    key = (row['condition'], int(row['seed']), row['method'])
    items = multi[key]
    assert len(items) == len({item['key'] for item in items}) == 500
    strict = 100 * sum(int(item['miss']) == 0 and int(item['extra']) == 0 for item in items) / 500
    assert abs(strict - float(row['strict_acc'])) < 1e-8
    repeat[(row['condition'], row['method'])]['strict_acc'].append(strict)
    repeat[(row['condition'], row['method'])]['map50_95'].append(float(row['map50_95']))
for item in calc['repeat']:
    values = repeat[(item['condition'], item['method'])]
    for metric in ['strict_acc', 'map50_95']:
        assert abs(statistics.mean(values[metric]) - item[metric]['mean']) < 1e-10
        assert abs(statistics.stdev(values[metric]) - item[metric]['sample_sd']) < 1e-10
done.append(3)

# 4. 조합과 더 좋은 구성 필터의 원정밀도 차이를 확인합니다.
assert len(calc['combinations']) == 5
for item in calc['combinations']:
    for metric in ['map50_95', 'strict_acc']:
        best = max(by_name[name][metric] for name in item['components'])
        assert abs(by_name[item['method']][metric] - best - item[metric]['delta_pp']) < 1e-10
    assert item['map50_95']['delta_pp'] < 0
done.append(4)

# 5. 실제 영상 재검사 근거와 분할 누출의 보고가 일치하는지 확인합니다.
assert actual['dataset_count'] == 500 and actual['groups'] == 368 and actual['similar_pairs'] == 154
assert actual['image_sizes'] == {'2944x2352': 500}
assert actual['split_counts'] == {'train': 400, 'val': 100}
assert len(calc['splits']) == 15 and all(item['outer_group_overlap'] == 0 for item in calc['splits'])
assert min(item['inner_group_overlap'] for item in calc['splits']) == 9
assert max(item['inner_group_overlap'] for item in calc['splits']) == 20
assert checks[4]['status'] == '주의'
done.append(5)

# 6. 저장된 실제 학습 설정 표본을 본문 설정과 대조합니다.
expected_args = {'model': 'yolov8n.pt', 'epochs': 30, 'imgsz': 1280, 'batch': 8, 'patience': 15,
                 'seed': 42, 'flipud': 0.5, 'fliplr': 0.5, 'scale': 0.3, 'translate': 0.1, 'hsv_v': 0.4}
assert len(actual['args_samples']) == 3
for item in actual['args_samples']:
    assert all(item['settings'][key] == value for key, value in expected_args.items())
assert all(item['oversample_factor'] == 1 for item in calc['splits'])
done.append(6)

# 7. 실제 대응 함수를 격리하여 경계 상황을 다시 실행합니다.
scope = {'np': np}
for node in ast.parse((evidence / 'notebook_cell_30.py').read_text(encoding='utf-8')).body:
    if isinstance(node, ast.FunctionDef) and node.name == 'ball_match_stats':
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'original_metric_function', 'exec'), scope)
function = scope['ball_match_stats']
tests = [([[10, 10, 4, 4]], [[10, 10, 4, 4]], [0.8], (0, 0)),
         ([[10, 10, 4, 4]], [], [], (1, 0)),
         ([[10, 10, 4, 4]], [[10, 10, 4, 4], [10.1, 10, 4, 4]], [0.8, 0.7], (0, 1)),
         ([[10, 10, 4, 4]], [[12, 10, 4, 4]], [0.8], (0, 0)),
         ([[10, 10, 4, 4]], [[12.01, 10, 4, 4]], [0.8], (1, 1)),
         ([], [[10, 10, 4, 4]], [0.8], (0, 1))]
for gt, prediction, confidence, expected in tests:
    value = function(gt, prediction, confidence)
    assert (value['miss'], value['extra']) == expected
done.append(7)

# 8. 그림 메타데이터를 원정밀도 값과 대조하여 세 표시 오류를 재현합니다.
labels = json.loads((ROOT / 'evidence/BIN0003.png.metadata.json').read_text(encoding='utf-8'))['visible_text'][:33]
differences = []
for index, item in enumerate([summary['baseline']] + summary['round1']):
    values = [item['map50_95']]
    for level in ['40', '80']:
        name = f'Noise std={level}' if index == 0 else f"{item['name']} | noise {level}"
        values.append(next(row['map50_95'] for row in sweep['grid'][level] if row['name'] == name))
    for column, value in enumerate(values):
        if labels[index * 3 + column] != f'{value:.1f}':
            differences.append((item['name'], [0, 40, 80][column], labels[index * 3 + column], f'{value:.1f}'))
assert differences == [('Otsu Threshold', 80, '76.7', '76.6'),
                       ('Histogram Equalization', 40, '88.0', '88.1'),
                       ('Sobel Edges', 80, '71.0', '71.1')]
assert checks[7]['status'] == '수정필요'
done.append(8)

# 9. 편집 문제와 참고문헌 확인의 근거를 확인합니다.
assert 'ITTP-2024-00436954' in source_text
assert all(text in source_text for text in ['입력에적합', '후에도검출', '조합이유리'])
assert sum('Emboss' in text and '82.86' in text and '79.60' in text for text in paragraphs) == 2
assert len(main['references']) == 3 and all(item['status'] == '확인' for item in main['references'])
assert checks[8]['status'] == '수정필요'
done.append(9)

# 10. 서식·그림 해상도와 전체 조판 미확인 한계를 보존합니다.
assert abs(main['image_geometry'][0]['dpi_x'] - 96) < 0.1
assert not main['visual_review']['full_document_render_verified']
assert not main['visual_review']['page_count_verified']
assert checks[9]['status'] == '확인불가'
assert '전체 페이지 렌더' in report and '3쪽' in report
done.append(10)

assert done == list(range(1, 11))
print(json.dumps({'검사': '검증보고서 근거·완결성 검사', '통과항목': len(done), '전체항목': 10,
                  '원본보존': True, '논문제출가능': False, '판정집계': audit['status_counts'],
                  '검사통과의미': '보고서의 검사 통과이며 논문 제출 승인이 아닙니다.'}, ensure_ascii=False))
