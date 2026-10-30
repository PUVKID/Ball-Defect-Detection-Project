from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
files=sorted(Path('work/restyled').rglob('*.png'))
out=Path('work/contacts');out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
for start in range(0,len(files),6):
 page=Image.new('RGB',(2200,1800),'#cccccc');d=ImageDraw.Draw(page)
 for j,p in enumerate(files[start:start+6]):
  x=(j%2)*1100;y=(j//2)*600
  im=Image.open(p);im.thumbnail((1080,552))
  page.paste(im,(x+(1100-im.width)//2,y+40+(552-im.height)//2))
  d.text((x+12,y+8),str(p.relative_to('work/restyled')),font=font,fill='black')
 page.save(out/f'contact-{start//6+1:02}.jpg',quality=95)
print(len(files),'images',len(list(out.glob('*.jpg'))),'sheets')
