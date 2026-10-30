import pathlib,json,re,sys
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
P=pathlib.Path;C=json.loads(P('work/content.json').read_text(encoding='utf8'));O=P('outputs');O.mkdir(exist_ok=True)
root=P('C:/Program Files (x86)/Hnc/Office NEO')
fonts={'body':P('work/fonts/body.ttf'),'heading':P('work/fonts/heading.ttf'),'caption':P('C:/Windows/Fonts/H2GTRM.TTF'),'engtitle':P('C:/Windows/Fonts/H2MJRE.TTF'),'english':P('C:/Windows/Fonts/times.ttf')}
for k,p in fonts.items():pdfmetrics.registerFont(TTFont(k,str(p)))
W,H=538.58,737.01;M=56.69;BW=W-2*M;CW=(BW-22.68)/2;bottom=49.61
cv=canvas.Canvas(str(O/'추계학술대회_볼배치검사_3쪽논문.pdf'),pagesize=(W,H));cv.setTitle(C['title'].replace('\n',' '));cv.setAuthor('')
logs=[]
def width(text,font,size,scale=.9,spacing=-.06):return (pdfmetrics.stringWidth(text,font,size)+(len(text)-1)*spacing*size)*scale

def wrap(text,font,size,limit,scale=.9,spacing=-.06):
 lines=[]
 for para in text.split('\n'):
  tokens=re.findall(r'[A-Za-z0-9][A-Za-z0-9_./:+%~-]*|\s+|.',para)
  line=''
  for t in tokens:
   if width(line+t,font,size,scale,spacing)<=limit or not line:line+=t
   else:lines.append(line.rstrip());line=t.lstrip()
  lines.append(line.rstrip())
 return lines

def text(text,x,y,w,font='body',size=10,leading=14,align='justify',indent=9,spacing=-.06,after=6):
 lines=wrap(text,font,size,w-indent)
 # conservative equal wrapping; first line indent only
 for i,line in enumerate(lines):
  lw=width(line,font,size,spacing=spacing); xx=x+(indent if i==0 else 0)
  if align=='center':xx=x+(w-lw)/2
  elif align=='right':xx=x+w-lw
  extra=0
  if align=='justify' and i<len(lines)-1 and len(line)>1:extra=(w-(indent if i==0 else 0)-lw)/.9/(len(line)-1)
  t=cv.beginText(xx,y);t.setFont(font,size);t.setHorizScale(90);t.setCharSpace(spacing*size+extra);t.textOut(line);cv.drawText(t);y-=leading
 return y-after

def header(pg):
 text('- 2026 한국정보기술학회 추계 종합학술대회 논문집 -',M,H-28.35,BW,size=9,align='center',indent=0,after=0)
 text(f'- {pg} -',M,18,BW,font='english',size=10,align='center',indent=0,after=0)
def col(items,x,y):
 for kind,s in items:
  if kind=='h':y=text(s,x,y-3,CW,'heading',11,16,'center',0,after=8)
  elif kind=='sub':y=text(s,x,y-2,CW,'caption',11,16,'left',0,after=6)
  elif kind=='ref':
   top=y
   y=text(s,x,y,CW,'english',10,11,'left',0,after=4)
   urls={'[1]':'https://docs.ultralytics.com/models/yolov8/','[2]':'https://github.com/erich666/GraphicsGems/blob/master/gemsiv/clahe.c','[3]':'https://arxiv.org/abs/1910.02190'}
   cv.linkURL(urls[s[:3]],(x,y+8,x+CW,top+10),relative=0,thickness=0)
  else:y=text(s,x,y,CW)
 return y
for page in range(1,4):
 header(page);y=H-58
 if page==1:
  y=text(C['title'],M,y,BW,size=17,leading=21,align='center',indent=0,spacing=-.07,after=18)
  y-=10 # blank Korean author line
  y=text(C['english'],M,y,BW,'engtitle',15,19,'center',0,-.07,18)
  y-=8 # blank English author line
  y=text('요  약',M,y,BW,'body',11,14,'center',0,after=7)
  y=text(C['abstract_ko'],M+5,y,BW-10,'body',9.2,13.2,after=8)
  y=text('Abstract',M,y,BW,'english',11,14,'center',0,after=7)
  y=text(C['abstract_en'],M+5,y,BW-10,'english',9.2,12.7,after=7)
  y=text('Key words',M,y,BW,'english',9.2,12,'center',0,after=2)
  y=text(C['keywords'],M,y,BW,'english',9.2,12,'center',0,after=17)
 else:
  path='work/figures/fig_round1_15_strict_accuracy.png' if page==2 else 'work/figure2_multiseed.png'
  im=Image.open(path);iw=BW if page==2 else BW; ih=iw*im.height/im.width;cv.drawImage(path,M+(BW-iw)/2,y-ih,width=iw,height=ih);y-=ih+10
  if page==2:
   y=text('그림 1. 일반 영상에서 단일 필터별 엄격 정확도 (시드 42)',M,y,BW,'caption',9,12,'center',0,after=0)
   y=text('Fig. 1. Strict accuracy of individual filters on clean images (seed 42)',M,y,BW,'caption',9,12,'center',0,after=12)
  else:
   y=text('그림 2. 열화 조건별 엄격 정확도 (막대: 3개 시드 평균, 오차막대: 표준편차, 점: 각 시드)',M,y,BW,'caption',9,12,'center',0,after=0)
   y=text('Fig. 2. Strict accuracy under degradation (mean, standard deviation, and individual seeds)',M,y,BW,'caption',9,12,'center',0,after=12)
  
 ends=[col(C['pages'][page-1][0],M,y),col(C['pages'][page-1][1],M+CW+22.68,y)]
 logs.append({'page':page,'body_top':y,'ends':ends,'overflow':[max(0,bottom-v) for v in ends]})
 cv.showPage()
cv.save();print(json.dumps(logs,indent=2));P('work/layout.json').write_text(json.dumps(logs))



