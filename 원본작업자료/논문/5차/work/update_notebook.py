import ast,json,pathlib
P=pathlib.Path
n=json.loads(P('work/notebook.ipynb').read_text(encoding='utf8'))
changed=[]
for i,c in enumerate(n['cells']):
 if c['cell_type']!='code':continue
 s=''.join(c['source']);old=s
 if i==4:
  s='''# Shared plotting style adapted from the supplied summer conference notebook.
# Graph labels and legends are fitted to avoid overlap; research computations are unchanged.
from reference_plot_style import (configure_reference_style, plot_clean_bar as _reference_bar,
    save_reference_figure, draw_bar, finish_bar, label, draw_reference_dashboard)
configure_reference_style()

def plot_clean_bar(*args, **kwargs):
    kwargs.setdefault("out_dir", FIG_DIR)
    return _reference_bar(*args, **kwargs)
'''
 else:
  if i==55:
   a=s.index('        # 10 ─ dashboard');b=s.index('    return saved',a)
   s=s[:a]+'''        # 10: six readable plots; no dense ranking table.
        fig = draw_reference_dashboard(results, title, diagnose_fit_yolo)
        savefig("10_dashboard.png")
'''+s[b:]
  # Rewrite only savefig call spans, retaining comments and all other source text.
  tree=ast.parse(s);lines=s.splitlines(keepends=True);offset=[0]
  for line in lines:offset.append(offset[-1]+len(line.encode('utf8')))
  edits=[];raw=s.encode('utf8')
  for node in ast.walk(tree):
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='savefig':
    owner=ast.get_source_segment(s,node.func.value)
    target='plt.gcf()' if owner=='plt' else owner
    a=offset[node.func.lineno-1]+node.func.col_offset
    b=offset[node.func.end_lineno-1]+node.func.end_col_offset
    edits.append((a,b,('save_reference_figure').encode()))
    # Add figure as the first argument immediately after the call's open parenthesis.
    pos=raw.find(b'(',b)+1
    edits.append((pos,pos,(target+', ').encode()))
  for a,b,repl in sorted(edits,reverse=True):raw=raw[:a]+repl+raw[b:]
  s=raw.decode('utf8')
 if s!=old:
  ast.parse(s);changed.append(i);c['source']=s.splitlines(keepends=True)
  c['outputs']=[];c['execution_count']=None
for c in n['cells']:
 if c['cell_type']=='code':c['outputs']=[];c['execution_count']=None
n['cells'].insert(0,{'cell_type':'markdown','metadata':{},'source':[
 '# 그래프 서식 수정본 · 2026-10-13\n',
 '그래프는 영어로 표기하고 필터 이름은 짧은 영어 이름으로 2~3줄 가로 배치합니다. 나눔고딕 Bold·흰 배경·색상 체계를 유지하고 겹침 방지를 위해 여백과 크기를 조절합니다.\n',
 '학습·데이터 분할·평가 지표·저장된 측정값은 변경하지 않았습니다. 전체 실행은 원래 설정대로 학습을 수행할 수 있습니다.\n',
 '**그래프만 다시 만들 때:** `python render_saved_figures.py --results yolo_filter_figures --output yolo_filter_figures_reference`\n']})
n['cells'].append({'cell_type':'markdown','metadata':{},'source':['## Conference paper figures: single filters, ordered combinations, and noise\n','These plots use detection mAP and saved results only. They do not train or change the detector.\n']})
n['cells'].append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':[
 'from paper_filter_figures import make_paper_filter_figures\n',
 'make_paper_filter_figures(FILTER_FIG_DIR, os.path.join(FILTER_FIG_DIR, "paper_filter_comparison"))\n']})
P('work/ball_ok_ng_yolo_v7_reference.ipynb').write_text(json.dumps(n,ensure_ascii=False,indent=1),encoding='utf8')
print('changed cells',changed)
