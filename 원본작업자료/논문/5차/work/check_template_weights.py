import olefile,zlib,struct
o=olefile.OleFileIO('C:/Users/PUVKID/Desktop/학술대회논문양식_표준형식.hwp')
def records(b):
 p=0
 while p<len(b):
  h=struct.unpack_from('<I',b,p)[0];p+=4;t=h&1023;n=h>>20
  if n==4095:n=struct.unpack_from('<I',b,p)[0];p+=4
  yield t,b[p:p+n];p+=n
sh=[]
for t,b in records(zlib.decompress(o.openstream('DocInfo').read(),-15)):
 if t==21:
  sh.append({'size':struct.unpack_from('<I',b,42)[0]/100,'bold':bool(struct.unpack_from('<I',b,46)[0]&2)})
text=''
for t,b in records(zlib.decompress(o.openstream('BodyText/Section0').read(),-15)):
 if t==67:text=b.decode('utf16',errors='replace')
 if t==68:
  ids=[struct.unpack_from('<II',b,i)[1] for i in range(0,len(b),8)]
  print(repr(text[:65]),[(i,sh[i]) for i in ids])
