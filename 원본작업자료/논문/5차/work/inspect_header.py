from pypdf import PdfReader
from PIL import Image
r=PdfReader('outputs/추계학술대회_볼배치검사_3쪽논문.pdf')
for i,p in enumerate(r.pages):
 print(i+1,p.get_contents().get_data()[:900])
 im=Image.open(f'work/final_review-{i+1}.png').convert('L');print('header dark',sum(1 for v in im.crop((200,20,1100,90)).getdata() if v<128))
