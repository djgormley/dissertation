#!/usr/bin/env python3
"""Instrument-tone gallery: each tone marked, identified, and its adaptive
notch extent shown, for the dissertation ledger."""
import csv, sys
import numpy as np
from scipy.ndimage import median_filter
sys.path.insert(0, '/root/work/rasti/repo/analysis')
import _paths  # noqa
from pilot_proxy.plot_style import setup_matplotlib
plt = setup_matplotlib()

SR = 390625.0; NB = 16384; BINW = SR / NB
FRACS = {"-SR/5": -SR/5, "+SR/5": SR/5, "-SR/3": -SR/3, "+SR/3": SR/3,
         "-2SR/5": -2*SR/5, "+2SR/5": 2*SR/5}
z = np.load(_paths.SPECTRA)
tones = list(csv.DictReader(open(_paths.OUT / 'instrument_tones.csv')))

fig, axes = plt.subplots(2, 3, figsize=(10.2, 5.6), sharey=False)
for ax, t in zip(axes.flat, tones):
    ch = int(t['atsc_channel']); fbb = float(t['f_bb_hz'])
    ident = t['identification']
    spec = z[f'ch{ch}_before'].astype(np.float64)
    ldb = 10*np.log10(np.maximum(spec, 1e-30))
    bg = median_filter(ldb, size=401, mode='wrap')
    exc = ldb - bg
    c = int(round(fbb / BINW)) % NB
    o = np.arange(-25, 26)
    ax.plot(o * BINW, [exc[(c+i) % NB] for i in o], color='0.25', lw=0.9)
    ax.axhline(0, color='0.75', lw=0.6)
    if t['action'] != 'retained':
        g0 = g1 = c
        while exc[(g0-1) % NB] > 4.0: g0 -= 1
        while exc[(g1+1) % NB] > 4.0: g1 += 1
        i0, i1 = g0, g1
        while i0 > g0-15 and exc[(i0-1) % NB] > 0.5: i0 -= 1
        while i1 < g1+15 and exc[(i1+1) % NB] > 0.5: i1 += 1
        i0 -= 3; i1 += 3
        ax.axvspan((i0-c)*BINW, (i1-c)*BINW, color='#D55E00', alpha=0.15,
                   lw=0, label=f'notch [{i0-c:+d},{i1-c:+d}] bins')
        frac = FRACS.get(ident.replace('SR', 'SR'), None)
        dfrac = abs(fbb - frac) if frac else float('nan')
        sub = f'$|f - {ident}| = {dfrac:.1f}$ Hz'
    else:
        sub = 'unidentified --- retained, not excised'
    ax.set_title(f"ch{ch}: {t['prominence_db_before']} dB at "
                 f"{fbb/1e3:+.3f} kHz ({ident})\n{sub}", fontsize=8)
    ax.legend(fontsize=6.5, loc='upper right') if t['action'] != 'retained' else None
    ax.grid(color='0.93', lw=0.4); ax.set_axisbelow(True)
    ax.set_xlabel('offset from tone [Hz]', fontsize=7.5)
    ax.set_ylabel('dB above background', fontsize=7.5)
    ax.tick_params(labelsize=7)
fig.suptitle('The six narrow lines outside the detector cells: five clock-fraction '
             'spurs (adaptive notch shown), one retained unknown\n'
             r'(mask-invariant prominence $\Delta \leq 0.3$ dB under the analytic mask'
             ' --- not sky-correlated; nearest line 73.6 kHz from any cell)',
             fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.90))
fig.savefig('figs/figS_tone_gallery.pdf', bbox_inches='tight')
print('wrote figS_tone_gallery.pdf')
