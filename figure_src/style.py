"""Dissertation-wide plotting style.

The body text is Latin Modern (LaTeX ``lmodern``).  Submission figures render
all text through the same LaTeX stack, at a fixed physical size, so labels are
not silently substituted with DejaVu or shrunk differently from chapter to
chapter.  This file also fixes the semantic palette and common line/axis rules.
"""
from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Dissertation text block is 6.5 in; figures are included at 0.98 linewidth.
TEXT_WIDTH = 6.35
HALF_WIDTH = 3.05

INK = "#202225"
MUTED = "#6F747A"
GRID = "#D9DADD"
PAPER = "#FFFFFF"
PANEL = "#F7F7F5"
# Semantic palette drawn from the WVU visual-identity color system
# (scm.wvu.edu/brand/visual-identity/); role names are unchanged.
MEASURED = "#0062A3"       # archive / instrument measurement (WVU safety blue)
MODEL = "#7F6310"          # model, assumption, or transfer (WVU old gold)
CONDITIONAL = "#6A724F"    # feasible/accepted, but conditional (WVU hemlock)
FAILURE = "#8D4638"        # failure, rejection, or excision (WVU woodburn)
PENDING = "#988E8B"        # unmeasured / contextual (WVU seneca gray)
PURPLE = "#F58672"         # additional series only (WVU sunset)
GOLD = "#EEAA00"           # additional series / warning (WVU gold)
LIGHT_BLUE = "#DEEBF3"     # pale tints of the role colors for fills
LIGHT_ORANGE = "#FCF2D9"
LIGHT_GREEN = "#E1E3DC"
LIGHT_RED = "#EADDDB"
LIGHT_GRAY = "#F0EEEE"
SERIES = [MEASURED, MODEL, CONDITIONAL, PURPLE, GOLD, PENDING]

# Fixed PDF metadata makes repeated figure builds byte-for-byte reproducible.
# The date identifies the frozen dissertation-export interface revision; it is
# not intended to represent the wall-clock time of a local rebuild.
PDF_METADATA_DATE = datetime(2026, 8, 12, tzinfo=timezone.utc)


def configure(*, require_tex: bool = True) -> None:
    """Apply the dissertation figure style.

    The bundled build requires TeX and fails rather than silently substituting
    another font.  ``require_tex=False`` is only for an explicitly requested
    quick preview and is never used by the Makefile or audit.
    """
    have_tex = all(shutil.which(c) for c in ("latex", "dvipng", "kpsewhich"))
    if require_tex and not have_tex:
        raise RuntimeError(
            "Figure generation requires latex, dvipng, and kpsewhich so that "
            "figure text uses Latin Modern exactly like the dissertation."
        )
    matplotlib.rcParams.update({
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "font.family": "serif",
        "font.serif": ["Latin Modern Roman", "CMU Serif", "DejaVu Serif"],
        "font.size": 9.0,
        "axes.titlesize": 10.0,
        "axes.labelsize": 9.0,
        "axes.labelcolor": INK,
        "axes.edgecolor": MUTED,
        "axes.linewidth": 0.75,
        "xtick.labelsize": 8.2,
        "ytick.labelsize": 8.2,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.major.width": 0.65,
        "ytick.major.width": 0.65,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "lines.linewidth": 1.45,
        "lines.markersize": 4.8,
        "patch.linewidth": 0.8,
        "legend.fontsize": 8.0,
        "legend.frameon": False,
        "grid.color": GRID,
        "grid.linewidth": 0.55,
        "grid.alpha": 0.78,
        "axes.grid": False,
        "axes.axisbelow": True,
        "axes.unicode_minus": False,
        "mathtext.fontset": "cm",
        "text.usetex": bool(have_tex),
        "text.color": INK,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.035,
    })
    if have_tex:
        matplotlib.rcParams["text.latex.preamble"] = (
            r"\usepackage[T1]{fontenc}"
            r"\usepackage{lmodern}"
            r"\usepackage{amsmath,amssymb}"
        )


def clean_axes(ax, *, grid: str | None = "both"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid:
        ax.grid(True, axis=grid, which="major")
    return ax


def panel_label(ax, label: str, *, x: float = -0.08, y: float = 1.035) -> None:
    ax.text(x, y, rf"\textbf{{({label})}}", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=9.0, color=INK)


def save(fig, path: Path, *, title: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="pdf", metadata={
        "Title": title,
        "Author": "Dylan Gormley",
        "Subject": "The Pilot-Proxy Method dissertation figure",
        "Creator": "Matplotlib with Latin Modern via LaTeX",
        "CreationDate": PDF_METADATA_DATE,
        "ModDate": PDF_METADATA_DATE,
    })
    plt.close(fig)
    return path


def diagram_box(ax, xy, wh, *, title: str, body: str,
                status: str = "context", fontsize: float = 7.7,
                title_size: float = 8.1, rounding: float = 0.018):
    fills = {
        "measured": LIGHT_BLUE, "model": LIGHT_ORANGE,
        "conditional": LIGHT_GREEN, "failure": LIGHT_RED,
        "pending": LIGHT_GRAY, "context": PANEL,
    }
    edges = {
        "measured": MEASURED, "model": MODEL,
        "conditional": CONDITIONAL, "failure": FAILURE,
        "pending": PENDING, "context": MUTED,
    }
    x, y = xy; w, h = wh
    p = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0.010,rounding_size={rounding}",
        facecolor=fills[status], edgecolor=edges[status], linewidth=0.9,
        transform=ax.transAxes, clip_on=False)
    ax.add_patch(p)
    title = title.replace(r"\\", "\n")
    body = body.replace(r"\\", "\n")
    ax.text(x+w/2, y+0.68*h, title, transform=ax.transAxes,
            ha="center", va="center", fontsize=title_size,
            fontweight="bold", color=INK)
    ax.text(x+w/2, y+0.32*h, body, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize,
            color=INK, linespacing=1.13)
    return p


def diagram_arrow(ax, start, end, *, status: str = "context",
                  style: str = "-|>", connectionstyle: str = "arc3",
                  linewidth: float = 1.0):
    colors = {
        "measured": MEASURED, "model": MODEL,
        "conditional": CONDITIONAL, "failure": FAILURE,
        "pending": PENDING, "context": MUTED,
    }
    p = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=8,
                        linewidth=linewidth, color=colors[status],
                        connectionstyle=connectionstyle,
                        transform=ax.transAxes, clip_on=False)
    ax.add_patch(p)
    return p


def status_handles(statuses: Iterable[str]):
    from matplotlib.lines import Line2D
    colors = {"measured": MEASURED, "model": MODEL,
              "conditional": CONDITIONAL, "failure": FAILURE,
              "pending": PENDING}
    labels = {"measured": "measured", "model": "model / transfer",
              "conditional": "conditional / feasible",
              "failure": "failure / excision",
              "pending": "pending / unmeasured"}
    return [Line2D([0], [0], color=colors[s], lw=3, label=labels[s]) for s in statuses]
