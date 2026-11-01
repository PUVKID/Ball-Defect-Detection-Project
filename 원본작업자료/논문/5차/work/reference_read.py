import json,pathlib
p=pathlib.Path(r'./그림/Blur_Block_1차_그래프_white.ipynb')
n=json.loads(p.read_text(encoding='utf8'))
for i,c in enumerate(n['cells']):
 print('\nCELL',i,c['cell_type']);print(''.join(c.get('source',[])))
