import ast
import contextlib
import glob
import hashlib
import io
import json
import os
import pathlib
from collections import Counter, defaultdict

import cv2
import numpy as np
import yaml

# 읽기 전용으로 원본 영상과 학습 설정 파일을 확인합니다. 모델을 불러오거나 학습하지 않습니다.
root = pathlib.Path('/root/\ucd94\uacc4\ud559\uc220\ub300\ud68c')
notebook = json.loads((root / 'ball_ok_ng_yolo_v7.ipynb').read_text(encoding='utf-8'))
namespace = {'os': os, 'glob': glob, 'IMG_EXTS': ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'),
             'DUP_SIZE': 128, 'DUP_MAD': 1.0, 'np': np, 'cv2': cv2}
for cell in notebook['cells']:
    if cell['cell_type'] != 'code':
        continue
    for node in ast.parse(''.join(cell['source'])).body:
        if isinstance(node, ast.FunctionDef) and node.name in {'list_dataset', 'find_dup_groups'}:
            exec(compile(ast.Module(body=[node], type_ignores=[]), 'original_notebook', 'exec'), namespace)
with contextlib.redirect_stdout(io.StringIO()):
    items = namespace['list_dataset'](str(root / 'DataSet'), ['train', 'val', 'test'])
group_map, pairs = namespace['find_dup_groups'](items)
sizes = Counter()
label_class_ids = Counter()
for item in items:
    image = cv2.imread(item['img'], cv2.IMREAD_GRAYSCALE)
    sizes[f'{image.shape[1]}x{image.shape[0]}'] += 1
    for line in pathlib.Path(item['lab']).read_text(encoding='utf-8').splitlines():
        fields = line.split()
        if len(fields) >= 5:
            label_class_ids[fields[0]] += 1
args_paths = sorted(root.glob('runs/detect/yolo_runs/ball_detect_*_cv5f*grp*e30_tf1_sz1280_v0.1/args.yaml'))
args_samples = []
for path in args_paths[:3]:
    config = yaml.safe_load(path.read_text(encoding='utf-8'))
    args_samples.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'settings': {key: config.get(key) for key in ['model', 'epochs', 'imgsz', 'batch', 'patience', 'seed',
                                                                     'flipud', 'fliplr', 'scale', 'translate', 'hsv_v', 'mosaic', 'mixup']}})
print(json.dumps({'dataset_count': len(items), 'split_counts': dict(Counter(item['split'] for item in items)),
                  'image_sizes': dict(sizes), 'groups': len(set(group_map.values())), 'similar_pairs': pairs,
                  'group_map': group_map, 'label_class_ids': dict(label_class_ids),
                  'notebook_sha256': hashlib.sha256((root/'ball_ok_ng_yolo_v7.ipynb').read_bytes()).hexdigest(),
                  'args_paths_count': len(args_paths), 'args_samples': args_samples,
                  'training_executed': False, 'model_loaded': False}, ensure_ascii=True))
