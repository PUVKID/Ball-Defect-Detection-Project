import json,pathlib
n=json.loads(pathlib.Path('work/notebook.ipynb').read_text(encoding='utf8'))
for i in [6,8,10,12,14,16,26,28,30,48,57,66,71,72]:
 c=n['cells'][i]
 if i in [30,57]: continue
 print('\n###CELL',i); print(''.join(c['source']))
 if i in [6,12,14,48]:
  for o in c.get('outputs',[]):
   if 'text' in o: print('OUTPUT:', ''.join(o['text'])[:6000])
