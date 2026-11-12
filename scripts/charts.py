import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, sys
from matplotlib.patches import Patch
out = sys.argv[1]
FIG = (7.2, 7.8)
NAVY='#3b5a80'; NAVY_L='#c7d4e2'; RUST='#c0532b'; RUST_L='#f0b07a'; PURP='#6a4c9c'; PURP_L='#d9c9ea'; GRAY='#555'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':20,'axes.spines.top':False,'axes.spines.right':False,
  'axes.edgecolor':'#222','axes.linewidth':1.2,'ytick.color':'#222','xtick.color':'#222'})
LEG = dict(loc='lower left', frameon=False, fontsize=18.5, ncol=2, bbox_to_anchor=(-0.02, 1.0), handlelength=1.2, columnspacing=1.2)

# Chart 1: Phase 2 change in suite average (Table 2)
fig, ax = plt.subplots(figsize=FIG, dpi=300)
names = ['MV', 'Comma', 'Nemotron', 'FW-Edu']
wo = [None, (-4.0,-5.1,-3.0), (-1.3,-2.0,-0.6), (-1.3,-2.3,-0.5)]
en = [(10.7,8.2,13.2), (15.8,13.2,18.4), (14.2,11.6,16.7), (13.3,10.7,16.0)]
light = [RUST_L, PURP_L, NAVY_L, NAVY_L]; dark = [RUST, PURP, NAVY, NAVY]
x = np.arange(4); w = 0.36
ax.grid(axis='y', color='#e6e6e6', lw=1); ax.set_axisbelow(True)
for i in range(4):
    if wo[i]:
        v, lo, hi = wo[i]; xx = x[i]-w/2-0.01
        ax.bar(xx, v, w, color=light[i]); ax.errorbar(xx, v, yerr=[[v-lo],[hi-v]], color=GRAY, capsize=4, lw=1.5)
        ax.text(xx, lo-0.8, f'{v:+.1f}', ha='center', va='top', color=GRAY, fontsize=19, style='italic')
    v, lo, hi = en[i]; xx = x[i]+w/2+0.01
    ax.bar(xx, v, w, color=dark[i]); ax.errorbar(xx, v, yerr=[[v-lo],[hi-v]], color=GRAY, capsize=4, lw=1.5)
    ax.text(xx, hi+0.5, f'{v:+.1f}', ha='center', va='bottom', color=(RUST if i == 0 else GRAY), fontsize=19, style='italic')
ax.axhline(0, color='#222', lw=1.2)
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=21); ax.tick_params(axis='x', length=0, pad=8)
ax.set_ylabel('Δ suite avg. (pts)', fontsize=20); ax.set_ylim(-7.5, 21)
ax.legend(handles=[Patch(color=NAVY_L, label='Without the subset'), Patch(color=NAVY, label='Enriched'),
                   Patch(color=RUST, label='MV (permissive)'), Patch(color=PURP, label='Comma (permissive)')], **LEG)
ax.spines['bottom'].set_visible(False)
fig.tight_layout(); fig.savefig(out+'/phase2_delta.png', facecolor='white'); plt.close(fig)

# Chart 2: MATH500 gain per reasoning corpus (Table 4, 287-problem subset)
corp = ['Open-\nThoughts3', 'Ace-\nReason', 'Nemotron-\nCascade', 'Superior-\nReasoning']
data = {'MixtureVitae': [(41.9,37.6,46.5),(38.7,34.3,43.1),(38.4,34.0,42.5),(26.6,22.5,30.8)],
        'Comma0.1': [(-0.1,-1.4,1.2),(0.5,-0.8,1.7),(1.6,0.3,3.0),(0.5,-0.8,1.7)],
        'Nemotron-CC-HQ': [(0.5,-0.7,1.5),(1.5,0.0,3.1),(0.9,-0.6,2.3),(0.5,-0.7,1.6)],
        'FineWeb-Edu': [(0.0,-0.9,0.8),(1.0,0.0,2.2),(0.9,-0.1,2.0),(1.3,0.1,2.6)]}
cols = [RUST, PURP, NAVY, '#8fa5bf']
fig, ax = plt.subplots(figsize=FIG, dpi=300)
ax.grid(axis='y', color='#e6e6e6', lw=1); ax.set_axisbelow(True)
x = np.arange(4); w = 0.2
for j, (k, vals) in enumerate(data.items()):
    off = (j-1.5)*w
    for i, (v, lo, hi) in enumerate(vals):
        ax.bar(x[i]+off, v, w*0.92, color=cols[j], label=k if i == 0 else None)
        ax.errorbar(x[i]+off, v, yerr=[[v-lo],[hi-v]], color=GRAY, capsize=2.5, lw=1.2)
        if j == 0: ax.text(x[i]+off, hi+0.8, f'+{v:.1f}', ha='center', va='bottom', color=RUST, fontsize=19, style='italic')
ax.axhline(0, color='#222', lw=1.2)
ax.set_xticks(x); ax.set_xticklabels(corp, fontsize=17); ax.tick_params(axis='x', length=0, pad=8)
ax.set_ylabel('Δ MATH500 (pts)', fontsize=20); ax.set_ylim(-3, 52)
ax.legend(**LEG)
ax.spines['bottom'].set_visible(False)
fig.tight_layout(); fig.savefig(out+'/corpora_math500.png', facecolor='white'); plt.close(fig)
print('done')
