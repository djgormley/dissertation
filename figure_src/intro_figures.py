"""Pedagogical figures for Chapter 1."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
from scipy.interpolate import interp1d
from scipy.stats import norm

from . import style
from .io_utils import OUT, read_csv, columns


def fig_claim_chain() -> Path:
    fig, ax = plt.subplots(figsize=(style.TEXT_WIDTH, 2.72)); ax.set_axis_off()
    ax.text(0.02,0.95,r"\textbf{Evidence chain and claim boundary}",transform=ax.transAxes,
            ha="left",va="top",fontsize=10.2)
    ax.text(0.02,0.875,r"Colour marks what is auditable, what is modelled, and what stays conditional.",
            transform=ax.transAxes,ha="left",va="top",fontsize=8.0,color=style.MUTED)
    # Uniform widths on a .16 pitch, leaving a real .035 gap so each box draws
    # its own rounded outline and the connectors have somewhere to live.
    xs=[0.02,0.18,0.34,0.50,0.66,0.82]; ws=[.125]*6
    boxes=[
        ("Broadcast\nstandard","specified\nfrequency\nand waveform\nfacts","measured"),
        ("Exact\ndetector","integer\nprojection,\ntransform,\nand decision","measured"),
        ("Triggered\narchive","recorded\ndetector\nterms and\nprovenance","measured"),
        ("Calibration\ntransfer","pilot to\nshelf; power\nproxy to\nvisibility","model"),
        ("Fisher\nforecast","bias\ntolerance,\ntime cost,\nmode cuts","model"),
        ("Channel\nverdict","conditional,\nexcision-\nshaped, or\npending","conditional"),
    ]
    for i,((title,body,status),x,w) in enumerate(zip(boxes,xs,ws)):
        style.diagram_box(ax,(x,.45),(w,.34),title=title,body=body,status=status,
                          fontsize=6.3,title_size=7.35)
        if i<len(boxes)-1:
            st="measured" if i<2 else ("model" if i<5 else "conditional")
            style.diagram_arrow(ax,(x+w+.005,.62),(xs[i+1]-.005,.62),status=st)
    # Explicit bracket rather than an arrowstyle whose width is set in points:
    # it has to land exactly on the two model boxes' outer edges.
    gl,gr=xs[3],xs[4]+ws[4]; gy=.415
    ax.plot([gl,gr],[gy,gy],transform=ax.transAxes,color=style.MODEL,lw=.9,clip_on=False)
    for gx in (gl,gr):
        ax.plot([gx,gx],[gy,gy+.022],transform=ax.transAxes,color=style.MODEL,lw=.9,clip_on=False)
    ax.plot([(gl+gr)/2]*2,[gy-.045,gy],transform=ax.transAxes,color=style.MODEL,lw=.9,clip_on=False)
    ax.text((gl+gr)/2,.355,r"load-bearing model gates",transform=ax.transAxes,
            ha="center",va="top",fontsize=7.3,color=style.MODEL)
    ax.text(.02,.10,r"\textbf{Legend:}",transform=ax.transAxes,fontsize=7.7)
    ax.legend(handles=style.status_handles(["measured","model","conditional"]),
              loc="lower left",bbox_to_anchor=(.10,.035),ncol=3,fontsize=7.2,
              columnspacing=1.1,handlelength=1.7)
    return style.save(fig,OUT/"fig_claim_chain.pdf",title="Evidence chain and claim boundary")


def fig_intro_soundwave() -> Path:
    fig, axes = plt.subplots(1,3,figsize=(style.TEXT_WIDTH,2.55),constrained_layout=True)
    titles=[r"overdensity",r"shell launched",r"frozen shell"]
    radii=[.10,.52,.76]
    for i,(ax,title,r) in enumerate(zip(axes,titles,radii)):
        ax.set_aspect("equal"); ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_axis_off()
        ax.add_patch(Circle((0,0),.12,facecolor=style.MEASURED,edgecolor=style.MEASURED,alpha=.92))
        if i>0:
            ax.add_patch(Wedge((0,0),r,0,360,width=.11,facecolor=style.LIGHT_ORANGE,
                               edgecolor=style.MODEL,lw=1.0))
            for ang in np.linspace(0,2*np.pi,8,endpoint=False):
                ax.annotate("",xy=((r+.12)*np.cos(ang),(r+.12)*np.sin(ang)),
                            xytext=((r-.05)*np.cos(ang),(r-.05)*np.sin(ang)),
                            arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.65))
        if i==2:
            ax.text(0,-.93,r"$r_d\simeq147\,\mathrm{Mpc}\;(\simeq150)$",ha="center",fontsize=8.0,color=style.CONDITIONAL)
            ax.plot([0,r],[0,0],color=style.CONDITIONAL,lw=1.2)
        ax.set_title(rf"\textbf{{({chr(97+i)})}} {title}",fontsize=8.0,pad=2)
    fig.text(.5,.015,r"One overdense region, followed from plasma pressure to a frozen matter shell (schematic)",
             ha="center",fontsize=7.5,color=style.MUTED)
    return style.save(fig,OUT/"fig_intro_soundwave.pdf",title="Origin of the BAO ruler")


# Planck-2018 fiducial used by the frozen export (Ch. 9 forecast bank).
_H0 = 0.6766; _OM = 0.3111; _OBH2 = 0.02242; _NS = 0.9665


def _eh98_nowiggle_transfer(k_mpc):
    """Eisenstein & Hu (1998) zero-baryon ('no-wiggle') transfer function,
    eqs. 26-31, for k in Mpc^-1 at the Planck-2018 fiducial."""
    h = _H0; om = _OM; omh2 = om * h * h; ob = _OBH2 / (h * h); fb = ob / om
    theta = 2.7255 / 2.7
    s = 44.5 * np.log(9.83 / omh2) / np.sqrt(1.0 + 10.0 * _OBH2 ** 0.75)   # sound horizon fit, Mpc
    a_g = 1.0 - 0.328 * np.log(431.0 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    gamma = om * h * (a_g + (1.0 - a_g) / (1.0 + (0.43 * k_mpc * s) ** 4))
    q = (k_mpc / h) * theta ** 2 / gamma
    L0 = np.log(2.0 * np.e + 1.8 * q); C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def _nowiggle_r2xi(r_mpc, k_damp=1.5):
    """r^2 xi_nw(r) from the no-wiggle spectrum P_nw ~ k^ns T_nw^2, by direct
    quadrature with a Gaussian small-scale damping that only affects r << 40 Mpc."""
    k = np.logspace(-4, 1, 6000)
    pk = k ** _NS * _eh98_nowiggle_transfer(k) ** 2 * np.exp(-(k / k_damp) ** 2)
    xi = np.array([np.trapezoid(k * k * pk * np.sinc(k * ri / np.pi), k) for ri in r_mpc]) / (2.0 * np.pi ** 2)
    return r_mpc ** 2 * xi


def _smooth_trend(r, y, exclude=(100.0, 195.0)):
    """The physical broadband: the no-wiggle correlation function at the same
    cosmology, amplitude-matched (with a small quadratic correction absorbing the
    EH98-vs-CAMB shape difference) to the data outside the acoustic feature.
    This is the real-space analogue of dividing by P_smooth in Fourier space."""
    mask = (r < exclude[0]) | (r > exclude[1])
    base = _nowiggle_r2xi(r)
    design = np.vstack([base, np.ones_like(r), r, r * r]).T
    coeff, *_ = np.linalg.lstsq(design[mask], y[mask], rcond=None)
    return design @ coeff


def fig_intro_wiggle() -> Path:
    corr=read_csv("intro_wiggle_correlation.csv"); power=read_csv("intro_wiggle_power.csv")
    r,xi=columns(corr,"separation_mpc","r2_xi"); k,ratio=columns(power,"k_mpc_inv","p_over_psmooth")
    trend=_smooth_trend(r,xi); bump=xi-trend
    # Fourier side: the frozen export carries the ratio; the smooth part is the same
    # no-wiggle spectrum used for the broadband in (a), so P = ratio * P_smooth.
    psmooth=k**_NS*_eh98_nowiggle_transfer(k)**2; psmooth=psmooth/psmooth.max()
    scale=k**1.5; scale=scale/np.max(scale*ratio*psmooth)
    fig,axes=plt.subplots(2,2,figsize=(style.TEXT_WIDTH,4.6),constrained_layout=True)
    ax=axes[0,0]; ax.fill_between(r,trend,xi,color=style.MEASURED,alpha=.13,lw=0)
    ax.plot(r,xi,color=style.MEASURED)
    ax.plot(r,trend,color=style.MODEL,ls=(0,(3,2)),lw=.9)
    ax.axvline(150,color=style.PENDING,lw=.7,ls=(0,(2,2)))
    ax.annotate(r"no-wiggle $\xi$ (same cosmology)",xy=(120,np.interp(120,r,trend)),xytext=(108,np.interp(120,r,trend)*0.42),
                fontsize=6.9,color=style.MODEL,arrowprops=dict(arrowstyle="->",lw=.6,color=style.MODEL))
    ax.set_xlabel(r"Separation $r$ [Mpc]"); ax.set_ylabel(r"$r^2\xi(r)$ [arbitrary units]")
    ax.set_xlim(35,205); style.clean_axes(ax); style.panel_label(ax,"a")
    ax.set_title(r"separation, with the smooth part",pad=3)
    ax=axes[0,1]; ax.plot(k,scale*ratio*psmooth,color=style.MEASURED)
    ax.plot(k,scale*psmooth,color=style.MODEL,ls=(0,(3,2)),lw=.9)
    ax.annotate(r"no-wiggle $P$ (same cosmology)",xy=(0.17,np.interp(0.17,k,scale*psmooth)),xytext=(0.04,0.56),
                fontsize=6.9,color=style.MODEL,arrowprops=dict(arrowstyle="->",lw=.6,color=style.MODEL))
    ax.set_ylim(0.45,1.05)
    ax.set_xscale("log"); ax.set_xlim(.035,.5); ax.set_xticks([.04,.06,.1,.2,.3,.5]); ax.set_xticklabels([r"0.04",r"0.06",r"0.1",r"0.2",r"0.3",r"0.5"]); ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel(r"Wavenumber $k$ [Mpc$^{-1}$]"); ax.set_ylabel(r"$k^{3/2}P(k)$ [arbitrary units]")
    style.clean_axes(ax); style.panel_label(ax,"b"); ax.set_title(r"wavenumber, with the smooth part",pad=3)
    ax=axes[1,0]; ax.plot(r,bump,color=style.MEASURED)
    ax.axhline(0,color=style.PENDING,lw=.75)
    ax.axvline(150,color=style.MODEL,ls=(0,(3,2)),lw=.9)
    ax.annotate(r"$\simeq150$ Mpc",xy=(150,np.max(bump)),xytext=(78,np.max(bump)*.9),
                fontsize=7.3,color=style.MODEL,arrowprops=dict(arrowstyle="->",lw=.7,color=style.MODEL))
    ax.set_xlabel(r"Separation $r$ [Mpc]"); ax.set_ylabel(r"$r^2[\xi(r)-\xi_{\rm smooth}(r)]$")
    ax.set_xlim(35,205); style.clean_axes(ax); style.panel_label(ax,"c")
    ax.set_title(r"separation, smooth part subtracted",pad=3)
    ax=axes[1,1]; ax.plot(k,ratio,color=style.MEASURED)
    ax.axhline(1,color=style.PENDING,lw=.75)
    ax.set_xscale("log"); ax.set_xlim(.035,.5); ax.set_xticks([.04,.06,.1,.2,.3,.5]); ax.set_xticklabels([r"0.04",r"0.06",r"0.1",r"0.2",r"0.3",r"0.5"]); ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel(r"Wavenumber $k$ [Mpc$^{-1}$]"); ax.set_ylabel(r"$P(k)/P_{\rm smooth}(k)$")
    style.clean_axes(ax); style.panel_label(ax,"d"); ax.set_title(r"wavenumber, smooth part divided out",pad=3)
    return style.save(fig,OUT/"fig_intro_wiggle.pdf",title="BAO bump and power-spectrum wiggles")


def fig_intro_dilation() -> Path:
    rows=read_csv("intro_wiggle_correlation.csv"); r,y=columns(rows,"separation_mpc","r2_xi")
    power=read_csv("intro_wiggle_power.csv"); k,ratio=columns(power,"k_mpc_inv","p_over_psmooth")
    alpha=1.08; gamma=1.18
    f=interp1d(r,y,bounds_error=False,fill_value="extrapolate")
    baseline=f(r); dilated=f(r/alpha); growth=gamma*baseline
    fig,axes=plt.subplots(1,2,figsize=(style.TEXT_WIDTH,3.05),constrained_layout=True)
    ax=axes[0]
    ax.plot(r,baseline,color=style.INK)
    ax.plot(r,dilated,color=style.MODEL)
    ax.plot(r,growth,color=style.CONDITIONAL,ls=(0,(4,2)))
    for xx,c in [(150,style.INK),(150*alpha,style.MODEL)]: ax.axvline(xx,color=c,lw=.65,ls=(0,(2,2)))
    ax.annotate(r"dilation: \emph{where} the feature sits",xy=(163,np.interp(163,r,dilated)),
                xytext=(98,52),fontsize=7.3,color=style.MODEL,
                arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.7))
    ax.annotate(r"growth: \emph{how high}",xy=(145,np.interp(145,r,growth)),
                xytext=(90,58),fontsize=7.3,color=style.CONDITIONAL,
                arrowprops=dict(arrowstyle="->",color=style.CONDITIONAL,lw=.7))
    ax.set_xlim(85,195); ax.set_ylim(0,64); ax.set_xlabel(r"Separation [Mpc]"); ax.set_ylabel(r"$r^2\xi(r)$")
    style.clean_axes(ax); style.panel_label(ax,"a"); ax.set_title(r"in the correlation function",pad=3)
    ax=axes[1]
    g=interp1d(np.log(k),ratio,bounds_error=False,fill_value=(ratio[0],ratio[-1]))
    fid=g(np.log(k)); dil=g(np.log(alpha*k)); grw=gamma*fid
    # a smooth additive contaminant against the same fixed smooth template: moves the level, not the crests
    contam=fid+0.06*np.exp(-((np.log(k)-np.log(0.06))/0.9)**2)
    h1,=ax.plot(k,fid,color=style.INK,label=r"fiducial")
    h2,=ax.plot(k,dil,color=style.MODEL,label=r"dilation ($\alpha=1.08$): the feature moves")
    h3,=ax.plot(k,grw,color=style.CONDITIONAL,ls=(0,(4,2)),label=r"growth ($\times1.18$): the level moves")
    h4,=ax.plot(k,contam,color=style.FAILURE,ls=(0,(1,1.5)),lw=1.1,label=r"smooth additive residual: the level moves, the feature does not")
    ax.axhline(1,color=style.PENDING,lw=.7)
    ax.set_xscale("log"); ax.set_xlim(.035,.5); ax.set_ylim(.9,1.32)
    ax.set_xlabel(r"Wavenumber $k$ [Mpc$^{-1}$]"); ax.set_ylabel(r"$P(k)/P_{\rm smooth}^{\rm fiducial}(k)$")
    style.clean_axes(ax); style.panel_label(ax,"b"); ax.set_title(r"in the wiggle",pad=3)
    fig.legend(handles=[h1,h2,h3,h4],loc="outside lower center",ncol=2,fontsize=6.8,handlelength=2.0,columnspacing=1.4)
    return style.save(fig,OUT/"fig_intro_dilation.pdf",title="BAO dilation versus growth")


def fig_intro_band() -> Path:
    fig,ax=plt.subplots(figsize=(style.TEXT_WIDTH,2.25))
    ax.set_xlim(390,810); ax.set_ylim(0,1); ax.set_yticks([])
    ax.add_patch(Rectangle((400,.30),400,.32,facecolor=style.LIGHT_GRAY,edgecolor=style.PENDING,lw=.8))
    ax.add_patch(Rectangle((470,.30),138,.32,facecolor=style.LIGHT_ORANGE,edgecolor=style.MODEL,lw=1.0))
    ax.text(560,.67,r"CHIME observing band, 400--800 MHz",ha="center",fontsize=8.1)
    ax.text(539,.46,"North-American DTV\n23 allocations of 6 MHz",ha="center",va="center",fontsize=7.5,color=style.MODEL)
    ax.text(539,.245,r"channels 14--36: 138 MHz, 34.5\% of the observed-frequency span",
            ha="center",va="top",fontsize=6.6,color=style.MODEL)
    ax.annotate(r"the 21-cm line slides through this band",xy=(690,.62),xytext=(690,.86),
                fontsize=7.3,color=style.MEASURED,ha="center",va="bottom",
                arrowprops=dict(arrowstyle="->",color=style.MEASURED,lw=.75))
    ax.set_xlabel(r"Observed frequency [MHz]")
    ax2=ax.twiny(); ax2.set_xlim(ax.get_xlim())
    rest=1420.40575177
    zs=[2.5,2.0,1.5,1.0,.8]; freqs=[rest/(1+z) for z in zs]
    ax2.set_xticks(freqs); ax2.set_xticklabels([f"{z:g}" for z in zs])
    ax2.set_xlabel(r"Redshift of the 21-cm line, $z$",labelpad=4)
    for s in ("left","right","top"): ax.spines[s].set_visible(False)
    ax2.spines["bottom"].set_visible(False); ax2.spines["left"].set_visible(False); ax2.spines["right"].set_visible(False)
    ax.set_title(r"The broadcast band occupies the cosmological leverage arm",pad=4)
    return style.save(fig,OUT/"fig_intro_band.pdf",title="CHIME, DTV, and redshift bands")


def fig_intro_two_errors() -> Path:
    x=np.linspace(-3.5,3.5,800)
    fig,ax=plt.subplots(figsize=(style.TEXT_WIDTH,2.7))
    ax.plot(x,norm.pdf(x,0,1.0),color=style.INK,label=r"correct uncertainty")
    ax.plot(x,norm.pdf(x,0,.45),color=style.MEASURED,label=r"underestimated error bar")
    ax.plot(x,norm.pdf(x,.85,.48),color=style.MODEL,label=r"biased estimate")
    ax.axvline(0,color=style.PENDING,lw=.7)
    ax.annotate(r"same center, wrong width",xy=(0,.84),xytext=(-2.9,.79),fontsize=7.4,color=style.MEASURED,
                arrowprops=dict(arrowstyle="->",color=style.MEASURED,lw=.7))
    ax.annotate(r"small error bar, wrong answer",xy=(.85,.83),xytext=(1.35,.72),fontsize=7.4,color=style.MODEL,
                arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.7))
    ax.set_xlabel(r"Measured value [units of the correctly estimated error bar]")
    ax.set_ylabel(r"Probability density"); ax.set_yticks([]); ax.set_ylim(0,1.22); style.clean_axes(ax,grid=None)
    ax.legend(loc="upper left",ncol=3,fontsize=7.3)
    ax.set_title(r"Two ways to be wrong; the time-cost error is a third",pad=4)
    return style.save(fig,OUT/"fig_intro_two_errors.pdf",title="Uncertainty, bias, and misleading precision")


def fig_intro_averaging() -> Path:
    rng=np.random.default_rng(20260810)
    n=np.logspace(0,3,120)
    thermal=100/np.sqrt(n)
    measured=thermal*np.exp(rng.normal(0,.11,size=n.size))
    measured=np.maximum(measured,1.6)
    systematic=np.sqrt(thermal**2+10.0**2)
    fig,ax=plt.subplots(figsize=(style.TEXT_WIDTH,2.75))
    ax.plot(n,measured,color=style.MEASURED,lw=1.0,label=r"thermal realization")
    ax.plot(n,thermal,color=style.INK,ls=(0,(4,2)),label=r"$N^{-1/2}$ expectation")
    ax.plot(n,systematic,color=style.MODEL,label=r"thermal noise + coherent floor")
    ax.axhline(10.0,color=style.FAILURE,lw=.75,ls=(0,(2,2)))
    ax.annotate(r"a coherent residual does not average away",xy=(500,10.6),xytext=(18,45),
                fontsize=7.4,color=style.MODEL,arrowprops=dict(arrowstyle="->",lw=.7,color=style.MODEL))
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1,1e3); ax.set_ylim(1.5,400)
    ax.set_xlabel(r"Samples averaged, $N$"); ax.set_ylabel(r"Residual level [arbitrary units]")
    style.clean_axes(ax); ax.legend(loc="upper right",fontsize=7.4)
    ax.set_title(r"Noise averages down; a transmitter does not",pad=4)
    return style.save(fig,OUT/"fig_intro_averaging.pdf",title="Thermal averaging and coherent residual floor")


def _rrc_like(x):
    y=np.ones_like(x); edge=.32
    left=x<edge; right=x>5.72
    y[left]=.5*(1-np.cos(np.pi*x[left]/edge))
    y[right]=.5*(1+np.cos(np.pi*(x[right]-5.72)/(6-5.72)))
    return np.clip(y,0,1)


def fig_intro_atsc() -> Path:
    x=np.linspace(0,6,1400); shelf=_rrc_like(x)
    fig,ax=plt.subplots(figsize=(style.TEXT_WIDTH,2.75))
    # CHIME coarse bins behind the allocation.
    bw=.390625
    for left in np.arange(0,6,bw):
        ax.add_patch(Rectangle((left,-17),bw,36,facecolor="none",edgecolor=style.GRID,lw=.45,zorder=0))
    ax.plot(x,20*np.log10(np.maximum(shelf,.03)),color=style.INK,lw=1.25)
    ax.fill_between(x,-20,20*np.log10(np.maximum(shelf,.03)),color=style.LIGHT_GRAY,alpha=.8)
    pilot=177/572
    ax.vlines(pilot,-20,22,color=style.MEASURED,lw=2.2)
    ax.annotate(r"pilot: concentrated by the broadcast standard" + "\n" + r"$21.6$ dB above the shelf on the detector axis",
                xy=(pilot,20),xytext=(1.05,22),fontsize=7.4,color=style.MEASURED,
                arrowprops=dict(arrowstyle="->",color=style.MEASURED,lw=.75))
    ax.text(3.2,3,r"randomized 8-VSB payload shelf",ha="center",fontsize=8.1)
    ax.annotate("one monitored bin speaks for\nthe remaining allocation",
                xy=(2.8,-5),xytext=(2.0,-14),fontsize=7.2,color=style.MODEL,
                arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.7))
    ax.set_xlim(0,6); ax.set_ylim(-20,27)
    ax.set_xlabel(r"Frequency above the allocation's lower edge [MHz]")
    ax.set_ylabel(r"Spectral density [dB, schematic]")
    style.clean_axes(ax); ax.set_title(r"What one digital-television allocation looks like to the telescope",pad=4)
    return style.save(fig,OUT/"fig_intro_atsc.pdf",title="ATSC shelf, pilot, and CHIME raster")


def build_all():
    return [fig_claim_chain(),fig_intro_soundwave(),fig_intro_wiggle(),fig_intro_dilation(),
            fig_intro_band(),fig_intro_two_errors(),fig_intro_averaging(),fig_intro_atsc()]
