import json,pathlib
p=pathlib.Path('work'); n=json.loads((p/'notebook.ipynb').read_text(encoding='utf8'))
f=[]
for i,c in enumerate(n['cells']):
 s=''.join(c.get('source',[])); f.append(f'\n\n# CELL {i} {c["cell_type"]}\n{s}')
 print(i,c['cell_type'],len(s),s[:150].replace('\n',' '))
(p/'notebook.txt').write_text(''.join(f),encoding='utf8')
