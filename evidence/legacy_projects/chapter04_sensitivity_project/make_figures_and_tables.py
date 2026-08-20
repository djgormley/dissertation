from __future__ import annotations

import json, math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'figures'
TAB = ROOT / 'tables'
DAT = ROOT / 'data'
for d in (FIG, TAB, DAT):
    d.mkdir(exist_ok=True)

# Detector constants for this dissertation chapter.
K = 128
M = 1_048_576
DF1 = 2*M
DF2 = 4*M
FINE_BIN_HZ = 3051.7578125
HALF_BIN_HZ = FINE_BIN_HZ/2
GUARD = 4
REF_OFFSET_HZ = GUARD*FINE_BIN_HZ
PFA0 = 1e-3
THRESH = 1.0037122049331666
NTRIALS = 12_000
N_SHELF = 16
PILOT_TO_INTEGRATED_DATA_DB = -11.7
PILOT_TO_SHELF_PER_BIN_DB = PILOT_TO_INTEGRATED_DATA_DB + 10*math.log10(N_SHELF)

csv_path = DAT / 'fig04_detection_sensitivity.csv'
npz_path = DAT / 'fig04_detection_sensitivity.npz'
df = pd.read_csv(csv_path)
npz = np.load(npz_path)
pfa_grid = np.array(npz['pfa_grid'], dtype=float)
heat_snr = np.array(npz['heat_snr'], dtype=float)
heat_pd = np.array(npz['heat_pd'], dtype=float)

LABELS = {
    '3sigma': r'$P_D=0.9986501$',
    '4sigma': r'$P_D=0.9999683$',
    '5sigma': r'$P_D=0.9999997$',
    '6sigma': r'$P_D=0.9999999$',
}

# ---------- plotting helpers ----------
def savefig(name: str):
    plt.tight_layout()
    plt.savefig(FIG / f'{name}.png', dpi=220)
    plt.savefig(FIG / f'{name}.pdf')
    plt.close()

def box(ax, x, y, w, h, txt, fontsize=9, fc='white'):
    p = FancyBboxPatch((x,y), w,h, boxstyle='round,pad=0.02,rounding_size=0.02',
                       linewidth=1.2, edgecolor='black', facecolor=fc)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, txt, ha='center', va='center', fontsize=fontsize)

def arrow(ax, start, end, rad=0.0):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=12,
                                 linewidth=1.2, color='black', connectionstyle=f'arc3,rad={rad}'))

# ---------- figures ----------
# 1 roadmap
fig, ax = plt.subplots(figsize=(10.5, 5.3)); ax.set_axis_off()
items = [
    ('Signal model','noise + shelf + pilot'),('SNR convention','data-shelf dB/bin'),
    ('Pilot normalization','-11.7 dB integrated data'),('Injection grid','SNR x P_FA x trials'),
    ('H1 model','noncentral F statistic'),('Sensitivity curves','P_D vs SNR and P_FA'),
    ('Scaling diagnostics','M, K, offset, pilot ratio'),('Artifacts','CSV/NPZ/JSON provenance')]
coords = [(0.04,0.66),(0.29,0.66),(0.54,0.66),(0.79,0.66),(0.04,0.29),(0.29,0.29),(0.54,0.29),(0.79,0.29)]
for (a,b),(x,y) in zip(items,coords): box(ax,x,y,0.18,0.18,f'{a}\n{b}',fontsize=8.5)
for i in range(3): arrow(ax,(coords[i][0]+0.18,coords[i][1]+0.09),(coords[i+1][0],coords[i+1][1]+0.09))
arrow(ax,(0.88,0.66),(0.88,0.48)); arrow(ax,(0.79,0.38),(0.72,0.38))
for i in range(4,7): arrow(ax,(coords[i][0]+0.18,coords[i][1]+0.09),(coords[i+1][0],coords[i+1][1]+0.09))
ax.text(0.5,0.94,'Chapter 4 evidence path: synthetic signal model to detection sensitivity',ha='center',fontsize=13,weight='bold')
savefig('fig04_01_sensitivity_roadmap')

# 2 signal decomposition
f = np.linspace(0, 6, 1200)
noise = np.ones_like(f)
roll_left = 1/(1+np.exp(-(f-0.30)/0.015))
roll_right = 1/(1+np.exp((f-5.75)/0.02))
shelf = 0.055*roll_left*roll_right
pilot = 0.24*np.exp(-0.5*((f-0.309441)/0.018)**2)
fig, ax = plt.subplots(figsize=(10.4,4.5))
ax.plot(f, noise, label='noise floor')
ax.plot(f, noise+shelf, label='noise + DTV data shelf')
ax.plot(f, noise+shelf+pilot, label='noise + shelf + pilot')
ax.axvline(0.309441, ls='--', lw=1.2); ax.text(0.42,1.24,'pilot at 0.309441 MHz',fontsize=9)
ax.set_xlim(0,6); ax.set_ylim(0.95,1.32); ax.set_xlabel('Channel-relative frequency (MHz)'); ax.set_ylabel('Relative power')
ax.set_title('Synthetic ATSC channel components used in sensitivity studies'); ax.grid(alpha=0.3); ax.legend(fontsize=9)
savefig('fig04_02_signal_decomposition')

# 3 normalization diagram
fig, ax = plt.subplots(figsize=(10.4,5.0)); ax.set_axis_off()
box(ax,0.04,0.60,0.18,0.18,'Data shelf\nper fine bin\n$P_{shelf}$')
box(ax,0.31,0.60,0.20,0.18,f'Integrated shelf\n$N_sP_{{shelf}}$\n$N_s={N_SHELF}$')
box(ax,0.60,0.60,0.18,0.18,'Pilot power\n$P_{pilot}$\n-11.7 dB')
box(ax,0.34,0.25,0.24,0.18,'Pilot relative to\nshelf per bin\n+0.341 dB')
arrow(ax,(0.22,0.69),(0.31,0.69)); ax.text(0.245,0.75,r'$\times N_s$',fontsize=11)
arrow(ax,(0.51,0.69),(0.60,0.69)); ax.text(0.525,0.75,r'$\times 10^{-11.7/10}$',fontsize=11)
arrow(ax,(0.69,0.60),(0.55,0.43),rad=-0.1); arrow(ax,(0.40,0.60),(0.44,0.43),rad=0.1)
ax.text(0.5,0.08,r'$10\log_{10}(P_{pilot}/P_{shelf})=-11.7+10\log_{10}(16)=+0.3412$ dB',ha='center',fontsize=12)
ax.text(0.5,0.94,'Pilot-to-shelf normalization used by the injection model',ha='center',fontsize=13,weight='bold')
savefig('fig04_03_pilot_to_shelf_normalization')

# 4 SNR mapping with offsets
snr_shelf = np.linspace(-30,0,301); snr_pilot = snr_shelf + PILOT_TO_SHELF_PER_BIN_DB
fig, ax = plt.subplots(figsize=(9.8,4.8))
ax.plot(snr_shelf, snr_pilot, label='centered pilot')
for off in [1000,2000]:
    resp = np.sinc(off/FINE_BIN_HZ)**2; loss=10*np.log10(resp)
    ax.plot(snr_shelf, snr_pilot+loss, ls='--', label=f'{off} Hz offset')
ax.axvline(-21.699, ls=':', lw=1.3, label='article operating example')
ax.set_xlabel('DTV data-shelf SNR (dB/bin)'); ax.set_ylabel('Effective pilot-row SNR proxy (dB)')
ax.set_title('Mapping from reported shelf SNR to pilot-row SNR'); ax.grid(alpha=0.3); ax.legend(fontsize=9)
savefig('fig04_04_snr_units_conversion')

# 5 heatmap/injection grid
fig, ax = plt.subplots(figsize=(9.6,5.0))
im = ax.imshow(heat_pd, origin='lower', aspect='auto', extent=[heat_snr[0], heat_snr[-1], np.log10(pfa_grid[0]), np.log10(pfa_grid[-1])])
ax.set_xlabel('Injected DTV data-shelf SNR (dB/bin)'); ax.set_ylabel(r'$\log_{10}(P_{FA})$')
ax.set_title('Empirical injection grid used for sensitivity estimates')
cb=fig.colorbar(im,ax=ax); cb.set_label(r'Detection probability $P_D$')
ax.axvline(-21.699,color='white',ls='--',lw=1.1); ax.text(-21.4,np.log10(1.5e-3),'nominal\noperating\npoint',color='white',fontsize=8)
savefig('fig04_05_injection_grid')

# 6 noncentral F construction
fig, ax = plt.subplots(figsize=(10.4,5.2)); ax.set_axis_off()
box(ax,0.04,0.65,0.18,0.17,'Target row\nnoise + pilot')
box(ax,0.04,0.27,0.18,0.17,'Reference rows\nlocal background')
box(ax,0.34,0.65,0.22,0.17,r'$X\sim\chi^2_{2M}(\lambda)$')
box(ax,0.34,0.27,0.22,0.17,r'$Y\sim\chi^2_{4M}$')
box(ax,0.67,0.46,0.24,0.18,r'$T=\frac{X/(2M)}{Y/(4M)}$')
box(ax,0.67,0.18,0.24,0.16,r'$P_D=Pr(T>\eta|H_1)$')
arrow(ax,(0.22,0.735),(0.34,0.735)); arrow(ax,(0.22,0.355),(0.34,0.355)); arrow(ax,(0.56,0.735),(0.67,0.57)); arrow(ax,(0.56,0.355),(0.67,0.51)); arrow(ax,(0.79,0.46),(0.79,0.34))
ax.text(0.48,0.90,r'Under $H_1$, the target numerator becomes noncentral; the reference denominator remains local background.',ha='center',fontsize=10.5)
ax.text(0.34,0.58,r'$\lambda\approx 2M\rho_{pilot,eff}$',fontsize=11)
savefig('fig04_06_noncentral_f_model')

# 8 P_D vs SNR slices
fig, ax = plt.subplots(figsize=(9.3,5.2))
for pfa in [1e-4,3e-4,1e-3,3e-3,1e-2]:
    idx=int(np.argmin(np.abs(pfa_grid-pfa)))
    ax.plot(heat_snr, heat_pd[idx], marker='o', ms=3, label=fr'$P_{{FA}}={pfa_grid[idx]:.0e}$')
ax.set_xlabel('DTV data-shelf SNR (dB/bin)'); ax.set_ylabel(r'Detection probability $P_D$')
ax.set_title('Detection-probability slices through the injection grid'); ax.set_ylim(-0.02,1.02); ax.grid(alpha=0.3); ax.legend(fontsize=9,loc='lower right')
savefig('fig04_08_pd_vs_snr_slices')

# 9 ROC-like curves
fig, ax = plt.subplots(figsize=(9.3,5.2))
for snr in [-25,-23,-22,-21,-20,-18]:
    j=int(np.argmin(np.abs(heat_snr-snr)))
    ax.semilogx(pfa_grid, heat_pd[:,j], marker='o', ms=3, label=f'SNR={heat_snr[j]:.0f} dB/bin')
ax.set_xlabel(r'Target false-alarm probability $P_{FA}$'); ax.set_ylabel(r'Detection probability $P_D$')
ax.set_title('ROC-like operating curves extracted from the injection grid'); ax.set_ylim(-0.02,1.02); ax.grid(alpha=0.3,which='both'); ax.legend(fontsize=8,loc='lower right')
savefig('fig04_09_roc_like_curves')

# 10 required SNR curves
fig, ax = plt.subplots(figsize=(9.3,5.2))
for pd_target, group in df.groupby('pd_target'):
    group=group.sort_values('pfa_target')
    ax.semilogx(group['pfa_target'], group['required_data_snr_db_theory'], marker='o', label=fr'$P_D={pd_target:.7g}$')
ax.axvline(PFA0, ls='--', lw=1.2); ax.set_xlabel(r'Target false-alarm probability $P_{FA}$'); ax.set_ylabel('Required data-shelf SNR (dB/bin)')
ax.set_title('Required SNR for fixed detection-probability targets'); ax.grid(alpha=0.3,which='both'); ax.legend(fontsize=8)
savefig('fig04_10_required_snr_curves')

# 11 finite-trial support
miss_probs=np.logspace(-7,-1,300); expected=NTRIALS*miss_probs
fig, ax = plt.subplots(figsize=(9.3,5.2)); ax.loglog(miss_probs, expected)
ax.axhline(1,ls='--',lw=1.2,label='one expected miss'); ax.axhline(10,ls=':',lw=1.2,label='ten expected misses')
for pd_t in sorted(df['pd_target'].unique()):
    miss=1-pd_t; ax.axvline(miss,ls='--',lw=0.9); ax.text(miss*1.1,0.2,fr'$P_D={pd_t:.4g}$',rotation=90,fontsize=8,va='bottom')
ax.set_xlabel(r'Miss probability $1-P_D$'); ax.set_ylabel('Expected misses in 12,000 trials')
ax.set_title('Finite-trial support for high detection-probability curves'); ax.grid(alpha=0.3,which='both'); ax.legend(fontsize=9)
savefig('fig04_11_finite_trial_support')

# 12 M scaling
base_required=float(df[(np.isclose(df.pfa_target,1e-3)) & (np.isclose(df.pd_target,0.9986501))]['required_data_snr_db_theory'].iloc[0])
M_values=np.array([2**16,2**17,2**18,2**19,2**20,2**21,2**22], dtype=float)
req_M=base_required-5*np.log10(M_values/M)
fig, ax = plt.subplots(figsize=(9.3,5.2)); ax.semilogx(M_values, req_M, marker='o'); ax.axvline(M,ls='--',lw=1.2)
ax.set_xlabel(r'Accumulated projected samples $M$'); ax.set_ylabel('Approximate required shelf SNR (dB/bin)')
ax.set_title('Approximate sensitivity scaling with accumulation length'); ax.grid(alpha=0.3,which='both'); ax.text(M*1.05,base_required+0.1,'current\noperating\npoint',fontsize=9)
savefig('fig04_12_sensitivity_scaling_M')

# 13 offset penalty
offset=np.linspace(0,2500,300); response=np.sinc(offset/FINE_BIN_HZ)**2; loss=-10*np.log10(np.maximum(response,1e-12))
fig, ax = plt.subplots(figsize=(9.3,5.2)); ax.plot(offset,loss); ax.axvline(2000,ls='--',lw=1.2,label='2 kHz design envelope'); ax.axvline(HALF_BIN_HZ,ls=':',lw=1.2,label='half-bin scale')
ax.set_xlabel('Pilot-frequency offset (Hz)'); ax.set_ylabel('Additional required SNR (dB)'); ax.set_title('Frequency-offset penalty under a rectangular fine-bin response'); ax.grid(alpha=0.3); ax.legend(fontsize=9)
savefig('fig04_13_offset_snr_penalty')

# 14 artifact workflow
fig, ax = plt.subplots(figsize=(10.4,5.2)); ax.set_axis_off()
items=[('detector_config.json','K, M, guard, DOF'),('injection_grid.npz','SNR x P_FA trials'),('sensitivity.csv','required SNR curves'),('sensitivity.json','metrics + provenance'),('figures','heatmaps, ROC, tables'),('dissertation text','interpretation + scope')]
xs=[0.03,0.20,0.37,0.54,0.70,0.84]
for x,(a,b) in zip(xs,items): box(ax,x,0.45,0.13,0.19,f'{a}\n{b}',fontsize=8)
for i in range(len(xs)-1): arrow(ax,(xs[i]+0.13,0.545),(xs[i+1],0.545))
ax.text(0.5,0.84,'Sensitivity-analysis artifact chain',ha='center',fontsize=13,weight='bold')
ax.text(0.5,0.20,'Dissertation-scale analyses should preserve arrays for auditability, CSV tables for reading, and JSON for provenance.',ha='center',fontsize=10)
savefig('fig04_14_artifact_workflow')

# ---------- tables ----------
BS = r'\\'

def latex_table(filename, caption, label, colspec, header, rows):
    lines=[]
    lines.append(r'\begin{table}[ht]')
    lines.append(r'\centering')
    lines.append(r'\caption{' + caption + '}')
    lines.append(r'\label{' + label + '}')
    lines.append(r'\begin{tabularx}{\textwidth}{' + colspec + '}' if 'Y' in colspec or 'X' in colspec else r'\begin{tabular}{' + colspec + '}')
    lines.append(r'\toprule')
    lines.append(header + ' ' + BS)
    lines.append(r'\midrule')
    for row in rows:
        lines.append(' & '.join(row) + ' ' + BS)
    lines.append(r'\bottomrule')
    lines.append(r'\end{tabularx}' if 'Y' in colspec or 'X' in colspec else r'\end{tabular}')
    lines.append(r'\end{table}')
    (TAB/filename).write_text('\n'.join(lines), encoding='utf-8')

latex_table('tab04_01_signal_model.tex','Signal-model quantities used in the synthetic sensitivity chapter.','tab:signal-model-quantities','l l Y',
            'Quantity & Symbol & Definition',
            [('Noise power per fine bin',r'$P_N$','Local thermal/instrumental background power used to define SNR.'),
             ('Data-shelf power per fine bin',r'$P_{\rm shelf}$','Mean DTV data-shelf power per fine bin in the injected channel.'),
             ('Reported shelf SNR',r'$\gamma_{\rm shelf}$',r'$P_{\rm shelf}/P_N$; plotted in dB/bin.'),
             ('Pilot power',r'$P_{\rm pilot}$','Narrow ATSC pilot power implied by the pilot-to-integrated-data convention.'),
             ('Effective pilot SNR',r'$\gamma_{\rm pilot,eff}$','Pilot SNR after pilot-to-shelf conversion and frequency-offset response loss.'),
             ('Detector statistic',r'$T$',r'$2P_T/(P_{R-}+P_{R+})$.'),
             ('Detection probability',r'$P_D$',r'$\Pr(T>\eta\mid H_1)$ for a chosen signal model.')])

latex_table('tab04_02_pilot_normalization.tex','Pilot-to-shelf normalization used for the current sensitivity examples.','tab:pilot-normalization','l r',
            'Quantity & Value',
            [('Data-shelf support used in the injection convention',f'{N_SHELF} fine bins'),
             ('Pilot power relative to integrated data power',f'{PILOT_TO_INTEGRATED_DATA_DB:.1f} dB'),
             (r'$10\log_{10}(16)$',f'{10*math.log10(N_SHELF):.4f} dB'),
             ('Pilot power relative to shelf power per fine bin',f'{PILOT_TO_SHELF_PER_BIN_DB:.4f} dB'),
             ('Current fine-bin width',f'{FINE_BIN_HZ:.4f} Hz'),
             ('Representative offset design envelope','2000 Hz')])

latex_table('tab04_03_injection_grid.tex','Current injection-grid summary for the article-scale sensitivity product.','tab:injection-grid','l r',
            'Quantity & Value',
            [('Detector fine-bin factor',rf'$K={K}$'),
             ('Accumulated projected samples',rf'$M={M:,}$'),
             ('Target/reference guard',f'{GUARD} fine bins'),
             ('Fine-bin width',f'{FINE_BIN_HZ:.2f} Hz'),
             ('SNR grid range',f'{heat_snr.min():.0f} to {heat_snr.max():.0f} dB/bin'),
             ('Number of SNR grid points',str(len(heat_snr))),
             (r'Number of $P_{FA}$ grid points',str(len(pfa_grid))),
             ('Injection trials per grid cell','12,000'),
             ('Default operating threshold',rf'$\eta={THRESH:.16f}$')])

req_rows=[]
for _,r in df[np.isclose(df.pfa_target,1e-3)].sort_values('pd_target').iterrows():
    req_rows.append((rf'${r["pd_target"]:.7g}$', f'{r["required_data_snr_db_theory"]:.3f}', f'{r["required_data_snr_db_empirical"]:.3f}', f'{r["pd_empirical_at_required_snr"]:.6f}', f'{int(r["hits"])}/{int(r["trial_count"])}'))
latex_table('tab04_04_required_snr_operating_point.tex',r'Required data-shelf SNR at the representative operating threshold $P_{FA}=10^{-3}$.','tab:required-snr-operating-point','l r r r r',
            r'Target $P_D$ & Theory SNR & Empirical SNR & Empirical $P_D$ & Hits/trials',req_rows)

ft_rows=[]
for pd_t in sorted(df['pd_target'].unique()):
    miss=1-pd_t; expected=NTRIALS*miss
    interp='empirically supported' if expected>=10 else 'model-supported / saturated'
    ft_rows.append((rf'${pd_t:.7g}$',f'{miss:.3e}',f'{expected:.3f}',interp))
latex_table('tab04_05_finite_trial_support.tex','Finite-trial support for high detection-probability targets in a 12,000-trial injection grid.','tab:finite-trial-support','l r r l',
            r'Target $P_D$ & Miss probability & Expected misses & Interpretation',ft_rows)

latex_table('tab04_06_scaling_laws.tex','Sensitivity-scaling relationships used as design diagnostics. These are not substitutes for injection tests, but they indicate which variables control the operating point.','tab:scaling-laws','l l Y',
            'Effect & Approximate dependence & Interpretation',
            [('Accumulation length',r'required weak-signal power $\propto M^{-1/2}$','Larger $M$ tightens the null distribution and lowers required pilot power, at the cost of latency and buffer requirements.'),
             ('Pilot-to-shelf convention',r'$\gamma_{pilot}=N_s10^{-11.7/10}\gamma_{shelf}$','Changing the assumed shelf support or pilot ratio shifts the reported data-shelf SNR scale.'),
             ('Frequency offset',r'$\gamma_{eff}=\gamma_{pilot}|H(\Delta f)|^2$','A shifted pilot pays an SNR penalty determined by the fine-bin/PFB response.'),
             ('Fine-bin factor',r'$\Delta f=\Delta f_{coarse}/K$','Larger $K$ improves spectral localization but narrows offset tolerance and increases compute.'),
             ('Guard spacing','reference leakage decreases with guard','Wider guards reduce pilot leakage into references but may make the background estimate less local.')])

latex_table('tab04_07_artifacts.tex','Recommended dissertation sensitivity artifacts.','tab:sensitivity-artifacts','l l Y',
            'Artifact & Format & Purpose',
            [(r'injection\_grid\_results','NPZ',r'Stores raw $P_D({\rm SNR},P_{FA})$ arrays and trial counts.'),
             (r'required\_snr\_table','CSV/JSON',r'Supports fixed-$P_D$ threshold curves and dissertation tables.'),
             (r'roc\_curves','CSV','Detector operating curves at fixed injected SNR.'),
             (r'normalization\_manifest','JSON','Records pilot-to-shelf conversion, shelf support, offset response, and score floor.'),
             (r'sensitivity\_scaling','CSV/JSON',r'Records $M$, $K$, pilot-offset, and pilot-ratio sensitivity sweeps.'),
             (r'figure\_manifest','JSON','Connects figures to data products, code version, and detector configuration.')])

summary={'K':K,'M':M,'df1':DF1,'df2':DF2,'fine_bin_hz':FINE_BIN_HZ,'pfa_default':PFA0,'threshold_fstat':THRESH,'pilot_to_integrated_data_db':PILOT_TO_INTEGRATED_DATA_DB,'shelf_bins':N_SHELF,'pilot_to_shelf_per_bin_db':PILOT_TO_SHELF_PER_BIN_DB,'trial_count_per_grid_cell':NTRIALS}
(DAT/'chapter04_sensitivity_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('Generated Chapter 4 figures and tables')
# Additional K-design trade figure required by the chapter text.
K_vals = np.array([32, 64, 128, 256, 512])
fine_vals = 390625.0 / K_vals
half_vals = fine_vals / 2.0
ref4_vals = 4.0 * fine_vals
fig, ax = plt.subplots(figsize=(8.8, 5.0))
ax.plot(K_vals, fine_vals/1000.0, marker='o', label='Fine-bin width')
ax.plot(K_vals, half_vals/1000.0, marker='s', label='Half-bin scale')
ax.plot(K_vals, ref4_vals/1000.0, marker='^', label='Guard=4 reference offset')
ax.axhline(2.0, color='r', ls='--', lw=1.2, label='2 kHz offset envelope')
ax.axhline(4.0, color='0.4', ls=':', lw=1.0, label='4 kHz target resolution')
ax.axvline(128, color='k', ls=':', lw=1.0)
ax.text(132, max(ref4_vals/1000.0)*0.72, 'selected\nK=128', fontsize=9, va='center')
ax.set_xscale('log', base=2)
ax.set_xticks(K_vals)
ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
ax.set_xlabel('Fine-bin factor K')
ax.set_ylabel('Frequency scale (kHz)')
ax.set_title('Fine-bin factor tradeoff for the current detector')
ax.grid(alpha=0.3, which='both')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(FIG/'fig04_09_K_trade.png', dpi=220)
fig.savefig(FIG/'fig04_09_K_trade.pdf')
plt.close(fig)
