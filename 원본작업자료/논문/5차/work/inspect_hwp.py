import olefile,zlib,struct,pathlib
p=pathlib.Path('C:/Users/PUVKID/Desktop/학술대회논문양식_표준형식.hwp')
o=olefile.OleFileIO(p)
print(o.listdir())
print(o.openstream('PrvText').read().decode('utf-16le'))
for s in o.listdir():
 if s[0]=='BodyText':
  b=zlib.decompress(o.openstream(s).read(),-15); pos=0
  while pos<len(b):
   h=struct.unpack_from('<I',b,pos)[0];pos+=4;t=h&1023;n=h>>20
   if n==4095:n=struct.unpack_from('<I',b,pos)[0];pos+=4
   d=b[pos:pos+n];pos+=n
   if t==67: print(d.decode('utf-16le',errors='replace'))
