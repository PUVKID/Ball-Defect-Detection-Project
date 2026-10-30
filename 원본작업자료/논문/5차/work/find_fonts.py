import pathlib,sys
sys.path.insert(0,'work/deps')
from fontTools.ttLib import TTFont,TTCollection
for p in pathlib.Path('C:/Windows/Fonts').glob('*'):
 if p.suffix.lower() not in ['.ttf','.ttc']:continue
 try:
  fs=TTCollection(p,lazy=True).fonts if p.suffix.lower()=='.ttc' else [TTFont(p,lazy=True)]
  for i,f in enumerate(fs):
   ns={n.toUnicode() for n in f['name'].names if n.nameID==1}
   if ns&{'휴먼명조','휴먼고딕','HY견명조','HY중고딕'}: print(p.name,i,ns)
 except:pass
