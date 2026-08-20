#!/usr/bin/env python3
"""Two dedicated figures for the dissertation supplement."""
import csv, datetime, sys
import numpy as np
sys.path.insert(0, '/root/work/rasti/repo/analysis')
import _paths  # noqa
from pilot_proxy.plot_style import setup_matplotlib
plt = setup_matplotlib()

# ---------- Fig S1: ch30 two-population dissection --------------------------
z = np.load(_paths.PERFRAME)
s = {int(r['atsc_channel']): r for r in
     csv.DictReader(open(_paths.OUT / 'empirical_zero_points.csv'))}[30]
mu0 = float(s['mu0_analytic'])
pt = z['ch30_p_target_u64'].astype(np.float64)
pr = z['ch30_p_ref_sum_u64'].astype(np.float64)
ok = z['ch30_valid'].astype(bool)
with np.errstate(divide='ignore', invalid='ignore'):
    f = 2.0 * pt / pr
ok &= np.isfinite(f)
F = f[ok] / mu0
fui = z['ch30_frame_unit_index'][ok]
t0 = z['ch30_unit_time0_ctime']

fig, (a, b) = plt.subplots(1, 2, figsize=(9.2, 3.6),
                           gridspec_kw={'width_ratios': [1.15, 1]})
bins = np.geomspace(0.7, 14.5, 160)
a.hist(F, bins=bins, color='0.35', lw=0)
a.axvspan(0.7, 2.0, color='#0072B2', alpha=0.10, lw=0)
a.axvline(1.0, color='#D55E00', lw=1.0, ls='--')
a.set_xscale('log'); a.set_yscale('log')
a.set_xlabel(r'$F/\mu_0^{\rm analytic}$')
a.set_ylabel('frames')
a.set_title('(a) ch30: two populations, empty gap', fontsize=10)
a.annotate('on-air clump\n96.3% at $11.7\\times\\mu_0$', xy=(11.7, 900),
           xytext=(3.2, 700), fontsize=8,
           arrowprops=dict(arrowstyle='->', lw=0.8))
a.annotate('off-air minority\n3.46%, centred at $\\mu_0$', xy=(1.0, 60),
           xytext=(1.6, 12), fontsize=8,
           arrowprops=dict(arrowstyle='->', lw=0.8))
a.grid(color='0.93', lw=0.4); a.set_axisbelow(True)

low_units = [u for u in np.unique(fui) if (F[fui == u] < 2).all()]
d0 = datetime.date(2019, 1, 1)
xs, ys, es = [], [], []
for u in low_units:
    x = F[fui == u]
    d = datetime.datetime.utcfromtimestamp(t0[u]).date()
    xs.append((d - d0).days)
    ys.append(x.mean())
    es.append(x.std(ddof=1) if x.size > 1 else 0.0)
b.axhspan(1 - 6e-3, 1 + 6e-3, color='#D55E00', alpha=0.15, lw=0,
          label=r'core window $\pm 6\times10^{-3}$')
b.axhspan(1 - 2.39e-3, 1 + 2.39e-3, color='#D55E00', alpha=0.30, lw=0,
          label='ideal null width')
b.errorbar(xs, ys, yerr=es, fmt='o', ms=3.5, lw=0, elinewidth=0.8,
           capsize=2, color='#0072B2', label='off-air capture mean $\\pm$ std')
b.set_xlabel('days since 2019-01-01')
b.set_ylabel(r'$F/\mu_0^{\rm analytic}$')
b.set_title('(b) the 38 off-air captures (Apr 6--25 + Oct 23, 2019)',
            fontsize=10)
b.legend(fontsize=7, loc='upper right')
b.grid(color='0.93', lw=0.4); b.set_axisbelow(True)
fig.tight_layout()
fig.savefig('figs/figS_ch30_two_population.pdf', bbox_inches='tight')
print('wrote figS_ch30_two_population.pdf')

# ---------- Fig S2: T2 generator startup transient --------------------------
blocks = [1.038998e-3, 8.842038e-3, 9.551332e-3, 9.634961e-3, 9.601829e-3,
          9.654954e-3, 9.520722e-3, 9.862883e-3, 9.997592e-3, 9.906840e-3]
stat = np.mean(blocks[2:])
fig, ax = plt.subplots(figsize=(6.4, 3.2))
db = 10 * np.log10(np.array(blocks) / stat)
ax.bar(range(10), db, color=['#D55E00', '#E69F00'] + ['#0072B2'] * 8,
       width=0.7)
ax.axhline(0, color='0.4', lw=0.8)
for i, v in enumerate(db):
    ax.text(i, v - 0.55 if v < -1 else v + 0.12, f'{v:+.2f}',
            ha='center', fontsize=7)
ax.set_xticks(range(10))
ax.set_xlabel('tenth-of-capture block (60k samples $\\approx$ 11 ms each)')
ax.set_ylabel('pilot $|A|^2$ vs stationary mean [dB]')
ax.set_title('Golden-capture generator startup transient (T2 resolution): '
             'blocks 2--9 stationary', fontsize=9.5)
ax.grid(axis='y', color='0.93', lw=0.4); ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig('figs/figS_t2_block_profile.pdf', bbox_inches='tight')
print('wrote figS_t2_block_profile.pdf')
