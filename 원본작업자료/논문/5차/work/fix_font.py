import sys,pathlib
sys.path.insert(0,'work/deps')
from fontTools.ttLib import TTFont
r=pathlib.Path('C:/Program Files (x86)/Hnc/Office NEO');o=pathlib.Path('work/fonts');o.mkdir(exist_ok=True)
for fname,outname in [('HMKMM.TTF','body'),('HMKMG.TTF','heading')]:
 f=TTFont(next(r.rglob(fname)))
 for n in f['name'].names:
  if n.nameID==6:n.string=f'Paper{outname}'.encode(n.getEncoding())
 f.save(o/f'{outname}.ttf')
