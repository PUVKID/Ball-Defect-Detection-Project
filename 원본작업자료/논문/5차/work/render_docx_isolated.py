"""Run the packaged renderer with isolated Linux conversion on Windows.
No desktop Office processes or installation are used or modified.
"""
import sys,os,tempfile,importlib.util,pathlib,subprocess
root=pathlib.Path('work').resolve();tmp=root/'render_tmp';tmp.mkdir(exist_ok=True)
tempfile.tempdir=str(tmp)
skill=pathlib.Path('C:/Users/PUVKID/.codex/plugins/cache/openai-primary-runtime/documents/26.1011.11113/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('packaged_renderer',skill);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod._resolve_soffice=lambda:'/usr/bin/soffice'
run=mod._run_cmd
def isolated_run(cmd,env,verbose):
 if cmd[0]=='/usr/bin/soffice':
  def translate(a):
   a=a.replace(str(root).replace('\\','/'),'/work').replace(str(root),'/work')
   a=a.replace(root.as_uri(),'file:///work')
   return a.replace('\\','/')
  cmd=['docker','exec','codex-docx-render-20261013']+[translate(a) for a in cmd]
 return run(cmd,env,verbose)
mod._run_cmd=isolated_run
os.environ['PATH']='C:/Users/PUVKID/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;'+os.environ['PATH']
mod.main()
