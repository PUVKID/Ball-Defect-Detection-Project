import ast
import json
import pathlib

import numpy as np

# 실제 중심점 대응 함수를 추출하여 경계 상황 여섯 가지를 검증합니다.
here = pathlib.Path(__file__).resolve().parent
source = (here / 'notebook_cell_30.py').read_text(encoding='utf-8')
scope = {'np': np}
for node in ast.parse(source).body:
    if isinstance(node, ast.FunctionDef) and node.name == 'ball_match_stats':
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'original_ball_match_stats', 'exec'), scope)
match = scope['ball_match_stats']
cases = [
    ('정상 일대일 대응', [[10, 10, 4, 4]], [[10, 10, 4, 4]], [0.8], (0, 0)),
    ('전체 누락', [[10, 10, 4, 4]], [], [], (1, 0)),
    ('중복 예측은 추가 검출', [[10, 10, 4, 4]], [[10, 10, 4, 4], [10.1, 10, 4, 4]], [0.8, 0.7], (0, 1)),
    ('허용 거리 경계 포함', [[10, 10, 4, 4]], [[12, 10, 4, 4]], [0.8], (0, 0)),
    ('허용 거리 초과', [[10, 10, 4, 4]], [[12.01, 10, 4, 4]], [0.8], (1, 1)),
    ('주석 없는 영상의 예측', [], [[10, 10, 4, 4]], [0.8], (0, 1)),
]
report = []
for name, gt, prediction, confidence, expected in cases:
    result = match(gt, prediction, confidence)
    assert (result['miss'], result['extra']) == expected
    report.append({'name': name, 'expected_miss_extra': expected, 'actual': result, 'passed': True})
definitions = {
    'strict_formula': '100 * count(miss == 0 and extra == 0) / n_images',
    'center_matching': '모든 주석-예측 쌍을 중심 거리 오름차순으로 정렬한 탐욕적 일대일 대응',
    'distance_tolerance': 'tol_frac=0.5 * max(gt_width, gt_height)',
    'predict_thresholds': {'confidence': 0.25, 'nms_iou': 0.5},
    'ap_thresholds': {'confidence': 0.001, 'nms_iou': 0.7},
    'map_aggregation': '외부 평가 폴드의 v.box.map을 100배 한 뒤 폴드 간 산술평균',
    'source': '원본 notebook.ipynb 셀 18, 30; 3차 HWP 2.4절',
    'scope': '함수 경계검사와 저장된 수치 대조이며 모델 추론/AP 재평가가 아님',
}
(here / 'metric_code_checks.json').write_text(json.dumps({'cases': report, 'definitions': definitions}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'metric_function_cases': len(report), 'passed': len(report), 'model_inference_executed': False}, ensure_ascii=False))
