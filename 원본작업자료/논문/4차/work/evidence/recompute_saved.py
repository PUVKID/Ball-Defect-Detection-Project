import ast
import csv
import hashlib
import json
import math
import pathlib
import random
import statistics
from collections import Counter, defaultdict

# 저장된 행을 다시 집계하고 원래 분할 함수만 격리하여 실행합니다. 학습은 수행하지 않습니다.
ROOT = pathlib.Path(__file__).resolve().parents[2]
OLD = pathlib.Path('C:/Users/PUVKID/Documents/Codex/2026-10-13/x20/work')
DATA = OLD / 'figures'
EVIDENCE = ROOT / 'work/evidence'


def read_rows(name):
    with (DATA / name).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


summary = json.loads((DATA / 'results_summary.json').read_text(encoding='utf-8'))
sweep = json.loads((DATA / 'sweep_results.json').read_text(encoding='utf-8'))
baseline = summary['baseline']
results = [baseline] + summary['round1'] + summary['round2']
by_name = {row['name']: row for row in results}
single_rows = read_rows('per_image_predictions.csv')
multi_rows = read_rows('ms_per_image.csv')
multi_summary = read_rows('ms_run_results.csv')
groups = json.loads((OLD / 'group_map.json').read_text(encoding='utf-8'))
single = defaultdict(list)
for row in single_rows:
    single[row['method']].append(row)
assert len(single_rows) == 8000
assert len(single) == 16
recomputed = []
for method, rows in single.items():
    assert len(rows) == len({row['key'] for row in rows}) == 500
    strict = 100 * sum(int(row['miss']) == 0 and int(row['extra']) == 0 for row in rows) / len(rows)
    assert abs(strict - by_name[method]['strict_acc']) < 1e-8
    assert all(int(row['match']) == (row['gt_pred'] == row['pred']) for row in rows)
    recomputed.append({'method': method, 'n': len(rows), 'strict_acc': strict,
                       'saved_map50_95': by_name[method]['map50_95']})

multi = defaultdict(list)
for row in multi_rows:
    multi[(row['condition'], int(row['seed']), row['method'])].append(row)
assert len(multi_rows) == 19500 and len(multi) == 39
multi_values = defaultdict(lambda: {'map50_95': [], 'strict_acc': [], 'seeds': []})
for row in multi_summary:
    key = (row['condition'], int(row['seed']), row['method'])
    rows = multi[key]
    assert len(rows) == len({r['key'] for r in rows}) == 500
    strict = 100 * sum(int(r['miss']) == 0 and int(r['extra']) == 0 for r in rows) / len(rows)
    assert abs(strict - float(row['strict_acc'])) < 1e-8
    assert all(int(r['match']) == (r['gt_pred'] == r['pred']) for r in rows)
    values = multi_values[(key[0], key[2])]
    values['strict_acc'].append(strict)
    values['map50_95'].append(float(row['map50_95']))
    values['seeds'].append(key[1])
repeat = []
for (condition, method), values in multi_values.items():
    assert sorted(values['seeds']) == [42, 43, 44]
    repeat.append({'condition': condition, 'method': method, 'seeds': values['seeds'],
                   **{metric: {'values': values[metric], 'mean': statistics.mean(values[metric]),
                               'sample_sd': statistics.stdev(values[metric])}
                      for metric in ['map50_95', 'strict_acc']}})

# 조합은 단일 시드에서 각 구성 필터 중 더 높은 값과 직접 비교합니다.
parts = {'Invert+CLAHE': ['Invert', 'CLAHE (max)'],
         'Blur+Otsu': ['Gaussian Blur (max)', 'Otsu Threshold'],
         'Sobel+Invert': ['Sobel Edges', 'Invert'],
         'HistEq+Emboss': ['Histogram Equalization', 'Emboss'],
         'Unsharp+Sobel': ['Unsharp (max)', 'Sobel Edges']}
combinations = []
for name, components in parts.items():
    item = {'method': name, 'components': components}
    for metric in ['map50_95', 'strict_acc']:
        best = max(components, key=lambda component: by_name[component][metric])
        item[metric] = {'combination': by_name[name][metric], 'best_component': best,
                        'best_component_value': by_name[best][metric],
                        'delta_pp': by_name[name][metric] - by_name[best][metric]}
    combinations.append(item)
assert all(row['map50_95']['delta_pp'] < 0 for row in combinations)
noise = []
for level in ['40', '80']:
    grid = {row['name']: row for row in sweep['grid'][level]}
    for row in read_rows(f'table_grid_noise{level}.csv'):
        assert abs(float(row['mAP50-95 (%)']) - grid[row['Filter']]['map50_95']) <= 0.00501
        assert abs(float(row['Strict Acc (%)']) - grid[row['Filter']]['strict_acc']) <= 0.00501
        noise.append({'noise': int(level), 'method': row['Filter'],
                      'saved_map50_95': grid[row['Filter']]['map50_95']})
assert len(noise) == 22

# 실제 노트북의 분할 함수 두 개만 실행합니다. 학습 셀과 파일 작성 함수는 실행하지 않습니다.
notebook = json.loads((OLD / 'notebook.ipynb').read_text(encoding='utf-8'))
namespace = {'random': random, 'defaultdict': defaultdict, 'GROUP_FOLDS': True,
             'DUP_GROUP_OF': groups, 'CV_FOLDS': 5, 'CV_VAL_FRAC': 0.1, 'STRESS_TRAIN_FRAC': 1.0}
first = single['Original']
labels = {row['key']: {'gt_pred': row['gt_pred']} for row in first}
# 데이터 함수와 동일하게 split 순서 뒤 이름순으로 정렬합니다.
keys = sorted(labels, key=lambda key: (['train', 'val', 'test'].index(key.split('/')[0]), key.split('/')[1]))
namespace.update(CV_ITEMS=[{'key': key} for key in keys], gt_by_key=labels)
for node in ast.parse(''.join(notebook['cells'][30]['source'])).body:
    if isinstance(node, ast.FunctionDef) and node.name in {'assign_folds', 'fold_split'}:
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'original_notebook_cell_30', 'exec'), namespace)
splits = []
for seed in [42, 43, 44]:
    namespace['SEED'] = seed
    namespace['FOLD_OF'] = namespace['assign_folds'](namespace['CV_ITEMS'], 5, seed)
    if seed == 42:
        assert all(namespace['FOLD_OF'][row['key']] == int(row['fold']) for row in first)
    for fold in range(5):
        train, val, test = namespace['fold_split'](fold)
        ts, vs, es = [{groups[row['key']] for row in section} for section in [train, val, test]]
        trlabels = Counter(labels[row['key']]['gt_pred'] for row in train)
        factor = min(6, max(1, round(max(trlabels.values()) / min(trlabels.values()))))
        record = {'seed': seed, 'fold': fold, 'n_train': len(train), 'n_val': len(val), 'n_test': len(test),
                  'outer_group_overlap': len((ts | vs) & es), 'inner_group_overlap': len(ts & vs),
                  'oversample_factor': factor}
        assert record['outer_group_overlap'] == 0
        splits.append(record)
assert min(s['inner_group_overlap'] for s in splits) == 9
assert max(s['inner_group_overlap'] for s in splits) == 20

hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in
          [DATA / 'per_image_predictions.csv', DATA / 'ms_per_image.csv', DATA / 'ms_run_results.csv',
           DATA / 'results_summary.json', DATA / 'sweep_results.json', OLD / 'notebook.ipynb', OLD / 'group_map.json']}
report = {'raw_rows': len(single_rows) + len(multi_rows), 'single_run_count': len(single),
          'multiseed_run_count': len(multi), 'noise_summary_count': len(noise),
          'single': recomputed, 'repeat': repeat, 'combinations': combinations, 'noise': noise,
          'dataset': {'n_images': len(keys), 'split_counts': dict(Counter(key.split('/')[0] for key in keys)),
                      'n_groups': len(set(groups.values())), 'class_counts': dict(Counter(v['gt_pred'] for v in labels.values()))},
          'splits': splits, 'sources_sha256': hashes,
          'scope': {'training_rerun': False, 'ap_recomputed': False, 'strict_recomputed': True,
                    'group_map_recreated_here': False, 'old_notebook_functions_executed': ['assign_folds', 'fold_split']}}
(EVIDENCE / 'recalculated.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'raw_rows': report['raw_rows'], 'single_runs': len(single), 'multiseed_runs': len(multi),
                  'noise_summaries': len(noise), 'dataset': report['dataset'],
                  'inner_group_overlap_range': [min(s['inner_group_overlap'] for s in splits), max(s['inner_group_overlap'] for s in splits)],
                  'all_outer_group_overlap_zero': True, 'oversample_factors': sorted(set(s['oversample_factor'] for s in splits))}, ensure_ascii=False))
