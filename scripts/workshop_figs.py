# Figures for the workshop poster (data from the workshop paper, Tables 1, 3 and 4).
# usage: python workshop_figs.py <outdir>
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, sys
from matplotlib.lines import Line2D
out = sys.argv[1]
NAVY='#3b5a80'; RUST='#c0532b'; PURP='#6a4c9c'; TEAL='#2f8a7a'; NAVY_L='#8fa5bf'; GRAY='#555'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':17,'axes.spines.top':False,'axes.spines.right':False,
  'axes.edgecolor':'#222','axes.linewidth':1.2})

def seg(ax, X, ys, col, dashed=False, lw=3.5, ms=12):
    ax.plot(X, ys, color=col, lw=lw, ls='--' if dashed else '-', alpha=.75 if dashed else 1, zorder=3)
    ax.plot(X, ys, 'o', ms=ms, color='white' if dashed else col, mec=col, mew=2.2, alpha=.75 if dashed else 1, zorder=4, ls='none')

def gap(ax, x, lo, hi, txt, big=False):
    ax.annotate('', xy=(x, hi), xytext=(x, lo), arrowprops=dict(arrowstyle='<->', color=GRAY, lw=2.4 if big else 1.6, shrinkA=6, shrinkB=6), zorder=2)
    ax.text(x+0.07, (lo+hi)/2, txt, ha='left', va='center', fontsize=20 if big else 17, color=GRAY, weight='bold' if big else 'normal')

# ---------- Figure 1: factorial, 16K, Protocol A (Table 1) ----------
D = {'MixtureVitae (permissive)': (RUST, [30.7,27.3,27.8], [11.6,11.8,12.0]),
     'Nemotron-CC-HQ':            (NAVY, [27.3,22.3,22.7], [8.1,8.4,8.6]),
     'FineWeb-Edu':               (NAVY, [27.1,22.6,22.1], [8.1,7.9,8.5])}
X = [0, 1, 2]
fig, axs = plt.subplots(1, 3, figsize=(9.2, 7.4), dpi=300, sharey=True)
for ax, (name, (c, en, wo)) in zip(axs, D.items()):
    ax.set_xticks(X); ax.set_xticklabels(['Base', 'Tulu3\nSFT', 'Tulu3\nDPO'], fontsize=16); ax.tick_params(axis='x', length=0, pad=6)
    ax.set_xlim(-0.35, 2.55); ax.set_ylim(0, 35); ax.grid(axis='y', color='#ececec', lw=1); ax.set_axisbelow(True)
    seg(ax, X, wo, c, dashed=True); seg(ax, X, en, c)
    gap(ax, 1.12, wo[1], en[1], f'+{en[1]-wo[1]:.1f}', big=True)
    ax.set_title(name.replace(' (', '\n('), fontsize=17, color=c if c != NAVY else '#222', weight='bold', pad=12)
axs[0].set_ylabel('Reasoning suite avg. (16K)', fontsize=17)
fig.legend(handles=[Line2D([], [], color='#444', lw=3, marker='o', ms=10, label='Front-loaded'),
                    Line2D([], [], color='#444', lw=3, ls='--', marker='o', mfc='white', mew=2.2, ms=10, label='Without front-loading')],
           loc='upper center', ncol=2, frameon=False, fontsize=17, bbox_to_anchor=(0.5, 1.01))
fig.tight_layout(rect=(0, 0, 1, 0.92)); fig.savefig(out+'/factorial.png', facecolor='white'); plt.close(fig)

# ---------- Figure 2: receptivity (Tables 3 and 4, Protocol B) ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 6.6), dpi=300, gridspec_kw=dict(width_ratios=[1, 1.75]))
# left: OT3 removal ablation
a1.set_xticks([0, 1]); a1.set_xticklabels(['Base', '+ reasoning\nSFT (OT3-30K)'], fontsize=15.5); a1.tick_params(axis='x', length=0, pad=6)
a1.set_xlim(-0.3, 1.75); a1.set_ylim(15, 37); a1.set_yticks([15,20,25,30,35]); a1.grid(axis='y', color='#ececec', lw=1); a1.set_axisbelow(True)
seg(a1, [0, 1], [26.2, 33.6], RUST); seg(a1, [0, 1], [22.5, 23.9], RUST, dashed=True)
a1.text(1.1, 33.6, '+7.4', color=RUST, fontsize=20, weight='bold', va='center')
a1.text(1.1, 23.9, '+1.4', color=GRAY, fontsize=20, weight='bold', va='center')
a1.set_ylabel('Reasoning suite avg.', fontsize=16)
a1.set_title('OT3 in pretraining?', fontsize=17, weight='bold', pad=12)
a1.legend(handles=[Line2D([], [], color=RUST, lw=3, marker='o', ms=9, label='kept'),
                   Line2D([], [], color=RUST, lw=3, ls='--', marker='o', mfc='white', mew=2, ms=9, alpha=.75, label='removed')],
          loc='lower right', frameon=False, fontsize=15, handlelength=1.8)
# right: MATH500 change per reasoning corpus
corp = ['Open-\nThoughts3', 'Ace-\nReason', 'Nemotron-\nCascade', 'Superior-\nReasoning']
data = {'MixtureVitae': (RUST, [(35.4,30.4,40.4),(34.2,29.4,38.8),(31.6,27.0,36.4),(16.4,11.2,21.4)]),
        'SmolLM2': (TEAL, [(-0.6,-3.4,2.2),(8.4,5.0,11.8),(6.6,3.2,10.2),(5.6,2.2,9.0)]),
        'Comma0.1': (PURP, [(-0.4,-2.2,1.4),(0.4,-1.4,2.2),(0.8,-1.2,2.8),(0.0,-1.6,1.6)]),
        'Nemotron-CC-HQ': (NAVY, [(-2.2,-3.8,-0.8),(0.0,-2.0,2.0),(-0.8,-2.6,1.0),(-1.0,-2.8,0.8)]),
        'FineWeb-Edu': (NAVY_L, [(-0.2,-1.6,1.2),(1.0,-0.4,2.6),(0.6,-1.0,2.2),(-0.8,-2.0,0.4)])}
x = np.arange(4); w = 0.16
a2.grid(axis='y', color='#e6e6e6', lw=1); a2.set_axisbelow(True)
for j, (k, (c, vals)) in enumerate(data.items()):
    off = (j-2)*w
    for i, (v, lo, hi) in enumerate(vals):
        a2.bar(x[i]+off, v, w*0.9, color=c, label=k if i == 0 else None)
        a2.errorbar(x[i]+off, v, yerr=[[v-lo], [hi-v]], color=GRAY, capsize=2, lw=1.1)
        if j == 0: a2.text(x[i]+off, hi+0.8, f'+{v:.0f}', ha='center', va='bottom', color=RUST, fontsize=15, weight='bold')
a2.axhline(0, color='#222', lw=1.2); a2.spines['bottom'].set_visible(False)
a2.set_xticks(x); a2.set_xticklabels(corp, fontsize=13.5); a2.tick_params(axis='x', length=0, pad=6)
a2.set_ylabel('Δ MATH500 (pts)', fontsize=16); a2.set_ylim(-5, 60); a2.set_yticks([0,10,20,30,40])
a2.set_title('Reasoning SFT corpus', fontsize=17, weight='bold', pad=12)
a2.legend(loc='upper right', frameon=False, fontsize=12.5, ncol=2, handlelength=1, borderaxespad=0.1)
fig.tight_layout(w_pad=2.5); fig.savefig(out+'/receptivity.png', facecolor='white'); plt.close(fig)
print('ok')
