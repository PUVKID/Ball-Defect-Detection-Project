from pathlib import Path
import json
p=Path('work/reference_plot_style.py');s=p.read_text(encoding='utf8')
s=s.replace('NanumGothic regular','NanumGothic Bold').replace("'font.weight': 'normal'","'font.weight': 'bold'").replace("'axes.labelweight': 'normal'","'axes.labelweight': 'bold'").replace("'axes.titleweight': 'normal'","'axes.titleweight': 'bold'")
s=s.replace("set_weight('normal')","set_weight('bold')").replace("set_fontweight('normal')","set_fontweight('bold')")
s=s.replace("    apply_reference_style(fig)\n    strings=", "    apply_reference_style(fig)\n    for t in fig.findobj(match=Text):\n        t.set_fontfamily(FONT); t.set_fontweight('bold')\n    strings=")
s=s.replace("'filter_label_rotations':rotations", "'filter_label_rotations':rotations,'typography':[{'text':t.get_text(),'size':t.get_fontsize(),'weight':t.get_fontweight(),'family':t.get_fontfamily()} for t in fig.findobj(match=Text) if t.get_visible() and t.get_text()]")
p.write_text(s,encoding='utf8')
p=Path('work/paper_filter_figures.py');s=p.read_text(encoding='utf8')
s=s.replace("[label(n).replace('Solarize','Solar.') for n in df.Filter],fontsize=31", "[{'Original':'Orig.','Invert':'Inv.','Otsu Threshold':'Otsu','Solarize':'Solar.','Histogram Equalization':'Hist.\\nEq.','CLAHE (max)':'CLH','Gamma 0.3':'Gamma\\n0.3','Gaussian Blur (max)':'Gauss.\\nblur','Sobel Edges':'Sobel','Emboss':'Emb.','Unsharp (max)':'Un-\\nsharp'}[n] for n in df.Filter],fontsize=35")
s=s.replace("['Orig.','Inv.+\\nCLAHE','Blur+\\nOtsu','Sobel+\\nInv.','HE+\\nEmb.','US+\\nSobel'],fontsize=31", "['Orig.','Inv.\\n+CLH','Blur\\n+Otsu','Sob.\\n+Inv.','HE\\n+Emb.','US\\n+Sob.'],fontsize=35")
s=s.replace("ax.tick_params(axis='x',pad=10)","ax.tick_params(axis='x',pad=12);ax.xaxis.labelpad=24")
s=s.replace("bottom=.25,top=.97", "bottom=.30,top=.97")
s=s.replace("cb.ax.tick_params(labelsize=30);cb.set_label('mAP50-95 (%)',fontsize=35)","cb.ax.tick_params(labelsize=35,pad=10);cb.set_label('mAP50-95 (%)',fontsize=45,labelpad=24)")
# A fixed canvas width makes the effective print type equal in all three figures.
s=s.replace("fig.subplots_adjust(left=.30,right=.82,bottom=.12,top=.97)","fig.subplots_adjust(left=.30,right=.73,bottom=.14,top=.97)")
s=s.replace("[.86,.18,.035,.70]","[.77,.20,.035,.65]")
p.write_text(s,encoding='utf8')
p=Path('work/build_docx_v2.py');s=p.read_text(encoding='utf8')
s=s.replace("r.font.name=fn[f];r.font.size=Pt(size)","r.font.bold=True;r.font.name=fn[f];r.font.size=Pt(size)")
s=s.replace("for st in d.styles:\n", "for st in d.styles:\n if hasattr(st,'font'):st.font.bold=True\n")
# The page field has its own run properties.
s=s.replace("fld.set(qn('w:instr'),'PAGE');r._r.addnext(fld)","fld.set(qn('w:instr'),'PAGE');fr=OxmlElement('w:r');fp=OxmlElement('w:rPr');fp.append(OxmlElement('w:b'));fr.append(fp);ft=OxmlElement('w:t');ft.text='1';fr.append(ft);fld.append(fr);r._r.addnext(fld)")
p.write_text(s,encoding='utf8')
p=Path('work/content_v2.json');c=json.loads(p.read_text(encoding='utf8'))
for col in c['columns']:
 for i,(kind,t) in enumerate(col):
  if t.startswith('단일 필터는'):t=t.replace('CLAHE,','CLAHE(CLH),').replace('Sobel,','Sobel(Sob.),')
  col[i]=[kind,t]
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
