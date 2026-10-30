from fontTools.ttLib import TTFont,TTCollection
from pathlib import Path
for p in list(Path('C:/Windows/Fonts').glob('HM*'))+list(Path('C:/Users/PUVKID/AppData/Local/Microsoft/Windows/Fonts').glob('*Nanum*')):
 try:
  fonts=TTCollection(p).fonts if p.suffix.lower()=='.ttc' else [TTFont(p)]
  print(p.name,[[x.toUnicode() for x in f['name'].names if x.nameID==1][:3] for f in fonts])
 except Exception as e:print(e)
