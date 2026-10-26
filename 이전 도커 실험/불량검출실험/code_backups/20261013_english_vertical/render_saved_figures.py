"""Rebuild existing autumn experiment graphs without loading models or training.

python render_saved_figures.py --results yolo_filter_figures --output yolo_filter_figures_reference
"""
import argparse,ast,json,math,os,re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd
from reference_plot_style import *

def main():
 p=argparse.ArgumentParser();p.add_argument('--results',default='yolo_filter_figures');p.add_argument('--output',default='yolo_filter_figures_reference');p.add_argument('--notebook',default=str(Path(__file__).with_name('ball_ok_ng_yolo_v7_reference.ipynb')));args=p.parse_args()
 R=Path(args.results);O=Path(args.output);O.mkdir(parents=True,exist_ok=True)
 summary=json.loads((R/'results_summary.json').read_text(encoding='utf8'))
 sweep=json.loads((R/'sweep_results.json').read_text(encoding='utf8'))
 notebook=Path(args.notebook)
 if not notebook.exists() and notebook.name=='ball_ok_ng_yolo_v7_reference.ipynb':
  notebook=notebook.with_name('ball_ok_ng_yolo_v7.ipynb')
 nb=json.loads(notebook.read_text(encoding='utf8'))
 env=dict(globals(),FILTER_FIG_DIR=str(O),FIG_DIR=str(O),CV_FOLDS=5,SHOW_INLINE=False,GRAPH_THEME='light',DARK_RC={},GPU_LOG=[],USE_CV=True)
 # Load function definitions and the metric specification, never executable training cells.
 wanted={'make_all_metric_plots','diagnose_fit_yolo','_pad_stack','make_reference_graphs','plot_components_vs_combination'}
 for cell in nb['cells']:
  if cell['cell_type']!='code':continue
  tree=ast.parse(''.join(cell['source']))
  nodes=[a for a in tree.body if (isinstance(a,ast.FunctionDef) and a.name in wanted) or (isinstance(a,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='METRIC_SPECS' for t in a.targets))]
  if nodes:exec(compile(ast.Module(body=nodes,type_ignores=[]),'saved_plot_functions','exec'),env)
 for roundname in ['round1','round2']:
  env['make_all_metric_plots'](summary[roundname],roundname,summary['baseline'])
 env['baseline_result']=summary['baseline']
 env['plot_components_vs_combination'](pd.read_csv(R/'table_combo_vs_components.csv'))
 groups=[('filters',[dict(summary['baseline'],label='Original')]+[dict(r,label=r['name']) for r in summary['round1']+summary['round2']], 'preprocessing filter','Preprocessing filter')]
 names={'blur':('Gaussian blur','Blur sigma'),'noise':('Gaussian noise','Noise sigma'),'resolution':('input resolution','Input size'),'data':('training subset','Training share')}
 for k,v in sweep['sweeps'].items():groups.append(('sweep_'+k,v,*names[k]))
 for k,v in sweep['grid'].items():groups.append(('grid_noise'+k,v,'filter at noise sigma='+k,'Preprocessing filter'))
 for key,res,title,xlabel in groups:
  env['make_reference_graphs'](key,res,title,xlabel,show_gpu=False)
  plt.close('all')
 # Repeat-seed plots retain both standard deviation and individual observed seeds.
 for name in ['normal','noise_80','hard__noise_40___25__data']:
  df=pd.read_csv(R/f'ms_table_{name}.csv')
  fig,ax=plt.subplots(figsize=(22,11))
  draw_bar(ax,df.Method,df['Strict mean'],xlabel='전처리 필터',yerr=df['Strict std'].to_numpy(),
           seeds={s:df[f'strict s{s}'] for s in [42,43,44]},show_max=False,show_min=False)
  finish_bar(fig);fig.savefig(O/f'fig_multiseed_{name}.png',dpi=150,bbox_inches='tight');plt.close(fig)
 # Paper figure 1 includes the original baseline explicitly.
 df=pd.read_csv(R/'table_round1.csv')
 plot_clean_bar(df.Filter,df['Strict Acc (%)'],'전처리 필터','엄격 정확도 (%)','paper_figure1.png',out_dir=O,
                threshold=None)
 # Two comparable degradation panels with shared typography, no legend over the data.
 fig,axs=plt.subplots(1,2,figsize=(26,10.5),gridspec_kw={'width_ratios':[1,1.75]})
 for ax,name,title in zip(axs,['noise_80','hard__noise_40___25__data'],['(a) 잡음 σ=80 · 학습 100%','(b) 잡음 σ=40 · 학습 25%']):
  df=pd.read_csv(R/f'ms_table_{name}.csv')
  draw_bar(ax,df.Method,df['Strict mean'],yerr=df['Strict std'].to_numpy(),
           seeds={s:df[f'strict s{s}'] for s in [42,43,44]},show_max=False,show_min=False)
  ax.set_title(title,fontsize=35,pad=22)
  ax.yaxis.label.set_fontsize(35);ax.tick_params(axis='both',labelsize=30)
 axs[1].set_ylabel('')
 finish_bar(fig);fig.savefig(O/'paper_figure2.png',dpi=150,bbox_inches='tight');plt.close(fig)
 # Track exact source files for reproducibility.
 import hashlib
 sources={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in R.glob('*.csv')}
 sources.update({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['results_summary.json','sweep_results.json']})
 (O/'source_hashes.json').write_text(json.dumps(sources,indent=2),encoding='utf8')
 print('Saved',len(list(O.rglob('*.png'))),'graphs to',O)

if __name__=='__main__':main()
