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
    # Left-aligned: the boundary-crossing arrow runs down the middle at x=.50,
    # and a centred label would be struck through by it.
    # One short line, right-aligned: the band between the box row and the rule
    # is only .08 tall, so two lines collide with both; and the crossing arrow
    # occupies the middle at x=.50, so the line has to live to the right of it.
    ax.text(.975,.515,r"thresholds cross only through measured nulls",
            transform=ax.transAxes,ha="right",va="bottom",fontsize=7.2,color=style.MODEL)
    # Same columns as the top row, so the two layers read as a grid.
    bottom=[(.03,"Measured departures",r"null core and tail\\feed covariance\\gain and leakage","measured"),
            (.37,"Calibration products",r"rank baseline\\anchor and bulk mask\\per-epoch multiplier","model"),
            (.71,"Required validation",r"false-alarm and detection\\performance on blocked\\holdout data","conditional")]
    for x,t,b,s in bottom: style.diagram_box(ax,(x,.17),(.26,.21),title=t,body=b,status=s,fontsize=6.8,title_size=7.4)
    style.diagram_arrow(ax,(.29,.275),(.365,.275),status="model"); style.diagram_arrow(ax,(.63,.275),(.705,.275),status="conditional")
    style.diagram_arrow(ax,(.50,.58),(.50,.39),status="model")
    return style.save(fig,OUT/"fig_model_calibration_layers.pdf",title="Analytic model and calibration boundary")


def fig_survey_evidence_flow() -> Path:
    fig,ax=canvas(3.72,"Survey evidence flow: measured products, selection, and holdout")
    boxes=[(.015,.162,"Archive",r"trigger-selected\\captures\\not uniform","model"),
           (.213,.162,"PilotProxy",r"archive scan\\checkpoint / retry\\restart safely","measured"),
           (.411,.162,"Per-frame",r"exact terms\\fine spectra\\mask + provenance","measured"),
           (.609,.162,"Calibration",r"anchors / floors\\nulls / epochs","model"),
           (.807,.162,"Forecast",r"masking cost\\conditional verdict","conditional")]
    for x,w,t,b,s in boxes:
        style.diagram_box(ax,(x,.58),(w,.22),title=t,body=b,status=s,fontsize=5.95,title_size=6.9)
    for a,b,s in [((.179,.69),(.209,.69),"measured"),((.377,.69),(.407,.69),"measured"),((.575,.69),(.605,.69),"model"),((.773,.69),(.803,.69),"conditional")]:
        style.diagram_arrow(ax,a,b,status=s)
    # The caption calls this boundary load-bearing, so it has to be drawn.
    ax.plot([.02,.98],[.475,.475],transform=ax.transAxes,color=style.MODEL,lw=1.05,ls=(0,(3,2)))
    # Two lines in the corridor between the descending connectors at x=.19,
    # .50 and .81. A masking bbox is not an option here: it cuts the very
    # arrows whose crossing of this boundary is the figure's point.
    ax.text(.215,.555,"a triggered archive is not a\nrandom sample of occupancy",
            transform=ax.transAxes,ha="left",va="top",fontsize=6.6,color=style.MODEL,linespacing=1.25)
    style.diagram_box(ax,(.07,.16),(.25,.21),title="Selection function",body=r"time, season, sky, trigger,\\and operations state",status="model",fontsize=6.45,title_size=7.1)
    style.diagram_box(ax,(.375,.16),(.25,.21),title="Blocked holdout",body=r"fit on training blocks;\\evaluate untouched blocks",status="conditional",fontsize=6.45,title_size=7.1)
    style.diagram_box(ax,(.68,.16),(.25,.21),title="Closing ledger",body=r"frames, coverage, failures,\\bytes + join completeness",status="pending",fontsize=6.45,title_size=7.1)
    style.diagram_arrow(ax,(.10,.58),(.19,.38),status="model",connectionstyle="arc3,rad=.1")
    style.diagram_arrow(ax,(.50,.58),(.50,.38),status="conditional")
    style.diagram_arrow(ax,(.805,.38),(.83,.58),status="conditional",connectionstyle="arc3,rad=-.08")
    return style.save(fig,OUT/"fig_survey_evidence_flow.pdf",title="Survey evidence flow")


def fig_residual_chain_audit() -> Path:
    fig,ax=canvas(3.85,"From pilot statistic to cosmological residual: measured terms and model gates")
    # .045 gaps: at the previous .03 the arrowheads filled the whole gap and
    # the chain read as six abutted boxes with triangles wedged between them.
    steps=[(.020,.127,"Pilot statistic",r"measured\\per frame","measured"),(.192,.136,"Pilot-to-shelf",r"standard +\\propagation model","model"),(.373,.127,"Kept-frame floor",r"measured\\or refused","measured"),(.545,.127,"Day variation",r"proxy\\decomposition","model"),(.717,.136,"Visibility residual",r"transfer\\calibration","model"),(.898,.082,"$P(k)$ bias",r"forecast","conditional")]
    for i,(x,w,t,b,s) in enumerate(steps):
        style.diagram_box(ax,(x,.61),(w,.21),title=t,body=b,status=s,fontsize=6.5,title_size=7.1)
        if i<len(steps)-1: style.diagram_arrow(ax,(x+w+.006,.715),(steps[i+1][0]-.006,.715),status="model" if i in (0,2,3) else "context")
    # Two lines on the left: the branch arrows sweep down the right-hand side
    # and a full-width single line is crossed by both of them.
    ax.text(.02,.565,"The current scalar-proxy calculation\n"
                     "is a conservative screening result,\n"
                     "not a visibility-domain proof.",
            transform=ax.transAxes,va="top",fontsize=7.0,color=style.MODEL,linespacing=1.25)
    style.diagram_box(ax,(.28,.22),(.26,.20),title=r"$r_{\rm stochastic}$",body=r"adds to covariance; averages\\with the declared coherence model",status="pending",fontsize=6.7,title_size=7.3)
    style.diagram_box(ax,(.63,.22),(.26,.20),title=r"$r_{\rm coherent}$",body=r"enters a signed residual template\\and parameter-bias calculation",status="pending",fontsize=6.7,title_size=7.3)
    style.diagram_arrow(ax,(.785,.61),(.43,.43),status="measured",connectionstyle="arc3,rad=.10")
    style.diagram_arrow(ax,(.785,.61),(.69,.43),status="measured",connectionstyle="arc3,rad=-.08")
    ax.add_patch(Rectangle((.02,.04),.96,.14,transform=ax.transAxes,facecolor=style.LIGHT_ORANGE,edgecolor=style.MODEL,lw=.8))
    ax.text(.50,.11,"Closing tests: full-allocation spectra; contaminated visibilities\n"
                    r"before/after $m=0$ subtraction; alternative residual shapes; combined-bin Fisher estimator.",
            transform=ax.transAxes,ha="center",va="center",fontsize=6.0,linespacing=1.2)
    return style.save(fig,OUT/"fig_residual_chain_audit.pdf",title="Residual-chain evidence audit")


def diamond(ax,center,wh,text,status="model",fontsize=6.8):
    x,y=center; w,h=wh; fill,edge={"model":(style.LIGHT_ORANGE,style.MODEL),"conditional":(style.LIGHT_GREEN,style.CONDITIONAL),"failure":(style.LIGHT_RED,style.FAILURE)}[status]
    p=Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],closed=True,transform=ax.transAxes,facecolor=fill,edgecolor=edge,lw=.9)
    text = text.replace(r"\\", "\n")
    # A diamond tapers away from its centre line, so the text has well under
    # the full width to work with; fit it rather than let it poke out the sides.
    text, fontsize = style._fit_fontsize(ax, text, fontsize, w*0.62, 0.50)
    ax.add_patch(p); ax.text(x,y,text,transform=ax.transAxes,ha="center",va="center",fontsize=fontsize,linespacing=1.05); return p


def fig_deployment_lifecycle() -> Path:
    fig,ax=canvas(3.55,"Real-time stage lifecycle: initialization is part of correctness")
    # .038 gaps across the top row so every connector has a visible shaft.
    # Boxes are tall enough for their wrapped bodies at the 5.6pt legibility
    # floor; at .19 the last line was pushed through the bottom border.
    style.diagram_box(ax,(.015,.60),(.135,.23),title="Input buffer",body=r"frame identity\\geometry + epoch\\receiver contract",status="measured",fontsize=6.4,title_size=7.0)
    diamond(ax,(.253,.715),(.13,.23),r"contracts\\valid?")
    style.diagram_box(ax,(.356,.60),(.16,.23),title="Initialize",body=r"bind weights\\zero outputs in stream\\reset completion state",status="measured",fontsize=6.3,title_size=7.0)
    style.diagram_box(ax,(.554,.60),(.15,.23),title="Frame launch",body=r"one block per stream\\exact row sums\\atomic global sums",status="measured",fontsize=6.3,title_size=7.0)
    diamond(ax,(.807,.715),(.13,.23),r"CUDA +\\tripwire OK?")
    style.diagram_box(ax,(.88,.30),(.10,.20),title="Publish",body=r"mask bit\\diagnostics",status="conditional",fontsize=6.1,title_size=6.8)
    style.diagram_box(ax,(.57,.26),(.20,.24),title="Last-block finalizer",body=r"re-read finalized sums\\exact threshold decision\\overwrite counter with mask",status="measured",fontsize=6.2,title_size=6.9)
    style.diagram_box(ax,(.22,.22),(.20,.25),title="Fail closed",body=r"mark frame invalid\\emit operations event\\never silently keep or mask",status="failure",fontsize=6.3,title_size=7.0)
    def edge_label(x,y,text,color,mask=True,size=6.2,ha="center"):
        # A masking box is safe only in open space; over a node border it eats
        # the outline and reads as a notch chewed out of the box.
        kw=dict(bbox=dict(facecolor="white",edgecolor="none",pad=0.8)) if mask else {}
        ax.text(x,y,text,transform=ax.transAxes,ha=ha,va="center",fontsize=size,color=color,**kw)
    style.diagram_arrow(ax,(.153,.715),(.185,.715),status="measured")
    style.diagram_arrow(ax,(.321,.715),(.353,.715),status="conditional"); edge_label(.348,.757,r"yes",style.CONDITIONAL,mask=False,size=5.9,ha="right")
    style.diagram_arrow(ax,(.519,.715),(.551,.715),status="measured")
    style.diagram_arrow(ax,(.707,.715),(.739,.715),status="measured")
    # Branches leave the diamonds' bottom vertices exactly, not near them.
    style.diagram_arrow(ax,(.807,.600),(.700,.500),status="conditional",connectionstyle="arc3,rad=.05"); edge_label(.780,.550,r"yes",style.CONDITIONAL)
    style.diagram_arrow(ax,(.770,.380),(.875,.380),status="conditional")
    style.diagram_arrow(ax,(.253,.600),(.320,.470),status="failure",connectionstyle="arc3,rad=-.15"); edge_label(.262,.535,r"no",style.FAILURE)
    style.diagram_arrow(ax,(.807,.600),(.420,.360),status="failure",connectionstyle="arc3,rad=.16"); edge_label(.490,.500,r"no",style.FAILURE)
    ax.text(.02,.08,r"A failure has an explicit scientific meaning: this frame has no valid decision and cannot enter retained/excised accounting.",transform=ax.transAxes,ha="left",fontsize=7.0,color=style.FAILURE)
    return style.save(fig,OUT/"fig_deployment_lifecycle.pdf",title="Real-time detector-stage lifecycle")


def build_all():
    return [fig_model_calibration_layers(),fig_survey_evidence_flow(),fig_residual_chain_audit(),fig_deployment_lifecycle()]
