exec(open('work/native_render_test.py',encoding='utf-8-sig').read().split("h=win32")[0])
import winreg
key=winreg.CreateKey(winreg.HKEY_CURRENT_USER,r'Software\HNC\HwpAutomation\Modules');winreg.SetValueEx(key,'FilePathCheckerModuleExample',0,winreg.REG_SZ,str(pathlib.Path('work/hwp_module/FilePathCheckerModuleExample.dll').resolve()));winreg.CloseKey(key)
h=win32com.client.gencache.EnsureDispatch('HWPFrame.HwpObject');print(type(h),h.Version,flush=True);h.XHwpWindows.Item(0).Visible=False
ok=h.RegisterModule('FilePathCheckDLL','FilePathCheckerModuleExample');print('Registered',ok,flush=True)
if ok:
 print('open',h.Open(str(pathlib.Path('work/paper.docx').resolve()),'OOXML','forceopen:true'),flush=True)
 print('save pdf',h.SaveAs(str(pathlib.Path('work/hwp_paper.pdf').resolve()),'PDF',''),flush=True)
 print('save hwp',h.SaveAs(str(pathlib.Path('work/paper.hwp').resolve()),'HWP',''),flush=True)
h.Quit()
