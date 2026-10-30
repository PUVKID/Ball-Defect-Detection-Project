exec(open('work/native_render_test.py',encoding='utf-8-sig').read().split("h=win32")[0])
w=win32com.client.gencache.EnsureDispatch('Word.Application');w.Visible=False;w.DisplayAlerts=0
print('open',flush=True)
d=w.Documents.Open(str(pathlib.Path('work/paper.docx').resolve()),ReadOnly=True,AddToRecentFiles=False,Visible=False,ConfirmConversions=False)
time.sleep(3);print('export',flush=True)
d.ExportAsFixedFormat(str(pathlib.Path('work/word_paper.pdf').resolve()),17);print('exported',flush=True);d.Close(0);w.Quit()
