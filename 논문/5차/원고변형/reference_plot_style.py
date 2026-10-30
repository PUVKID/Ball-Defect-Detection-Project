"""Summer-reference typography for the autumn conference results.

Only presentation is changed. No measurement, model, split or metric is changed.
Primary bars: NanumGothic Bold; axis 45, ticks 35, values bold 35,
legend 40 pt, 22 x 11 inches, white background, PNG 150 dpi.
Dense labels and multipanel diagnostics use smaller, explicitly bounded type.
"""
from pathlib import Path
import os, textwrap, re, json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.text import Text

FONT = 'NanumGothic'
def configure_reference_style():
    roots = [Path(__file__).resolve().parent / 'fonts',
             Path('/usr/share/fonts/truetype/nanum'),
             Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft/Windows/Fonts']
    found = False
    for root in roots:
        for name in ['NanumGothic.ttf', 'NanumGothicBold.ttf']:
            p = root / name
            if p.is_file(): fm.fontManager.addfont(str(p)); found = True
    if not found: raise FileNotFoundError('NanumGothic.ttf and NanumGothicBold.ttf are required')
    plt.rcParams.update({'font.family': FONT, 'font.weight': 'bold',
        'axes.labelweight': 'bold', 'axes.titleweight': 'bold',
        'axes.unicode_minus': False, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
        'axes.edgecolor': 'black', 'axes.labelcolor': 'black', 'xtick.color': 'black',
        'ytick.color': 'black', 'text.color': 'black', 'grid.color': '#cccccc',
        'grid.linestyle': '--', 'grid.alpha': .5, 'legend.facecolor': 'white',
        'legend.edgecolor': '#cccccc', 'legend.labelcolor': 'black', 'svg.fonttype': 'none'})

def accuracy_color(v):
    for cut, color in [(85,'#2ea043'),(75,'#7ec852'),(65,'#d4e052'),
                       (55,'#e8a838'),(45,'#e86b38')]:
        if v >= cut: return color
    return '#c0392b'

FILTER_NAMES = ('Original', 'Invert', 'Otsu', 'Solarize', 'Histogram', 'CLAHE',
                'Gamma', 'Gaussian', 'Sobel', 'Emboss', 'Unsharp', 'Blur+', 'HistEq+')
def label(s):
    names = {
        'Original':'Orig.', 'Invert':'Inv.', 'Otsu Threshold':'Otsu',
        'Histogram Equalization':'Hist.\nEq.', 'CLAHE (max)':'CLAHE',
        'Gaussian Blur (max)':'Gauss.\nblur', 'Gamma 0.3':'Gamma\n0.3',
        'Sobel Edges':'Sobel', 'Unsharp (max)':'Unsharp',
        'Invert+CLAHE':'Inv.+\nCLAHE', 'Blur+Otsu':'Blur+\nOtsu',
        'Sobel+Invert':'Sobel+\nInv.', 'HistEq+Emboss':'Hist.Eq.+\nEmboss',
        'Unsharp+Sobel':'Unsharp+\nSobel'}
    s = str(s).replace('\n', ' ')
    return names.get(s, s)


def is_filter_label(s):
    return any(word in str(s) for word in FILTER_NAMES + ('Orig.', 'Inv.', 'Hist.', 'Gauss.'))

def _fit_neighbor_text(fig, texts, minimum=18):
    # Only shrink when neighboring labels' actual rendered bounding boxes overlap.
    for _ in range(18):
        fig.canvas.draw(); renderer = fig.canvas.get_renderer()
        boxes = [t.get_window_extent(renderer) for t in texts]
        bad = set()
        for i in range(len(boxes)):
            for j in range(i+1,len(boxes)):
                if boxes[i].expanded(1.035,1.02).overlaps(boxes[j]): bad.update([i,j])
        if not bad: return
        changed = False
        for i in bad:
            t=texts[i]
            if t.get_fontsize()>minimum:
                t.set_fontsize(max(minimum,t.get_fontsize()-1)); changed=True
        if not changed: return

def draw_bar(ax, labels, values, xlabel='', ylabel='Strict accuracy (%)',
             value_fmt='{:.1f}%', ymax=None, ymin=0, threshold=None,
             threshold_label=None, show_max=True, show_min=True,
             higher_is_better=True, yerr=None, seeds=None, compact=False):
    values=np.asarray(values,float); n=len(values)
    colors=[accuracy_color(v) for v in values]
    if not higher_is_better:
        lo,hi=values.min(),values.max()
        colors=[accuracy_color(100-65*(v-lo)/max(hi-lo,1e-9)) for v in values]
    ax.bar(np.arange(n),values,width=.6,color=colors,zorder=3,
           yerr=yerr,capsize=7 if yerr is not None else 0,
           error_kw={'elinewidth':2,'capthick':2,'ecolor':'black'})
    if seeds is not None:
        for j,(seed,vals) in enumerate(seeds.items()):
            ax.scatter(np.arange(n)+(j-1)*.10,vals,s=70,marker=['o','s','^'][j],
                       color='white',edgecolors='black',linewidths=1.3,zorder=5)
    ann=[]
    spread=max(values.max()-values.min(),1)
    pad=2.0 if '%' in value_fmt else max(values.max()*.025,spread*.03)
    for i,v in enumerate(values):
        err=0 if yerr is None else float(yerr[i])
        peak=max(v+err,max(float(vals[i]) for vals in seeds.values())) if seeds is not None else v+err
        ann.append(ax.text(i,peak+pad,value_fmt.format(v),ha='center',va='bottom',
                           fontsize=35,fontweight='bold',color='black',zorder=6,
                           bbox={'facecolor':'white','edgecolor':'none','pad':.25}))
    if show_max: ax.axhline(values.max(),color='#ff6b6b',ls='--',lw=1.5,label=f'Max {values.max():.1f}'+('%' if '%' in value_fmt else ''))
    if show_min: ax.axhline(values.min(),color='#4ecdc4',ls='--',lw=1.5,label=f'Min {values.min():.1f}'+('%' if '%' in value_fmt else ''))
    if threshold is not None: ax.axhline(threshold,color='gray',ls=':',lw=1.2,label=threshold_label or f'{threshold:g}% reference')
    ax.set_xticks(np.arange(n),[label(s) for s in labels],fontsize=35, rotation=0, ha='center', va='top')
    ax.tick_params(axis='y',labelsize=35)
    ax.set_xlabel(xlabel,fontsize=45); ax.set_ylabel(ylabel,fontsize=45)
    top=ymax if ymax is not None else (115 if '%' in value_fmt else max(values.max()*1.22,.1))
    ax.set_ylim(ymin,max(top,values.max()+(np.max(yerr) if yerr is not None else 0)+pad*7))
    ax.set_axisbelow(True);ax.grid(axis='y');ax.margins(x=.04)
    # Above the plotting area so an almost-100% bar cannot be covered by the legend.
    if show_max or show_min or threshold is not None:
        ax.legend(loc='lower center',bbox_to_anchor=(.5,1.015),ncol=3,
                  fontsize=30 if compact else 40,frameon=True)
    ax._reference_annotations=ann
    ax._reference_bar=True
    return ann

def finish_bar(fig):
    fig.tight_layout(pad=1.4)
    for ax in fig.axes:
        _fit_neighbor_text(fig,ax.get_xticklabels(),minimum=23)
        _fit_neighbor_text(fig,getattr(ax,'_reference_annotations',[]),minimum=24)
    fig.tight_layout(pad=1.4)
    fig._reference_styled=True

def plot_clean_bar(labels, values, xlabel, ylabel, save_name, value_fmt='{:.1f}%',
                   ymax=None,ymin=0,show_max=True,show_min=True,threshold=None,
                   threshold_label=None,figsize=None,rotation=0,value_fontsize=None,
                   higher_is_better=True,out_dir=None,legend_above=True):
    configure_reference_style()
    # Match the reference's one-decimal labels; full precision remains in CSV/JSON.
    if '%' in value_fmt: value_fmt='{:.1f}%'
    fig,ax=plt.subplots(figsize=(max(22,len(labels)*2.2),11))
    draw_bar(ax,labels,values,'Preprocessing filter' if xlabel=='Filter' else xlabel,ylabel,
             value_fmt,max(115,ymax or 0) if '%' in value_fmt else ymax,ymin,
             threshold,threshold_label,show_max,show_min,higher_is_better)
    finish_bar(fig)
    path=Path(out_dir or 'yolo_filter_figures')/save_name;path.parent.mkdir(parents=True,exist_ok=True)
    save_reference_figure(fig,path)
    plt.close(fig)
    return str(path)

def apply_reference_style(fig):
    """Type-specific adaptation for existing scientific diagnostic figures."""
    if getattr(fig,'_reference_styled',False):return
    configure_reference_style(); fig.set_facecolor('white')
    w,h=fig.get_size_inches(); scale=max(1,22/w)
    fig.set_size_inches(w*scale,h*scale)
    # Retain the hierarchy of dense multi-panel/scatter/heatmap reference charts.
    for text in fig.findobj(match=Text):
        text.set_fontfamily(FONT)
        text.set_fontsize(min(35,max(12,text.get_fontsize()*scale)))
        if isinstance(text.get_color(),str) and text.get_color() in ['#aaa','#222222','#1a1a1a']:text.set_color('black')
    for ax in fig.axes:
        # Put filter categories on the horizontal axis and rotate their short, horizontal names.
        old_y=[t.get_text() for t in ax.get_yticklabels()]
        if ax.images and sum(is_filter_label(t) for t in old_y)>1:
            im=ax.images[0]; data=np.asarray(im.get_array()); old_x=[t.get_text() for t in ax.get_xticklabels()]
            im.set_data(data.T);im.set_extent((-.5,data.shape[0]-.5,data.shape[1]-.5,-.5))
            ax.set_xlim(-.5,data.shape[0]-.5);ax.set_ylim(data.shape[1]-.5,-.5)
            for t in ax.texts:
                tx,ty=t.get_position();t.set_position((ty,tx))
            ax.set_xticks(range(data.shape[0]),old_y,rotation=0,ha='center',fontsize=16)
            ax.set_yticks(range(data.shape[1]),old_x,rotation=0,fontsize=16)
            xl,yl=ax.get_xlabel(),ax.get_ylabel();ax.set_xlabel(yl);ax.set_ylabel(xl)
        for t in ax.get_xticklabels():
            if is_filter_label(t.get_text()):
                t.set_text(label(t.get_text()));t.set_rotation(0);t.set_ha('center');t.set_va('top')
        xt = ax.get_xticklabels()
        if any(is_filter_label(t.get_text()) for t in xt):
            ax.set_xticks(ax.get_xticks(), [label(t.get_text()) for t in xt], rotation=0)
        ax.set_facecolor('white')
        ax.xaxis.label.set_weight('bold');ax.yaxis.label.set_weight('bold')
        for t in ax.get_xticklabels()+ax.get_yticklabels():t.set_weight('bold')
        for l in ax.get_xgridlines()+ax.get_ygridlines():l.set(color='#cccccc',linestyle='--',alpha=.5)
        _fit_neighbor_text(fig,ax.get_xticklabels(),minimum=12)
        _fit_neighbor_text(fig,ax.texts,minimum=10)
        leg=ax.get_legend()
        if leg is not None:
            leg.get_frame().set_facecolor('white');leg.get_frame().set_edgecolor('#cccccc')
            for t in leg.get_texts():t.set_fontweight('bold')
    fig.tight_layout(pad=1.6)
    fig._reference_styled=True

def save_reference_figure(fig,*args,**kwargs):
    apply_reference_style(fig)
    for t in fig.findobj(match=Text):
        t.set_fontfamily(FONT); t.set_fontweight('bold')
    strings=[t.get_text() for t in fig.findobj(match=Text) if t.get_visible() and t.get_text()]
    if any(re.search(r'[\uac00-\ud7af\u3131-\u318e]',s) for s in strings):
        raise ValueError('Korean text remains in the graph')
    rotations=[{'text':t.get_text(),'angle':t.get_rotation()} for ax in fig.axes for t in ax.get_xticklabels() if is_filter_label(t.get_text())]
    kwargs['metadata']={'Description':json.dumps({'visible_text':strings,'filter_label_rotations':rotations,'typography':[{'text':t.get_text(),'size':t.get_fontsize(),'weight':t.get_fontweight(),'family':t.get_fontfamily()} for t in fig.findobj(match=Text) if t.get_visible() and t.get_text()]},ensure_ascii=False)}
    kwargs.update(dpi=150,facecolor='white',bbox_inches='tight')
    return fig.savefig(*args,**kwargs)

def draw_reference_dashboard(results,title,diagnose):
    """Six plots, with a horizontal ranking instead of the old dense table."""
    configure_reference_style()
    fig,axs=plt.subplots(2,3,figsize=(32,20),layout='constrained')
    labs=[str(r.get('label',r['name'])) for r in results];x=np.arange(len(labs))
    short=[label(s) for s in labs]
    acc=np.array([r['accuracy'] for r in results]);mp=np.array([r['map50_95'] for r in results])
    for ax,vals,title_ in [(axs[0,0],acc,'1) OK/NG agreement (%)'),(axs[0,1],mp,'2) mAP50-95 (%)')]:
        ax.bar(x,vals,color=[accuracy_color(v) for v in vals]);ax.set_xticks(x,short,fontsize=12,rotation=0)
        ax.set_ylim(0,114);ax.set_title(title_,fontsize=22,pad=15)
        for i,v in enumerate(vals):ax.text(i,v+1,f'{v:.1f}',ha='center',fontsize=11)
        ax.grid(axis='y');ax.set_axisbelow(True)
    ax=axs[0,2];mat=np.array([[r[k] for k in ['ok_recall','ng_recall','ball_recall']] for r in results])
    im=ax.imshow(mat.T,cmap='YlGn',vmin=0,vmax=100,aspect='auto')
    ax.set_yticks(range(3),['OK','NG','Ball'],fontsize=18);ax.set_xticks(x,short,fontsize=12,rotation=0)
    for i in range(len(labs)):
        for j in range(3):ax.text(i,j,f'{mat[i,j]:.0f}',ha='center',va='center',fontsize=11,color='white' if mat[i,j]>70 else 'black')
    ax.set_title('3) Recall (%)',fontsize=22,pad=15);fig.colorbar(im,ax=ax,shrink=.8)
    ax=axs[1,0];hs=list((results[0].get('histories') or {}).values())
    for key,col in [('map50','#2ea043'),('map50_95','#e8a838')]:
        seq=[h[key] for h in hs if h.get(key)]
        if seq:
            n=max(map(len,seq));m=np.array([list(s)+[s[-1]]*(n-len(s)) for s in seq])*100
            ep=np.arange(1,n+1);ax.plot(ep,m.mean(0),label=key,color=col,lw=2)
            ax.fill_between(ep,m.mean(0)-m.std(0),m.mean(0)+m.std(0),color=col,alpha=.18)
    ax.set_title('4) Baseline validation curves',fontsize=22,pad=15);ax.set_xlabel('Epoch',fontsize=18);ax.set_ylabel('mAP (%)',fontsize=18)
    ax.legend(loc='lower right',fontsize=16);ax.grid()
    ax=axs[1,1];bottom=np.zeros(len(results))
    for state,col in [('good','#2ea043'),('overfit','#e86b38'),('underfit','#e8a838')]:
        vals=[sum(diagnose(h)==state for h in (r.get('histories') or {}).values()) for r in results]
        ax.bar(x,vals,bottom=bottom,color=col,label=state);bottom+=vals
    ax.set_xticks(x,short,fontsize=12,rotation=0);ax.set_ylim(0,max(bottom)+2)
    ax.set_title('5) Fold diagnostics (heuristic)',fontsize=22,pad=15);ax.set_ylabel('Folds',fontsize=18)
    ax.legend(loc='upper right',fontsize=14);ax.grid(axis='y');ax.set_axisbelow(True)
    ax=axs[1,2];order=np.argsort(-acc,kind='stable')
    ax.bar(x,acc[order],color=[accuracy_color(v) for v in acc[order]])
    ax.set_xticks(x,[short[i] for i in order],fontsize=12,rotation=0);ax.set_ylim(0,114)
    for i,v in enumerate(acc[order]):ax.text(i,v+1,f'{v:.1f}',ha='center',fontsize=11)
    ax.set_title('6) OK/NG agreement ranking (%)',fontsize=22,pad=15);ax.grid(axis='y');ax.set_axisbelow(True)
    fig.suptitle(title+' — YOLOv8n',fontsize=26)
    fig._reference_styled=True
    return fig

configure_reference_style()
