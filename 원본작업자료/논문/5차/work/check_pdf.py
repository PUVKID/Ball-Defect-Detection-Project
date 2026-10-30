import pdfplumber,pathlib
with pdfplumber.open('outputs/추계학술대회_볼배치검사_3쪽논문.pdf') as p:
 for i,pg in enumerate(p.pages):
  print(i+1,pg.width,pg.height,pg.extract_text()[:100], 'top chars',[(c['text'],round(c['x0'],1),round(c['top'],1)) for c in pg.chars if c['top']<40][:12])
  print('bounds',min(c['x0'] for c in pg.chars),max(c['x1'] for c in pg.chars),max(c['bottom'] for c in pg.chars if c['top']<690))
