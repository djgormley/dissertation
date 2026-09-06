"""Chapter 9 geometry, cost, and Fisher-screening figures."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from . import style
from .io_utils import OUT

REST_MHZ=1420.40575177


def fig_bao_footprint() -> Path:
    fig,axes=plt.subplots(2,1,figsize=(style.TEXT_WIDTH,4.55),constrained_layout=True)
    # One 6-MHz allocation, using the physical channel-35 interval 596-602 MHz.
    ax=axes[0]; lo,hi=596.,602.; bw=.390625
    edges=np.arange(lo,hi+bw,bw); centers=edges[:-1]+bw/2
    pilot=596+177/572; pilot_i=int(np.floor((pilot-lo)/bw))
    for i,(a,b,c) in enumerate(zip(edges[:-1],edges[1:],centers)):
        color=style.MODEL if i==pilot_i else style.MEASURED
        height=1.0 if i==pilot_i else .44
        ax.add_patch(Rectangle((a,0),b-a,height,facecolor=color,edgecolor="white",lw=.65,alpha=.9))
    ax.vlines(pilot,0,1.18,color=style.MODEL,lw=1.2)
    ax.annotate(r"ATSC pilot",xy=(pilot,1.17),xytext=(597.1,1.27),fontsize=7.4,color=style.MODEL,
                arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.7))
    ax.annotate(r"one monitored coarse bin",xy=(centers[pilot_i]+.12,.75),xytext=(598.9,1.12),fontsize=7.3,color=style.MODEL,
                arrowprops=dict(arrowstyle="->",color=style.MODEL,lw=.7))
    ax.annotate(r"remaining bins inherit the decision" + "\n" + r"only through the shelf-transfer model",xy=(599.6,.44),xytext=(601.2,.86),
                ha="center",fontsize=7.2,color=style.MEASURED,
                arrowprops=dict(arrowstyle="->",color=style.MEASURED,lw=.7))
    ax.set_xlim(lo-.15,hi+.15); ax.set_ylim(-.02,1.45); ax.set_yticks([])
    ax.set_xlabel(r"Frequency [MHz] -- one 6 MHz allocation, 15.36 CHIME coarse channels")
    style.clean_axes(ax,grid=None); style.panel_label(ax,"a"); ax.set_title(r"one allocation: what is measured and what the measurement covers",loc="left",pad=18)
    ax2=ax.twiny(); ax2.set_xlim(ax.get_xlim()); ticks=np.linspace(lo,hi,4); ax2.set_xticks(ticks); ax2.set_xticklabels([f"{REST_MHZ/t-1:.3f}" for t in ticks]); ax2.set_xlabel(r"21-cm redshift $z$",labelpad=3)
    ax2.spines["bottom"].set_visible(False); ax2.spines["left"].set_visible(False); ax2.spines["right"].set_visible(False)

    ax=axes[1]; band_lo,band_hi=470.,608.; ch_edges=np.linspace(band_lo,band_hi,24)
    coarse=np.arange(band_lo,band_hi+bw,bw)
    # Protected/background band.
    ax.add_patch(Rectangle((band_lo,0),band_hi-band_lo,.66,facecolor=style.LIGHT_BLUE,edgecolor=style.MEASURED,lw=.75))
    for chleft in ch_edges[:-1]:
        p=chleft+177/572
        ax.add_patch(Rectangle((p-bw/2,0),bw,.66,facecolor=style.MODEL,edgecolor="none"))
    for x in ch_edges: ax.axvline(x,color="white",lw=.6)
    ax.text(470,.91,r"23 monitored bins $\longrightarrow$ 354 covered (6.5\% monitored)",fontsize=8.0)
    ax.set_xlim(468,610); ax.set_ylim(-.05,1.05); ax.set_yticks([]); ax.set_xlabel(r"Frequency [MHz]")
    style.clean_axes(ax,grid=None); style.panel_label(ax,"b"); ax.set_title(r"the same geometry across the DTV band",loc="left",pad=4)
    handles=[Rectangle((0,0),1,1,facecolor=style.MODEL,label=r"monitored pilot-containing bin"),
             Rectangle((0,0),1,1,facecolor=style.MEASURED,label=r"other allocation bins covered by the decision")]
    ax.legend(handles=handles,loc="lower center",bbox_to_anchor=(.5,-.42),ncol=2,fontsize=7.2)
    return style.save(fig,OUT/"fig_bao_footprint.pdf",title="Pilot-proxy frequency footprint")


def build_all():
    return [fig_bao_footprint()]
