import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, sys
out=sys.argv[1]
NAVY='#3b5a80'; RUST='#c0532b'; PURP='#6a4c9c'; GRAY='#555'; LIGHT='#9aa7b8'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':18,'axes.spines.top':False,'axes.spines.right':False,
  'axes.edgecolor':'#222','axes.linewidth':1.2})
# 16K, suite average. Phase 1: Protocol A (Table 20). Phase 2: Protocol B (Table 26).
# values: [Base_A, SFT_A, SFT_B, ReasSFT_B]
D={'MixtureVitae':{'c':RUST,'en':[29.1,26.6,23.4,34.1],'wo':[11.3,11.5,None,None]},
   'Comma0.1':{'c':PURP,'en':[27.5,25.3,22.2,38.0],'wo':[11.1,11.7,11.5,7.5]},
   'Nemotron-CC-HQ':{'c':NAVY,'en':[26.5,22.1,21.2,35.3],'wo':[7.8,8.1,7.9,6.6]},
   'FineWeb-Edu':{'c':NAVY,'en':[26.0,22.2,20.0,33.3],'wo':[8.3,7.7,7.5,6.2]}}
X=[0,1,1.9,2.9]   # gap between x=1 and x=1.9 = protocol break
XL=['Base','Tulu3\nSFT','Tulu3\nSFT','Reasoning\nSFT']

def frame(ax,ymax=42):
    ax.axvspan(1.25,1.65,color='#f1f3f6',zorder=0)
    ax.set_xticks(X); ax.set_xticklabels(XL,fontsize=17); ax.tick_params(axis='x',length=0,pad=6)
    ax.set_xlim(-0.35,3.3); ax.set_ylim(0,ymax); ax.grid(axis='y',color='#ececec',lw=1); ax.set_axisbelow(True)
    ax.text(0.5,ymax*1.0,'Phase 1',ha='center',va='top',fontsize=15.5,color='#8a93a3',weight='bold')
    ax.text(2.4,ymax*1.0,'Phase 2',ha='center',va='top',fontsize=15.5,color='#8a93a3',weight='bold')

def seg(ax,ys,col,dashed=False,lw=3.5,ms=12,alpha=1,z=3):
    for a,b in [(0,1),(2,3)]:
        if ys[a] is None or ys[b] is None: continue
        ax.plot([X[a],X[b]],[ys[a],ys[b]],color=col,lw=lw,ls='--' if dashed else '-',alpha=alpha,zorder=z)
    for i,y in enumerate(ys):
        if y is None: continue
        ax.plot(X[i],y,'o',ms=ms,color=col if not dashed else 'white',mec=col,mew=2.2,alpha=alpha,zorder=z+1)

def gapbar(ax,x,lo,hi,txt,col=GRAY,big=False,left=False):
    ax.annotate('',xy=(x,hi),xytext=(x,lo),arrowprops=dict(arrowstyle='<->',color=col,lw=1.6 if not big else 2.4,shrinkA=6,shrinkB=6),zorder=2)
    ax.text(x+(-0.07 if left else 0.07),(lo+hi)/2,txt,ha='right' if left else 'left',va='center',fontsize=18 if not big else 21,color=col,weight='bold' if big else 'normal')

# ---------- Variant A: small multiples ----------
fig,axs=plt.subplots(1,3,figsize=(13.5,5.2),dpi=300,sharey=True)
for ax,(name,d) in zip(axs,[(k,D[k]) for k in ('MixtureVitae','Comma0.1','Nemotron-CC-HQ')]):
    frame(ax); c=d['c']
    seg(ax,d['wo'],c,dashed=True,alpha=0.75); seg(ax,d['en'],c)
    ax.set_title(name+(' (permissive)' if name in('MixtureVitae','Comma0.1') else ''),fontsize=19,color=c if c!=NAVY else '#222',weight='bold',pad=30)
    for i in [0,3] if d['wo'][3] is not None else [0]:
        g=d['en'][i]-d['wo'][i]; gapbar(ax,X[i]+(0.13 if i==0 else 0.1),d['wo'][i],d['en'][i],f'{g:.0f}',big=(i==3))
axs[0].set_ylabel('Reasoning suite avg. (16K)',fontsize=18)
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([],[],color='#444',lw=3,marker='o',ms=10,label='Front-loaded (enriched)'),
                    Line2D([],[],color='#444',lw=3,ls='--',marker='o',mfc='white',mew=2.2,ms=10,label='Without front-loading')],
           loc='upper center',ncol=2,frameon=False,fontsize=19,bbox_to_anchor=(0.5,1.02))
fig.tight_layout(rect=(0,0,1,0.93)); fig.savefig(out+'/draft_stages_multiples.png',facecolor='white'); plt.close(fig)

# ---------- Variant B: one panel, mean of the 3 complete pairs + MV ----------
fig,ax=plt.subplots(figsize=(9.5,6),dpi=250)
frame(ax,ymax=42); ax.set_xlim(-0.35,3.6)
names=['Comma0.1','Nemotron-CC-HQ','FineWeb-Edu']
for n in names:
    seg(ax,D[n]['en'],NAVY,lw=1.2,ms=0,alpha=0.25,z=1); seg(ax,D[n]['wo'],NAVY,lw=1.2,ms=0,alpha=0.25,z=1)
men=[np.mean([D[n]['en'][i] for n in names]) for i in range(4)]
mwo=[np.mean([D[n]['wo'][i] for n in names]) for i in range(4)]
seg(ax,mwo,NAVY,dashed=True,ms=11); seg(ax,men,NAVY,ms=11)
seg(ax,D['MixtureVitae']['en'],RUST,lw=2.4,ms=9)
for i in range(4):
    gapbar(ax,X[i]+(0.12 if i<2 else (-0.12 if i==2 else 0.3)),mwo[i],men[i],('gap ' if i==0 else '')+f'{men[i]-mwo[i]:.1f}',big=(i==3),left=(i==2))
ax.text(X[3]-0.1,D['MixtureVitae']['en'][3]-1.6,'MV',color=RUST,fontsize=14,weight='bold',va='center')
ax.set_ylabel('Reasoning suite avg. (16K)',fontsize=15)
ax.legend(handles=[Line2D([],[],color=NAVY,lw=3,marker='o',ms=10,label='Front-loaded'),
                   Line2D([],[],color=NAVY,lw=3,ls='--',marker='o',mfc='white',mew=2.2,ms=10,label='Without front-loading'),
                   Line2D([],[],color=RUST,lw=2.4,marker='o',ms=9,label='MixtureVitae (front-loaded)'),
                   Line2D([],[],color=NAVY,lw=1.2,alpha=0.3,label='individual datasets')],
          loc='lower left',bbox_to_anchor=(0,1.04),ncol=2,frameon=False,fontsize=13)
fig.tight_layout(); fig.savefig(out+'/draft_stages_mean.png',facecolor='white'); plt.close(fig)
print('ok')
