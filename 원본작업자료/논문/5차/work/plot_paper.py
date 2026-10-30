import pathlib,pandas as pd,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
R=pathlib.Path('/root/추계학술대회/yolo_filter_figures');O=pathlib.Path('/tmp/paper_audit');O.mkdir(exist_ok=True)
font_manager.fontManager.addfont('/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf')
plt.rcParams.update({'font.family':'NanumGothic','font.weight':'bold','axes.labelweight':'bold','axes.titleweight':'bold','font.size':8,'axes.unicode_minus':False})
fig,axs=plt.subplots(1,2,figsize=(6,2.8),gridspec_kw={'width_ratios':[1,1.55]})
for ax,file,title,labs in zip(axs,['ms_table_noise_80.csv','ms_table_hard__noise_40___25__data.csv'],['(a) Noise σ = 80, full training set','(b) Noise σ = 40, 25% training set'],[['Original','Gaussian\nblur','CLAHE'],['Original','CLAHE','HistEq','Gamma\n0.3','Gaussian\nblur','Invert']]):
 d=pd.read_csv(R/file);x=np.arange(len(d));colors=['#a7abb0']+['#447da5']*(len(d)-1)
 ax.bar(x,d['Strict mean'],yerr=d['Strict std'],capsize=2.4,width=.65,color=colors,edgecolor='#34495e',linewidth=.65,error_kw={'elinewidth':.8})
 for k,s in enumerate([42,43,44]):ax.scatter(x+(k-1)*.10,d[f'strict s{s}'],s=10,marker=['o','s','^'][k],color=['#222222','#ed9b40','#5d9269'][k],label=f'Seed {s}',zorder=3)
 for i,r in d.iterrows():ax.text(i,r['Strict mean']+r['Strict std']+3,f'{r["Strict mean"]:.1f}',ha='center',fontsize=7)
 ax.set_ylim(0,108);ax.set_yticks(range(0,101,20));ax.set_xticks(x,labs,fontsize=7);ax.set_title(title,fontsize=7.7,pad=9);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.25);ax.spines[['top','right']].set_visible(False)
axs[0].set_ylabel('Strict accuracy (%)',fontsize=8)
axs[0].legend(loc='lower left',fontsize=6.5,frameon=False)
fig.subplots_adjust(left=.085,right=.99,bottom=.18,top=.87,wspace=.28)
fig.savefig(O/'figure2_multiseed.png',dpi=500);fig.savefig(O/'figure2_multiseed.pdf')
print('chart done')
