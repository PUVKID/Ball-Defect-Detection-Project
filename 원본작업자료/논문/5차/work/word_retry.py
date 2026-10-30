exec(open('work/native_render_test.py',encoding='utf-8-sig').read().split("h=win32")[0])
w=win32com.client.gencache.EnsureDispatch('Word.Application');w.Visible=False;w.DisplayAlerts=0
d=w.Documents.Add();time.sleep(4)
for i in range(12):
 try:
  print(d.Name,flush=True);d.Content.Text='Render check';d.ExportAsFixedFormat(str(pathlib.Path('work/word_test.pdf').resolve()),17);print('exported',flush=True);d.Close(0);break
 except Exception as e: print('retry',str(e)[:100],flush=True);time.sleep(2)
w.Quit()
