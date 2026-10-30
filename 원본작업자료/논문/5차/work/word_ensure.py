exec(open('work/native_render_test.py',encoding='utf-8-sig').read().split("h=win32")[0])
w=win32com.client.gencache.EnsureDispatch('Word.Application');print(type(w));print('version',w.Version);w.Visible=False;w.DisplayAlerts=0
d=w.Documents.Add();print(type(d));print('n',w.Documents.Count);print(d.Name);print(d.Content);d.Content.Text='Render check';d.ExportAsFixedFormat(str(pathlib.Path('work/word_test.pdf').resolve()),17);d.Close(0);w.Quit()
