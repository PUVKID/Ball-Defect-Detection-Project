import pathlib,json,ast,os,glob,math,random,csv,hashlib
from collections import Counter,defaultdict
import numpy as np,cv2,pandas as pd
R=pathlib.Path('/root/추계학술대회'); O=pathlib.Path('/tmp/paper_audit');O.mkdir(exist_ok=True)
nb=json.loads((R/'ball_ok_ng_yolo_v7.ipynb').read_text())
IMG_EXTS=(".png",".jpg",".jpeg"); BALL_CLASSES=None; REGION_RULE={'top':5,'left':4,'bottom':2,'right':2}
DUP_SIZE=128;DUP_MAD=1.0;GROUP_FOLDS=True;CV_FOLDS=5;CV_VAL_FRAC=.1;STRESS_TRAIN_FRAC=1.;SEED=42
for i in [6,8,10,12,14,30,72]:
 tree=ast.parse(''.join(nb['cells'][i]['source']))
 allowed={'read_yolo_boxes','list_dataset','_ellipse','_locate_part_once','locate_part','assign_region','judge_boxes','_gt_worker','find_dup_groups','assign_folds','fold_split','ms_cluster_boot','ball_match_stats'}
 for n in tree.body:
  if isinstance(n,ast.Assign) and i==8 and any(isinstance(t,ast.Name) and t.id=='LOC_PARAMS' for t in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),'nb','exec'))
  if isinstance(n,ast.FunctionDef) and n.name in allowed:exec(compile(ast.Module(body=[n],type_ignores=[]),'nb','exec'))
cv2.setNumThreads(1)
CV_ITEMS=list_dataset(str(R/'DataSet'),['train','val','test'])
gt_by_key={it['key']:_gt_worker(it) for it in CV_ITEMS}
print('GT',Counter(g['gt_pred'] for g in gt_by_key.values()),flush=True)
DUP_GROUP_OF,pairs=find_dup_groups(CV_ITEMS)
print('groups',len(set(DUP_GROUP_OF.values())),'pairs',pairs,flush=True)
report={'n':len(CV_ITEMS),'class_counts':dict(Counter(g['gt_pred'] for g in gt_by_key.values())),'groups':len(set(DUP_GROUP_OF.values())),'similar_pairs':pairs,'failures':sum(g['loc_fail'] for g in gt_by_key.values()),'sizes':dict(Counter((g['W'],g['H']) for g in gt_by_key.values()))}
report['sizes']={str(k):v for k,v in report['sizes'].items()}
report['splits']={}
for seed in [42,43,44]:
 SEED=seed;FOLD_OF=assign_folds(CV_ITEMS,5,seed)
 arr=[]
 for fold in range(5):
  tr,va,te=fold_split(fold); ts={DUP_GROUP_OF[x['key']] for x in tr};vs={DUP_GROUP_OF[x['key']] for x in va};es={DUP_GROUP_OF[x['key']] for x in te}
  arr.append({'n':[len(tr),len(va),len(te)],'outer_group_overlap':len((ts|vs)&es),'inner_group_overlap':len(ts&vs)})
 report['splits'][seed]=arr
(O/'group_map.json').write_text(json.dumps(DUP_GROUP_OF))
df=pd.read_csv(R/'yolo_filter_figures/ms_per_image.csv');df['strict']=(df['miss']==0)&(df['extra']==0)
assert len(df)==19500
assert all(len(x)==500 and x.key.nunique()==500 for _,x in df.groupby(['condition','seed','method']))
assert all(df['match']==(df.gt_pred==df.pred))
assert all(df.gt_pred==df.key.map({k:g['gt_pred'] for k,g in gt_by_key.items()}))
summary=df.groupby(['condition','method','seed']).agg(strict=('strict','mean'),accuracy=('match','mean'))*100
summary.to_csv(O/'recalculated.csv')
comparisons=[]
for cond,cd in df.groupby('condition',sort=False):
 ref=cd[cd.method=='Original'].pivot(index='key',columns='seed',values='strict').astype(int)
 for method,md in cd.groupby('method',sort=False):
  scores=summary.loc[(cond,method)]
  r={'condition':cond,'method':method,'strict_mean':float(scores.strict.mean()),'strict_sd':float(scores.strict.std()),'acc_mean':float(scores.accuracy.mean())}
  if method!='Original':
   alt=md.pivot(index='key',columns='seed',values='strict').astype(int);diff=(alt-ref).mean(axis=1).to_dict()
   a,lo,hi=ms_cluster_boot(diff,DUP_GROUP_OF);r.update(delta=100*a,ci=[100*lo,100*hi])
  comparisons.append(r)
report['metrics']=comparisons
(O/'audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)

