"""Column-sized figures for filter and composition comparisons, from saved results only."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from reference_plot_style import configure_reference_style, draw_bar, save_reference_figure, label
from matplotlib.text import Text

def verify_paper_typography(fig):
    for t in fig.findobj(match=Text):t.set_fontweight('bold')
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    for ax in fig.axes:
        for ticks in [ax.get_xticklabels(),ax.get_yticklabels()]:
            boxes=[t.get_window_extent(renderer) for t in ticks if t.get_visible() and t.get_text()]
            for a,b in zip(boxes,boxes[1:]):
                assert not a.expanded(1.07,1.03).overlaps(b),'Tick labels overlap'
        if ax.get_xlabel():
            box=ax.xaxis.label.get_window_extent(renderer)
            assert all(not box.expanded(1,1.12).overlaps(t.get_window_extent(renderer)) for t in ax.get_xticklabels()),'Axis title overlaps filter names'
    assert all(t.get_fontweight()=='bold' for t in fig.findobj(match=Text))

def make_paper_filter_figures(results, output):
    R,O=Path(results),Path(output);O.mkdir(exist_ok=True,parents=True)
    configure_reference_style()
    single=pd.read_csv(R/'table_round1.csv');combo=pd.read_csv(R/'table_round2.csv')
    # Six categories at most per panel: no tiny, rotated names after column insertion.
    fig,axes=plt.subplots(2,1,figsize=(11,13.5))
    for ax,df in zip(axes,[single.iloc[:6],single.iloc[6:]]):
        draw_bar(ax,df.Filter,df['mAP50-95 (%)'],ylabel='mAP50-95 (%)',value_fmt='{:.1f}',
                 ymax=112,show_max=False,show_min=False)
        ax.set_yticks([0,50,100]);ax.set_xticklabels([{'Original':'Orig.','Invert':'Inv.','Otsu Threshold':'Otsu','Solarize':'Solar.','Histogram Equalization':'Hist.\nEq.','CLAHE (max)':'CLH','Gamma 0.3':'Gam.\n0.3','Gaussian Blur (max)':'Gauss.\nblur','Sobel Edges':'Sobel','Emboss':'Emb.','Unsharp (max)':'Un-\nsharp'}[n] for n in df.Filter],fontsize=35)
        ax.set_xlabel('');ax.tick_params(axis='x',pad=8)
        for t in ax._reference_annotations:t.set_fontsize(35)
    fig.subplots_adjust(left=.21,right=.98,top=.98,bottom=.08,hspace=.46)
    fig._reference_styled=True
    verify_paper_typography(fig)
    save_reference_figure(fig,O/'paper_figure1.png');fig.savefig(O/'paper_figure1.pdf',bbox_inches='tight');plt.close(fig)
    # Same mAP criterion for combinations; component gains are independently exported.
    fig,ax=plt.subplots(figsize=(11,8.2))
    draw_bar(ax,combo.Filter,combo['mAP50-95 (%)'],xlabel='Filter',ylabel='mAP50-95 (%)',
             value_fmt='{:.1f}',ymax=112,show_max=False,show_min=False)
    ax.set_xticklabels(['Orig.','Inv.\n+\nCLH','Blur\n+\nOtsu','Sob.\n+\nInv.','HE\n+\nEmb.','US\n+\nSob.'],fontsize=35)
    ax.set_yticks([0,20,40,60,80,100]);ax.tick_params(axis='x',pad=12);ax.xaxis.labelpad=24
    fig.subplots_adjust(left=.20,right=.985,bottom=.38,top=.97);fig._reference_styled=True
    verify_paper_typography(fig)
    save_reference_figure(fig,O/'paper_figure2.png');fig.savefig(O/'paper_figure2.pdf',bbox_inches='tight');plt.close(fig)
    # The same filters under noise; fixed 0..100 color scale does not exaggerate small gaps.
    n40=pd.read_csv(R/'table_grid_noise40.csv');n80=pd.read_csv(R/'table_grid_noise80.csv')
    assert single.Filter.tolist()[1:]==n40.Level.tolist()[1:]==n80.Level.tolist()[1:]
    data=np.array([single['mAP50-95 (%)'],n40['mAP50-95 (%)'],n80['mAP50-95 (%)']]).T
    fig,ax=plt.subplots(figsize=(11,10))
    im=ax.imshow(data,vmin=0,vmax=100,cmap='YlGn',aspect='auto')
    ax.set_xticks([0,1,2],['0','40','80'],fontsize=35)
    ax.set_xlabel('Noise SD',fontsize=45,labelpad=12)
    ax.set_yticks(range(11),['Orig.','Invert','Otsu','Solarize','Hist. Eq.','CLAHE','Gamma','Gauss.','Sobel','Emboss','Unsharp'],fontsize=35)
    ax.tick_params(length=0,pad=8)
    for i in range(11):
        for j in range(3):ax.text(j,i,f'{data[i,j]:.1f}',ha='center',va='center',fontsize=35,
                               fontweight='bold',color='white' if data[i,j]>=65 else 'black')
    fig.subplots_adjust(left=.30,right=.73,bottom=.14,top=.97)
    cax=fig.add_axes([.77,.20,.035,.65]);cb=fig.colorbar(im,cax=cax,ticks=[0,50,100]);cb.ax.tick_params(labelsize=35,pad=10);cb.set_label('mAP50-95 (%)',fontsize=45,labelpad=24)
    fig._reference_styled=True
    verify_paper_typography(fig)
    save_reference_figure(fig,O/'paper_figure3.png');fig.savefig(O/'paper_figure3.pdf',bbox_inches='tight');plt.close(fig)
    pairs={'Invert+CLAHE':('Invert','CLAHE (max)'), 'Blur+Otsu':('Gaussian Blur (max)','Otsu Threshold'),
           'Sobel+Invert':('Sobel Edges','Invert'),'HistEq+Emboss':('Histogram Equalization','Emboss'),
           'Unsharp+Sobel':('Unsharp (max)','Sobel Edges')}
    indexed=single.set_index('Filter');out=[]
    for _,r in combo.iloc[1:].iterrows():
        a,b=pairs[r.Filter];entry={'combination':r.Filter,'first':a,'second':b}
        for metric in ['mAP50-95 (%)','Strict Acc (%)']:
            best=max(indexed.loc[a,metric],indexed.loc[b,metric]);entry[metric]=float(r[metric]);entry[metric+' gain vs best component']=round(float(r[metric]-best),4)
        out.append(entry)
    (O/'combination_detection_comparison.json').write_text(json.dumps(out,indent=2),encoding='utf8')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    make_paper_filter_figures(a.results,a.output)
