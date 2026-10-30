from pathlib import Path
p=Path('work/build_pdf.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("elif kind=='ref':y=text(s,x,y,CW,'english',10,11,'left',0,after=4)","""elif kind=='ref':
   top=y
   y=text(s,x,y,CW,'english',10,11,'left',0,after=4)
   urls={'[1]':'https://docs.ultralytics.com/models/yolov8/','[2]':'https://github.com/erich666/GraphicsGems/blob/master/gemsiv/clahe.c','[3]':'https://arxiv.org/abs/1910.02190'}
   cv.linkURL(urls[s[:3]],(x,y+8,x+CW,top+10),relative=0,thickness=0)""")
p.write_text(s,encoding='utf8')
