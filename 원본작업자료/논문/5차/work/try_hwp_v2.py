import sys,site,pathlib,os
D=pathlib.Path('work/deps').resolve();site.addsitedir(str(D));sys.path.extend([str(D/'win32'),str(D/'win32/lib')]);os.add_dll_directory(str(D/'pywin32_system32'))
import win32com.client
h=win32com.client.DispatchEx('HWPFrame.HwpObject')
print('HWP automation created',flush=True)
h.XHwpWindows.Item(0).Visible=False
ok=h.RegisterModule('FilePathCheckDLL','CodexPaperFilePathModule');print('Module',ok,flush=True)
if ok:
 print('Open',h.Open(str(pathlib.Path('work/paper_v2.docx').resolve()),'OOXML','forceopen:true'),flush=True)
 print('HWP',h.SaveAs(str(pathlib.Path('work/paper_v2.hwp').resolve()),'HWP',''),flush=True)
 print('PDF',h.SaveAs(str(pathlib.Path('work/hwp_v2.pdf').resolve()),'PDF',''),flush=True)
h.Quit()
