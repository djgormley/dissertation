"""Evidence, calibration, deployment, and status diagrams."""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from . import style
from .io_utils import OUT


def canvas(height,title):
    fig,ax=plt.subplots(figsize=(style.TEXT_WIDTH,height)); ax.set_axis_off()
    ax.text(.02,.96,rf"\textbf{{{title}}}",transform=ax.transAxes,ha="left",va="top",fontsize=10.0)
    return fig,ax


def fig_model_calibration_layers() -> Path:
    fig,ax=canvas(3.45,"Analytic detector model and empirical calibration boundary")
    top=[(.03,"Idealized hypotheses",r"$H_0$: noise only\\$H_1$: known tone + noise","measured"),
         (.37,"Assumptions",r"circular complex Gaussian\\locally smooth background\\effective feed independence","model"),
         (.71,"Analytic consequences",r"central/noncentral laws\\coherent-gain identity\\scale cancellation","measured")]
    for x,t,b,s in top: style.diagram_box(ax,(x,.58),(.26,.23),title=t,body=b,status=s,fontsize=6.8,title_size=7.4)
    style.diagram_arrow(ax,(.29,.695),(.365,.695),status="model"); style.diagram_arrow(ax,(.63,.695),(.705,.695),status="model")
    ax.plot([.025,.975],[.50,.50],transform=ax.transAxes,color=style.MODEL,lw=1.05,ls=(0,(3,2)))
    ax.text(.50,.515,r"thresholds cross this boundary only through measured nulls",transform=ax.transAxes,ha="center",va="bottom",fontsize=7.2,color=style.MODEL)
    bottom=[(.07,"Measured departures",r"null core and tail\\feed covariance\\gain and leakage","measured"),
            (.38,"Calibration products",r"rank baseline\\anchor and bulk mask\\per-epoch multiplier","model"),
            (.69,"Required validation",r"false-alarm and detection\\performance on blocked\\holdout data","conditional")]
    for x,t,b,s in bottom: style.diagram_box(ax,(x,.17),(.24,.21),title=t,body=b,status=s,fontsize=6.8,title_size=7.4)
    style.diagram_arrow(ax,(.31,.275),(.375,.275),status="model"); style.diagram_arrow(ax,(.62,.275),(.685,.275),status="conditional")
    style.diagram_arrow(ax,(.50,.58),(.50,.39),status="model")
    return style.save(fig,OUT/"fig_model_calibration_layers.pdf",title="Analytic model and calibration boundary")


def fig_survey_evidence_flow() -> Path:
    fig,ax=canvas(3.72,"Survey evidence flow: measured products, selection, and holdout")
    boxes=[(.015,.18,"Archive",r"trigger-selected\\captures\\not uniform","model"),
           (.212,.18,"Datatrawl",r"inventory\\stream / delete\\restart safely","measured"),
           (.409,.18,"Per-frame",r"exact terms\\fine spectra\\mask + provenance","measured"),
           (.606,.18,"Calibration",r"anchors / floors\\nulls / epochs","model"),
           (.803,.18,"Forecast",r"mask cost\\conditional verdict","conditional")]
    for x,w,t,b,s in boxes:
        style.diagram_box(ax,(x,.58),(w,.22),title=t,body=b,status=s,fontsize=5.95,title_size=6.9)
    for a,b,s in [((.195,.69),(.207,.69),"measured"),((.392,.69),(.404,.69),"measured"),((.589,.69),(.601,.69),"model"),((.786,.69),(.798,.69),"conditional")]:
        style.diagram_arrow(ax,a,b,status=s)
    style.diagram_box(ax,(.07,.16),(.25,.21),title="Selection function",body=r"time, season, sky, trigger,\\and operations state",status="model",fontsize=6.45,title_size=7.1)
    style.diagram_box(ax,(.375,.16),(.25,.21),title="Blocked holdout",body=r"fit on training blocks;\\evaluate untouched blocks",status="conditional",fontsize=6.45,title_size=7.1)
    style.diagram_box(ax,(.68,.16),(.25,.21),title="Closing ledger",body=r"frames, coverage, failures,\\bytes + join completeness",status="pending",fontsize=6.45,title_size=7.1)
    style.diagram_arrow(ax,(.10,.58),(.19,.38),status="model",connectionstyle="arc3,rad=.1")
    style.diagram_arrow(ax,(.50,.58),(.50,.38),status="conditional")
    style.diagram_arrow(ax,(.805,.38),(.83,.58),status="conditional",connectionstyle="arc3,rad=-.08")
    return style.save(fig,OUT/"fig_survey_evidence_flow.pdf",title="Survey evidence flow")


def fig_residual_chain_audit() -> Path:
    fig,ax=canvas(3.85,"From pilot statistic to cosmological residual: measured terms and model gates")
    steps=[(.02,.14,"Pilot statistic",r"measured\\per frame","measured"),(.19,.15,"Pilot-to-shelf",r"standard +\\propagation model","model"),(.37,.14,"Kept-frame floor",r"measured\\or refused","measured"),(.54,.14,"Day variation",r"proxy\\decomposition","model"),(.71,.15,"Visibility residual",r"transfer\\calibration","model"),(.89,.09,"$P(k)$ bias",r"forecast","conditional")]
    for i,(x,w,t,b,s) in enumerate(steps):
        style.diagram_box(ax,(x,.61),(w,.21),title=t,body=b,status=s,fontsize=6.5,title_size=7.1)
        if i<len(steps)-1: style.diagram_arrow(ax,(x+w,.715),(steps[i+1][0]-.005,.715),status="model" if i in (0,2,3) else "context")
    ax.text(.02,.51,r"The current scalar-proxy calculation is a conservative screening result, not a visibility-domain proof.",transform=ax.transAxes,fontsize=7.3,color=style.MODEL)
    style.diagram_box(ax,(.28,.22),(.26,.20),title=r"$r_{\rm stochastic}$",body=r"adds to covariance; averages\\with the declared coherence model",status="pending",fontsize=6.7,title_size=7.3)
    style.diagram_box(ax,(.63,.22),(.26,.20),title=r"$r_{\rm coherent}$",body=r"enters a signed residual template\\and parameter-bias calculation",status="pending",fontsize=6.7,title_size=7.3)
    style.diagram_arrow(ax,(.785,.61),(.43,.43),status="measured",connectionstyle="arc3,rad=.10")
    style.diagram_arrow(ax,(.785,.61),(.69,.43),status="measured",connectionstyle="arc3,rad=-.08")
    ax.add_patch(Rectangle((.02,.07),.96,.09,transform=ax.transAxes,facecolor=style.LIGHT_ORANGE,edgecolor=style.MODEL,lw=.8))
    ax.text(.50,.115,r"Closing tests: full-allocation spectra; contaminated visibilities before/after $m=0$ subtraction; alternative residual shapes; combined-bin Fisher estimator.",transform=ax.transAxes,ha="center",va="center",fontsize=6.5)
    return style.save(fig,OUT/"fig_residual_chain_audit.pdf",title="Residual-chain evidence audit")


def diamond(ax,center,wh,text,status="model",fontsize=6.8):
    x,y=center; w,h=wh; fill,edge={"model":(style.LIGHT_ORANGE,style.MODEL),"conditional":(style.LIGHT_GREEN,style.CONDITIONAL),"failure":(style.LIGHT_RED,style.FAILURE)}[status]
    p=Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],closed=True,transform=ax.transAxes,facecolor=fill,edgecolor=edge,lw=.9)
    text = text.replace(r"\\", "\n")
    ax.add_patch(p); ax.text(x,y,text,transform=ax.transAxes,ha="center",va="center",fontsize=fontsize,linespacing=1.05); return p


def fig_deployment_lifecycle() -> Path:
    fig,ax=canvas(3.55,"Real-time stage lifecycle: initialization is part of correctness")
    style.diagram_box(ax,(.02,.62),(.14,.19),title="Input buffer",body=r"frame identity\\geometry + epoch\\receiver contract",status="measured",fontsize=6.4,title_size=7.0)
    diamond(ax,(.25,.715),(.14,.19),r"contracts\\valid?")
    style.diagram_box(ax,(.34,.62),(.17,.19),title="Initialize",body=r"bind weights\\zero outputs in stream\\reset completion state",status="measured",fontsize=6.3,title_size=7.0)
    style.diagram_box(ax,(.58,.62),(.16,.19),title="Frame launch",body=r"one block per stream\\exact row sums\\atomic global sums",status="measured",fontsize=6.3,title_size=7.0)
    diamond(ax,(.83,.715),(.14,.19),r"CUDA +\\tripwire OK?")
    style.diagram_box(ax,(.88,.31),(.10,.18),title="Publish",body=r"mask bit\\diagnostics",status="conditional",fontsize=6.1,title_size=6.8)
    style.diagram_box(ax,(.57,.28),(.20,.21),title="Last-block finalizer",body=r"re-read finalized sums\\exact threshold decision\\overwrite counter with mask",status="measured",fontsize=6.2,title_size=6.9)
    style.diagram_box(ax,(.22,.24),(.20,.22),title="Fail closed",body=r"mark frame invalid\\emit operations event\\never silently keep or mask",status="failure",fontsize=6.3,title_size=7.0)
    style.diagram_arrow(ax,(.16,.715),(.18,.715),status="measured"); style.diagram_arrow(ax,(.32,.715),(.335,.715),status="conditional"); ax.text(.322,.75,r"yes",transform=ax.transAxes,fontsize=6.2,color=style.CONDITIONAL)
    style.diagram_arrow(ax,(.51,.715),(.575,.715),status="measured"); style.diagram_arrow(ax,(.74,.715),(.76,.715),status="measured")
    style.diagram_arrow(ax,(.83,.62),(.70,.49),status="conditional",connectionstyle="arc3,rad=.05"); ax.text(.76,.55,r"yes",transform=ax.transAxes,fontsize=6.2,color=style.CONDITIONAL)
    style.diagram_arrow(ax,(.77,.385),(.875,.385),status="conditional")
    style.diagram_arrow(ax,(.25,.62),(.32,.46),status="failure",connectionstyle="arc3,rad=-.15"); ax.text(.245,.54,r"no",transform=ax.transAxes,fontsize=6.2,color=style.FAILURE)
    style.diagram_arrow(ax,(.83,.62),(.42,.35),status="failure",connectionstyle="arc3,rad=.16"); ax.text(.64,.47,r"no",transform=ax.transAxes,fontsize=6.2,color=style.FAILURE)
    ax.text(.02,.08,r"A failure has an explicit scientific meaning: this frame has no valid decision and cannot enter retained/excised accounting.",transform=ax.transAxes,ha="left",fontsize=7.0,color=style.FAILURE)
    return style.save(fig,OUT/"fig_deployment_lifecycle.pdf",title="Real-time detector-stage lifecycle")


def build_all():
    return [fig_model_calibration_layers(),fig_survey_evidence_flow(),fig_residual_chain_audit(),fig_deployment_lifecycle()]
