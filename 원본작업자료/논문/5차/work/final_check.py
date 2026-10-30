import json,pathlib
from pypdf import PdfReader
r=PdfReader('outputs/추계학술대회_볼배치검사_3쪽논문.pdf')
assert len(r.pages)==3
s=''.join(p.extract_text() for p in r.pages)
for token in ['19.09','25.27','12.40','18.53','95.40','94.13','55.27','368','500']:
 assert token in s,token
for p in r.pages:
 for f in p['/Resources']['/Font'].values():
  f=f.get_object()
  if '/FontDescriptor' in f:
   desc=f['/FontDescriptor'];assert any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3']),f
assert len(r.pages[2].get('/Annots',[]))==3
assert all(not any(p['overflow']) for p in json.loads(pathlib.Path('work/layout.json').read_text()))
print('PASS: 3 pages; reported key numbers; embedded used TrueType fonts; 3 reference links; page bounds.')
