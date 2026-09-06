"""Dissertation-wide plotting style.

The body text is Latin Modern (LaTeX ``lmodern``).  Submission figures render
all text through the same LaTeX stack, at a fixed physical size, so labels are
not silently substituted with DejaVu or shrunk differently from chapter to
chapter.  This file also fixes the semantic palette and common line/axis rules.
"""
from __future__ import annotations

import shutil
import textwrap
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


def _fit_fontsize(ax, text: str, size: float, box_w: float,
                  ratio: float, floor: float = 5.6) -> float:
    """Shrink size until the widest line fits box_w (axes fraction).

    Never grows the size, so a box whose text already fits is untouched. The
    width estimate is char-count times ratio ems, which is accurate enough for
    the Latin Modern text used in these diagrams; floor stops a very long line
    from being reduced to something unreadable.
    """
    lines = [ln for ln in text.replace(r"\\", "\n").split("\n") if ln]
    if not lines:
        return size
    avail = box_w * ax.get_window_extent().width * 0.86
    probe = ax.text(0, 0, text, transform=ax.transAxes, fontsize=size,
                    linespacing=1.13, alpha=0)
    try:
        got = probe.get_window_extent(
            renderer=ax.figure.canvas.get_renderer()).width
    except Exception:
        # No renderer available: fall back to a char-count estimate.
        bbox = ax.get_position()
        box_w_in = box_w * bbox.width * ax.figure.get_size_inches()[0]
        widest = max(len(ln) for ln in lines)
        probe.remove()
        est = (box_w_in * 72.0 * 0.90) / (widest * ratio)
        return text, max(floor, min(size, est))
    probe.remove()
    if got <= avail or got <= 0:
        return text, size
    # Re-wrap to the box before shrinking: a wide box with long lines should
    # gain rows, not illegible type. Only shrink for what wrapping cannot fix
    # (a single word, or math that must stay on one line).
    per_char = got / max(len(ln) for ln in lines)
    if per_char > 0 and not any("$" in ln for ln in lines):
        cols = max(6, int(avail / per_char))
        wrapped = "\n".join(
            "\n".join(textwrap.wrap(ln, cols, break_long_words=False,
                                    break_on_hyphens=False)) or ln
            for ln in lines)
        wlines = [ln for ln in wrapped.split("\n") if ln]
        widest = max(len(ln) for ln in wlines) * per_char
        if widest <= avail:
            return wrapped, size
        return wrapped, max(floor, size * avail / widest)
    return text, max(floor, size * avail / got)


def _text_height(ax, text: str, size: float) -> float:
    probe = ax.text(0, 0, text, transform=ax.transAxes, fontsize=size,
                    linespacing=1.13, alpha=0)
    try:
        h = probe.get_window_extent(
            renderer=ax.figure.canvas.get_renderer()).height
    except Exception:
        h = 0.0
    probe.remove()
    return h


def _fit_stack(ax, title: str, title_pt: float, body: str, body_pt: float,
               box_h: float, floor: float = 5.6):
    """Shrink both blocks together until they fit the box height."""
    avail = box_h * ax.get_window_extent().height * 0.88
    total = _text_height(ax, title, title_pt) + _text_height(ax, body, body_pt)
    if total <= 0 or total <= avail:
        return title_pt, body_pt
    k = avail / total
    return max(floor, title_pt * k), max(floor, body_pt * k)


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
    # Anchored to opposite edges rather than centred on fixed fractions: at the
    # box heights used here the two blocks' half-heights meet in the middle and
    # the descenders of the title collide with the first body line.
    title_text, title_pt = _fit_fontsize(ax, title, title_size, w, 0.55)
    body_text, body_pt = _fit_fontsize(ax, body, fontsize, w, 0.50)
    # Wrapping buys width by spending height, so the two blocks together can
    # now outgrow a short box. Scale both down until they fit.
    title_pt, body_pt = _fit_stack(ax, title_text, title_pt,
                                   body_text, body_pt, h)
    # Title and body are one stack, top-aligned with a fixed pad. Centring the
    # stack instead floats the title by however many body lines a box happens
    # to have, so titles across a row of boxes never share a baseline.
    H = ax.get_window_extent().height
    t_h = _text_height(ax, title_text, title_pt) / H
    b_h = _text_height(ax, body_text, body_pt) / H
    gap = (0.40 * title_pt * ax.figure.dpi / 72.0) / H
    pad = (0.55 * title_pt * ax.figure.dpi / 72.0) / H
    slack = max(0.0, h - t_h - b_h)
    gap = min(gap, slack * 0.5)
    pad = min(pad, max(0.0, slack - gap) * 0.5)
    top = y + h - pad
    ax.text(x+w/2, top, title_text, transform=ax.transAxes,
            ha="center", va="top", fontsize=title_pt,
            fontweight="bold", color=INK)
    ax.text(x+w/2, top-t_h-gap, body_text, transform=ax.transAxes,
            ha="center", va="top", fontsize=body_pt,
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
