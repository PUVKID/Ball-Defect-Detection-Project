import sys,site,pathlib,os,time
D=pathlib.Path('work/deps').resolve();site.addsitedir(str(D));sys.path.extend([str(D/'win32'),str(D/'win32/lib')]);os.add_dll_directory(str(D/'pywin32_system32'))
import win32com.client
h=win32com.client.DispatchEx('HWPFrame.HwpObject');h.XHwpWindows.Item(0).Visible=False
ok=h.RegisterModule('FilePathCheckDLL','CodexPaperFilePathModule');print('HWP module',ok,flush=True)
if ok:
 print(h.Open(r'C:\Users\PUVKID\Desktop\학술대회논문양식_표준형식.hwp','HWP','forceopen:true'),flush=True)
 print(h.SaveAs(str(pathlib.Path('work/template.pdf').resolve()),'PDF',''),flush=True)
 print(h.SaveAs(str(pathlib.Path('work/template.hml').resolve()),'HWPML2X',''),flush=True)
h.Quit()
w=win32com.client.DispatchEx('Word.Application');w.Visible=False;w.DisplayAlerts=0
for i in range(10):
 try:
  d=w.Documents.Add();d.Content.Text='Render check';d.ExportAsFixedFormat(str(pathlib.Path('work/word_test.pdf').resolve()),17);d.Close(0);print('Word successful',flush=True);break
 except Exception as e:print('Word retry',str(e)[:130],flush=True);time.sleep(1)
w.Quit()
