import io,json,pathlib,struct,zlib
import olefile
from PIL import Image

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=pathlib.Path('C:/Users/PUVKID/Desktop/2026/추계학술대회/논문/3차/추계학술대회 논문 3차.hwp')
TEMPLATE=pathlib.Path('C:/Users/PUVKID/Desktop/2025/학술대회논문양식_표준양식.hwp')

def records(data):
    position=0
    while position<len(data):
        header=struct.unpack_from('<I',data,position)[0];position+=4
        tag=header&1023;level=(header>>10)&1023;size=header>>20
        if size==4095:size=struct.unpack_from('<I',data,position)[0];position+=4
        yield tag,level,data[position:position+size]
        position+=size

def text_only(data):
    text=data.decode('utf-16le');result=[];position=0
    while position<len(text):
        number=ord(text[position])
        if number in [1,2,3,4,5,6,7,8,9,11,12,14,15,16,17,18,19,20,21,22,23]:position+=8
        else:
            if number>=32 or number in [10,13]:result.append(text[position])
            position+=1
    return ''.join(result).strip()

def inspect(path):
    ole=olefile.OleFileIO(path);fonts=[];shapes=[];mapping=None
    for tag,level,data in records(zlib.decompress(ole.openstream('DocInfo').read(),-15)):
        if tag==17:mapping=struct.unpack_from('<8I',data)
        if tag==19:
            count=struct.unpack_from('<H',data,1)[0]
            fonts.append(data[3:3+count*2].decode('utf-16le'))
        if tag==21:
            ids=struct.unpack_from('<7H',data)
            shapes.append({'korean_font_id':ids[0],'latin_font_id':ids[1],'size_pt':struct.unpack_from('<I',data,42)[0]/100,'bold':bool(struct.unpack_from('<I',data,46)[0]&2),'width_percent':list(data[14:21]),'spacing_percent':list(struct.unpack_from('<7b',data,21))})
    for shape in shapes:
        shape['korean_font']=fonts[shape['korean_font_id']]
        shape['latin_font']=fonts[mapping[1]+shape['latin_font_id']]
    paragraphs=[];pages=[];images=[];columns=[];paragraph=None
    for tag,level,data in records(zlib.decompress(ole.openstream('BodyText/Section0').read(),-15)):
        if tag==66:
            paragraph={'level':level,'text':'','char_shape_ids':[]};paragraphs.append(paragraph)
        elif tag==67:paragraph['text']=text_only(data)
        elif tag==68:paragraph['char_shape_ids']=[struct.unpack_from('<II',data,i)[1] for i in range(0,len(data),8)]
        elif tag==73:
            values=struct.unpack_from('<9I',data)
            pages.append({'width_mm':values[0]/7200*25.4,'height_mm':values[1]/7200*25.4,'margins_mm':[v/7200*25.4 for v in values[2:6]],'header_footer_mm':[v/7200*25.4 for v in values[6:8]]})
        elif tag==71 and data[:4]==b'dloc':columns.append({'level':level,'raw':data.hex(),'flags':struct.unpack_from('<H',data,4)[0]})
        elif tag==71 and data[:4]==b' osg':
            width,height=struct.unpack_from('<II',data,16)
            images.append({'width_mm':width/7200*25.4,'height_mm':height/7200*25.4})
    for paragraph in paragraphs:paragraph['styles']=[shapes[i] for i in paragraph['char_shape_ids']]
    return {'paragraphs':paragraphs,'page_definitions':pages,'column_controls':columns,'image_sizes':images}

current=inspect(SOURCE);template=inspect(TEMPLATE)
(ROOT/'evidence/main_layout_details.json').write_text(json.dumps({'source':current,'template':template},ensure_ascii=False,indent=2),encoding='utf8')
for i,item in enumerate(current['image_sizes'],1):
    path=ROOT/'work'/f'BIN000{i}.{ "bmp" if i==1 else "png"}.png'
    im=Image.open(path);item['pixels']=list(im.size);item['dpi_x']=im.width/(item['width_mm']/25.4)
    item['dpi_y']=im.height/(item['height_mm']/25.4)
print(json.dumps({'page':current['page_definitions'],'columns':current['column_controls'],'images':current['image_sizes']},ensure_ascii=False,indent=2))
for data,title in [(current,'SOURCE'),(template,'TEMPLATE')]:
    for p in data['paragraphs']:
        if p['text'].startswith(('YOLOv8n 기반','한글제목','Performance Comparison','영문제목','곽윤석','저자*','요  약','Abstract','현장에 따라','비접촉 삼차원','그림 1.','그림 3.','참 고 문 헌')):
            print(title,p['text'][:40],json.dumps(p['styles'],ensure_ascii=False))
