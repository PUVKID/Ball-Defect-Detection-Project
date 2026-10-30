import olefile,zlib,struct,pathlib
p=pathlib.Path('C:/Users/PUVKID/Desktop/학술대회논문양식_표준형식.hwp');o=olefile.OleFileIO(p)
pathlib.Path('work/template_preview.png').write_bytes(o.openstream('PrvImage').read())
b=zlib.decompress(o.openstream('BodyText/Section0').read(),-15);pos=0
while pos<len(b):
 h=struct.unpack_from('<I',b,pos)[0];pos+=4;t=h&1023;n=h>>20
 if n==4095:n=struct.unpack_from('<I',b,pos)[0];pos+=4
 d=b[pos:pos+n];pos+=n
 if t in [73,71,74]:print(t,n,d.hex() if t!=71 else repr(d[:28]))
