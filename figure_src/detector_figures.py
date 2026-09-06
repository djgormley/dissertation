"""Detector geometry and worked examples."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from . import style
from .io_utils import OUT


def fig_dirichlet_duality() -> Path:
    fig,axes=plt.subplots(1,2,figsize=(style.TEXT_WIDTH,2.85),constrained_layout=True)
    x=np.linspace(-4.5,4.5,2200); response=np.sinc(x-.5)**2
    ax=axes[0]; ax.plot(x,10*np.log10(np.maximum(response,1e-5)),color=style.INK,lw=1.05)
    samples=np.arange(-4,5); vals=10*np.log10(np.maximum(np.sinc(samples-.5)**2,1e-5))
    ax.plot(samples,vals,color=style.MEASURED,marker="o",lw=1.0,ms=3.7)
    for ref in (-2,2): ax.axvline(ref,color=style.MODEL,ls=(0,(3,2)),lw=.9)
    ax.annotate(r"adjacent bin:" + "\n" + r"$-3.9$ dB",xy=(1,vals[list(samples).index(1)]),xytext=(-2.3,-3.2),ha="right",va="center",
                fontsize=7.1,color=style.MUTED,arrowprops=dict(arrowstyle="->",color=style.MUTED,lw=.7))
    ax.annotate(r"reference:" + "\n" + r"$-13.5$ dB",xy=(2,vals[list(samples).index(2)]),xytext=(2.3,-3.2),ha="left",va="center",
                fontsize=7.1,color=style.MODEL,arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.7))
    ax.set_xlim(-4,4); ax.set_ylim(-42,4); ax.set_xlabel(r"Coarse-grid displacement $\Delta k$ [bins]")
    ax.set_ylabel(r"Power response [dB]"); style.clean_axes(ax); style.panel_label(ax,"a")
    ax.set_title(r"reference placement: kernel decay",pad=4)
    u=np.linspace(-6,6,1800); fine=np.sinc(u/2)**2
    ax=axes[1]; ax.axvspan(-2,2,color=style.LIGHT_BLUE); ax.plot(u,fine,color=style.MEASURED)
    for z in (-2,2): ax.axvline(z,color=style.MODEL,ls=(0,(3,2)),lw=.9)
    ax.text(0,1.07,r"designated window",ha="center",fontsize=7.4,color=style.MEASURED)
    ax.text(-2.3,.30,r"zero",ha="right",fontsize=7.0,color=style.MODEL); ax.text(2.3,.30,r"zero",ha="left",fontsize=7.0,color=style.MODEL)
    ax.set_xlim(-6,6); ax.set_ylim(-.02,1.16); ax.set_xlabel(r"Padded fine-grid offset [bins]")
    ax.set_ylabel(r"Normalized power"); style.clean_axes(ax); style.panel_label(ax,"b")
    ax.set_title(r"capture window: main-lobe extent",pad=4)
    return style.save(fig,OUT/"fig_dirichlet_duality.pdf",title="Dual uses of the Dirichlet response")


def build_all(): return [fig_dirichlet_duality()]
