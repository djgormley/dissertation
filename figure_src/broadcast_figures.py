"""Broadcast-standard and transmitter-context figures."""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from mpl_toolkits.basemap import Basemap

from . import style
from .io_utils import OUT, read_csv


def _rrc_like(x: np.ndarray) -> np.ndarray:
    y=np.ones_like(x); rise=.310; fall0=5.69
    lo=x<rise; hi=x>fall0
    y[lo]=.5*(1-np.cos(np.pi*x[lo]/rise))
    y[hi]=.5*(1+np.cos(np.pi*(x[hi]-fall0)/(6-fall0)))
    return np.clip(y,0,1)


def fig_vsb_standard_model() -> Path:
    x=np.linspace(-.08,6.08,1800); env=_rrc_like(np.clip(x,0,6))
    env[(x<0)|(x>6)]=0
    pilot_exact=177/572
    pilot_nom=.309
    alpha_std=.1152
    bn=684/286*4.5  # MHz
    half_transition=alpha_std*bn/2
    fig,ax=plt.subplots(figsize=(style.TEXT_WIDTH,2.8))
    ax.fill_between(x,0,env,facecolor=style.LIGHT_BLUE,edgecolor=style.MEASURED,lw=1.05)
    ax.vlines(pilot_exact,0,1.14,color=style.MEASURED,lw=1.8)
    ax.scatter([pilot_exact],[1.14],s=18,color=style.MEASURED,zorder=4)
    ax.axvline(pilot_nom,color=style.MODEL,lw=.8,ls=(0,(3,2)))
    ax.axvline(half_transition,color=style.CONDITIONAL,lw=.8,ls=(0,(3,2)))
    ax.text(3.0,.60,r"8-VSB payload shelf",ha="center",fontsize=8.2)
    ax.annotate(r"exact frequency model used here" + "\n" + r"$177/572\,\mathrm{MHz}=309.441$ kHz",
                xy=(pilot_exact,1.1),xytext=(1.15,1.00),fontsize=7.2,color=style.MEASURED,
                arrowprops=dict(arrowstyle="->",color=style.MEASURED,lw=.7))
    ax.text(pilot_nom,-.04,"A/53 nominal\n309 kHz",ha="right",va="top",fontsize=6.8,color=style.MODEL)
    ax.text(half_transition,.20,r"$\alpha B_N/2$" + "\n309.95 kHz",ha="left",fontsize=6.8,color=style.CONDITIONAL)
    ax.text(3.0,.13,r"$B_N=5.381\,\mathrm{MHz}$; $\alpha=0.1152$ are normative values",
            ha="center",fontsize=7.1,color=style.MUTED)
    ax.set_xlim(-.05,6.05); ax.set_ylim(-.02,1.20)
    ax.set_xlabel(r"Offset from the lower edge of the 6 MHz allocation [MHz]")
    ax.set_ylabel(r"Normalized amplitude"); ax.set_yticks([0,.5,1])
    style.clean_axes(ax); ax.set_title(r"ATSC normative values are close to, but not, one exact geometric identity",pad=5)
    return style.save(fig,OUT/"fig_vsb_standard_model.pdf",title="ATSC normative values and pilot geometry")


def fig_vsb_layout() -> Path:
    pilot=177/572; x=np.linspace(0,6,1500); env=_rrc_like(x)
    fig,axes=plt.subplots(1,2,figsize=(style.TEXT_WIDTH,2.8),gridspec_kw={"width_ratios":[1.55,1]},constrained_layout=True)
    ax=axes[0]
    ax.fill_between(x,0,env,color=style.LIGHT_BLUE,edgecolor=style.MEASURED,lw=1.0)
    ax.vlines(pilot,0,1.17,color=style.MEASURED,lw=1.7); ax.scatter([pilot],[1.17],color=style.MEASURED,s=18)
    for edge in np.arange(0,6.01,.390625): ax.axvline(edge,color=style.GRID,lw=.35,zorder=0)
    ax.annotate(r"pilot",xy=(pilot,1.14),xytext=(1.05,1.05),fontsize=7.4,color=style.MEASURED,
                arrowprops=dict(arrowstyle="->",color=style.MEASURED,lw=.7))
    ax.text(3,.68,r"8-VSB payload shelf",ha="center",fontsize=8.0)
    ax.set_xlim(0,6); ax.set_ylim(0,1.28); ax.set_yticks([])
    ax.set_xlabel(r"Frequency above lower edge [MHz]"); style.clean_axes(ax,grid=None); style.panel_label(ax,"a")
    ax.set_title(r"allocation geometry",pad=4)
    ax=axes[1]; u=np.linspace(-8,8,1400); response=np.sinc(u/2)**2
    ax.axvspan(-2,2,color=style.LIGHT_BLUE); ax.plot(u,response,color=style.MEASURED)
    for ref in (-6.1036,6.1036): ax.axvline(ref,color=style.MODEL,lw=.9,ls=(0,(3,2)))
    ax.axvline(0,color=style.INK,lw=.7)
    ax.text(0,.84,r"target",ha="center",fontsize=7.4)
    ax.text(-6.1,.45,r"ref",ha="center",fontsize=7.2,color=style.MODEL)
    ax.text(6.1,.45,r"ref",ha="center",fontsize=7.2,color=style.MODEL)
    ax.set_xlim(-8,8); ax.set_ylim(-.02,1.03)
    ax.set_xlabel(r"Offset about the pilot [kHz]"); ax.set_ylabel(r"Normalized response")
    style.clean_axes(ax); style.panel_label(ax,"b"); ax.set_title(r"detector geometry",pad=4)
    return style.save(fig,OUT/"fig_vsb_layout.pdf",title="ATSC allocation and detector geometry")



_CENSUS_SITE_MARKERS = {
    "primary": "s",
    "relay": "o",
    "secondary": "^",
    "mixed": "D",
}
_CENSUS_SITE_LABELS = {
    "primary": r"full-power / Class A only",
    "relay": r"relay only",
    "secondary": r"translator / LPTV only",
    "mixed": r"mixed service classes",
}
_CENSUS_TOL_COLORS = {
    "disciplined": style.MEASURED,
    "unspecified": style.MODEL,
    "mixed": style.CONDITIONAL,
}
_CENSUS_TOL_LABELS = {
    "disciplined": r"all records list $\pm1$ kHz",
    "unspecified": r"no record lists a tolerance",
    "mixed": r"mixed tolerance records",
}
_KM_PER_MILE = 1.609344
_DRAO_LAT = 49.3208
_DRAO_LON = -119.6239


def _census_site_class(records):
    groups = set()
    for record in records:
        service = record["service_class"]
        if service in ("Full-power", "Class A"):
            groups.add("primary")
        elif service == "Relay":
            groups.add("relay")
        else:
            groups.add("secondary")
    return next(iter(groups)) if len(groups) == 1 else "mixed"


def _census_tolerance_class(records):
    values = {record["frequency_tolerance"] for record in records}
    if values == {"±1 kHz"}:
        return "disciplined"
    if values == {"None specified"}:
        return "unspecified"
    return "mixed"


def _aggregate_census_sites(rows):
    """Aggregate co-located emitter-channel records without inventing coordinates.

    The authoritative census carries range and bearing but not transmitter
    latitude/longitude.  Records with the same rounded source range/bearing are
    therefore shown as one site; marker area records multiplicity.  This keeps
    the map faithful to the source geometry while avoiding a misleading cloud
    of exactly coincident symbols.
    """
    grouped = defaultdict(list)
    for row in rows:
        key = (
            round(float(row["distance_km"]), 1),
            round(float(row["bearing_deg"]), 1),
        )
        grouped[key].append(row)

    sites = []
    for (distance_km, bearing_deg), records in grouped.items():
        city, state = Counter(
            (record["city"].strip(), record["state_prov"].strip())
            for record in records
        ).most_common(1)[0][0]
        sites.append({
            "distance_km": distance_km,
            "distance_mi": distance_km / _KM_PER_MILE,
            "bearing_deg": bearing_deg,
            "n": len(records),
            "city": city,
            "state": state,
            "service": _census_site_class(records),
            "tolerance": _census_tolerance_class(records),
        })
    return sites


def _census_marker_area(n_records):
    return 17.0 + 8.0 * math.sqrt(n_records)


def _census_xy(center_x, center_y, distance_mi, bearing_deg):
    theta = math.radians(bearing_deg)
    radius_m = distance_mi * 1609.344
    return (
        center_x + radius_m * math.sin(theta),
        center_y + radius_m * math.cos(theta),
    )


def _census_background(ax, radius_miles):
    """Draw vector geographic context in a DRAO-centred equidistant map."""
    margin = 1.055
    span = 2.0 * radius_miles * 1609.344 * margin
    map_ = Basemap(
        projection="aeqd",
        lat_0=_DRAO_LAT,
        lon_0=_DRAO_LON,
        width=span,
        height=span,
        resolution="i",
        ax=ax,
    )
    map_.drawmapboundary(fill_color=style.PAPER, color=style.MUTED, linewidth=0.65)
    map_.fillcontinents(color=style.PANEL, lake_color=style.PAPER, zorder=0)
    map_.drawcoastlines(color=style.MUTED, linewidth=0.48, zorder=1)
    map_.drawcountries(color=style.INK, linewidth=0.65, zorder=2)
    map_.drawstates(color=style.GRID, linewidth=0.38, zorder=1.5)
    return map_


def _draw_census_range_grid(
    ax,
    center_x,
    center_y,
    radius_miles,
    *,
    ring_step=100,
    labels=True,
):
    for miles in range(ring_step, radius_miles + 1, ring_step):
        edge = style.MUTED if miles == radius_miles else style.GRID
        width = 0.75 if miles == radius_miles else 0.45
        ax.add_patch(Circle(
            (center_x, center_y),
            miles * 1609.344,
            fill=False,
            edgecolor=edge,
            linewidth=width,
            zorder=2.2,
        ))
        if labels:
            x, y = _census_xy(center_x, center_y, miles, 15)
            ax.text(
                x,
                y,
                rf"{miles}\,mi",
                fontsize=6.2,
                color=style.MUTED,
                ha="left",
                va="bottom",
                zorder=6,
            )

    compass = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    for bearing, label in zip(range(0, 360, 45), compass):
        x, y = _census_xy(center_x, center_y, radius_miles, bearing)
        ax.plot([center_x, x], [center_y, y], color=style.GRID, lw=0.30, zorder=2.1)
        if labels:
            label_x, label_y = _census_xy(
                center_x, center_y, radius_miles * 1.025, bearing
            )
            ax.text(
                label_x,
                label_y,
                label,
                fontsize=6.2,
                color=style.MUTED,
                ha="center",
                va="center",
                zorder=6,
            )


def _draw_census_sites(ax, sites, center_x, center_y):
    order = {"secondary": 0, "relay": 1, "primary": 2, "mixed": 3}
    for site in sorted(sites, key=lambda value: (order[value["service"]], value["n"])):
        x, y = _census_xy(
            center_x,
            center_y,
            site["distance_mi"],
            site["bearing_deg"],
        )
        ax.scatter(
            [x],
            [y],
            s=_census_marker_area(site["n"]),
            marker=_CENSUS_SITE_MARKERS[site["service"]],
            facecolor=_CENSUS_TOL_COLORS[site["tolerance"]],
            edgecolor=style.PAPER,
            linewidth=0.55,
            zorder=4.5,
        )


def _draw_census_center(ax, center_x, center_y, *, label=True):
    ax.scatter(
        [center_x],
        [center_y],
        s=58,
        marker="*",
        facecolor=style.INK,
        edgecolor=style.PAPER,
        linewidth=0.6,
        zorder=7,
    )
    if label:
        ax.annotate(
            r"CHIME / DRAO",
            xy=(center_x, center_y),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=6.8,
            fontweight="bold",
            zorder=7,
        )


def fig_census_map() -> Path:
    rows = read_csv("census_full_500mi.csv")
    inner_rows = read_csv("census_inner_120mi.csv")
    sites = _aggregate_census_sites(rows)
    physical_channels = len({int(row["rf_channel"]) for row in rows})

    fig = plt.figure(figsize=(style.TEXT_WIDTH, 5.68))
    gs = fig.add_gridspec(
        3,
        2,
        width_ratios=[2.72, 1.02],
        height_ratios=[1.12, 0.88, 0.30],
        left=0.018,
        right=0.985,
        bottom=0.105,
        top=0.925,
        wspace=0.08,
        hspace=0.24,
    )

    # Full census.  The source data are range/bearing measurements, so the
    # azimuthal-equidistant projection is both the natural visualization and
    # the one that preserves the supplied geometry exactly.
    ax = fig.add_subplot(gs[:2, 0])
    map_ = _census_background(ax, 500)
    center_x, center_y = map_(_DRAO_LON, _DRAO_LAT)
    ax.add_patch(Circle(
        (center_x, center_y),
        120 * 1609.344,
        facecolor=style.LIGHT_BLUE,
        edgecolor=style.MEASURED,
        linewidth=0.75,
        linestyle=(0, (3, 2)),
        alpha=0.52,
        zorder=2.0,
    ))
    _draw_census_range_grid(ax, center_x, center_y, 500)
    _draw_census_sites(ax, sites, center_x, center_y)
    _draw_census_center(ax, center_x, center_y)

    label_specs = {
        ("Logan Lake", "BC"): (-4, 8, "right"),
        ("Vancouver", "BC"): (-7, -9, "right"),
        ("SEATTLE", "WA"): (-7, -8, "right"),
        ("SPOKANE", "WA"): (7, -2, "left"),
        ("PORTLAND", "OR"): (-7, -8, "right"),
        ("BOISE", "ID"): (7, -7, "left"),
        ("BEND", "OR"): (7, -2, "left"),
        ("EUGENE", "OR"): (-7, 2, "right"),
        ("Calgary", "AB"): (7, -5, "left"),
        ("Edmonton", "AB"): (7, 7, "left"),
        ("Prince George", "BC"): (-7, -11, "right"),
        ("Fort St James", "BC"): (7, 8, "left"),
    }
    # A city can contain several nearby range--bearing sites.  Label it once,
    # at its largest site, and report the city-wide record count; otherwise the
    # repeated city strings overwrite one another at dissertation scale.
    for key, (dx, dy, align) in label_specs.items():
        city_sites = [
            site for site in sites
            if (site["city"], site["state"]) == key
        ]
        if not city_sites:
            continue
        site = max(city_sites, key=lambda value: value["n"])
        city_records = sum(value["n"] for value in city_sites)
        x, y = _census_xy(
            center_x,
            center_y,
            site["distance_mi"],
            site["bearing_deg"],
        )
        city = site["city"].title() if site["city"].isupper() else site["city"]
        ax.annotate(
            city + rf" ({city_records})",
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=5.85,
            ha=align,
            va="center",
            color=style.INK,
            arrowprops=dict(
                arrowstyle="-",
                color=style.MUTED,
                lw=0.35,
                shrinkA=1,
                shrinkB=2,
            ),
            zorder=7,
        )
    zoom_x, zoom_y = _census_xy(center_x, center_y, 121, 105)
    ax.text(
        zoom_x,
        zoom_y,
        r"inner 120-mi zoom",
        fontsize=6.2,
        color=style.MEASURED,
        ha="left",
        va="center",
        zorder=7,
    )
    ax.set_axis_off()
    ax.set_title(
        rf"\textbf{{(a)}} full 500-mile field: {len(rows)} records at "
        rf"{len(sites)} range--bearing sites",
        fontsize=8.8,
        pad=3,
    )

    # Inner detail retains the individual-record geometry from the earlier
    # figure so the nearby population remains readable at dissertation scale.
    ax2 = fig.add_subplot(gs[0, 1])
    map_inner = _census_background(ax2, 126)
    inner_x, inner_y = map_inner(_DRAO_LON, _DRAO_LAT)
    _draw_census_range_grid(
        ax2, inner_x, inner_y, 120, ring_step=40, labels=False
    )
    markers = {
        "Full-power": "s",
        "Class A": "s",
        "Relay": "o",
        "Translator (LPTV)": "^",
        "Low-power (LPTV)": "^",
    }
    colors = {"±1 kHz": style.MEASURED, "None specified": style.MODEL}
    for row in inner_rows:
        x, y = _census_xy(
            inner_x,
            inner_y,
            float(row["distance_km"]) / _KM_PER_MILE,
            float(row["bearing_deg"]),
        )
        color = colors.get(row["frequency_tolerance"], style.PENDING)
        ax2.plot(
            [inner_x, x],
            [inner_y, y],
            color=color,
            alpha=0.18,
            lw=0.4,
            zorder=2.2,
        )
        ax2.scatter(
            [x],
            [y],
            s=18,
            marker=markers.get(row["service_class"], "D"),
            facecolor=color,
            edgecolor=style.PAPER,
            linewidth=0.4,
            zorder=4,
        )
    _draw_census_center(ax2, inner_x, inner_y, label=False)
    ax2.text(
        inner_x,
        inner_y + 8 * 1609.344,
        r"CHIME",
        fontsize=5.8,
        ha="center",
        fontweight="bold",
        zorder=7,
    )
    inset_labels = {
        "CHKL-1": (5, -9, "left"),
        "CHKL-DT+CHBC-DT": (-5, 8, "right"),
        "CH4491-DT": (5, 9, "left"),
        "CHKL-2": (5, -8, "left"),
        "CHCV-DT": (5, -7, "left"),
    }
    for row in inner_rows:
        if row["callsign"] not in inset_labels:
            continue
        x, y = _census_xy(
            inner_x,
            inner_y,
            float(row["distance_km"]) / _KM_PER_MILE,
            float(row["bearing_deg"]),
        )
        label = row["callsign"].replace(
            "CHKL-DT+CHBC-DT", r"CHKL-DT+$\,$CHBC-DT"
        )
        dx, dy, align = inset_labels[row["callsign"]]
        ax2.annotate(
            label,
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=4.7,
            ha=align,
            va="center",
            arrowprops=dict(
                arrowstyle="-",
                color=style.MUTED,
                lw=0.3,
                shrinkA=1,
                shrinkB=1,
            ),
            zorder=7,
        )
    ax2.set_axis_off()
    ax2.set_title(r"\textbf{(b)} inner 120-mile detail", fontsize=8.1, pad=2)

    # The annular summary exposes the strong radial growth of the source
    # population without overloading the geographic panel with labels.
    ax3 = fig.add_subplot(gs[1, 1])
    boundaries = [0, 100, 200, 300, 400, 500]
    annulus_labels = [
        r"$0$--$100$",
        r"$100$--$200$",
        r"$200$--$300$",
        r"$300$--$400$",
        r"$400$--$500$",
    ]
    disciplined = []
    unspecified = []
    site_counts = []
    for low, high in zip(boundaries[:-1], boundaries[1:]):
        epsilon = 1e-8 if high == 500 else 0.0
        selected = [
            row
            for row in rows
            if low
            <= float(row["distance_km"]) / _KM_PER_MILE
            < high + epsilon
        ]
        disciplined.append(
            sum(row["frequency_tolerance"] == "±1 kHz" for row in selected)
        )
        unspecified.append(
            sum(row["frequency_tolerance"] != "±1 kHz" for row in selected)
        )
        site_counts.append(
            sum(
                low <= site["distance_mi"] < high + epsilon
                for site in sites
            )
        )
    positions = np.arange(len(annulus_labels))
    ax3.barh(
        positions,
        disciplined,
        color=style.MEASURED,
        height=0.62,
        label=r"listed $\pm1$ kHz",
    )
    ax3.barh(
        positions,
        unspecified,
        left=disciplined,
        color=style.MODEL,
        height=0.62,
        label=r"no tolerance listed",
    )
    for index, (n_disciplined, n_unspecified, n_sites) in enumerate(
        zip(disciplined, unspecified, site_counts)
    ):
        ax3.text(
            n_disciplined + n_unspecified + 2,
            index,
            rf"{n_disciplined + n_unspecified} / {n_sites}",
            fontsize=5.8,
            va="center",
            color=style.MUTED,
        )
    ax3.set_yticks(positions, annulus_labels)
    ax3.invert_yaxis()
    ax3.set_xlim(0, max(np.asarray(disciplined) + np.asarray(unspecified)) * 1.32)
    ax3.set_xlabel(r"emitter-channel records", fontsize=7.1)
    ax3.tick_params(labelsize=6.3)
    style.clean_axes(ax3, grid="x")
    ax3.set_title(r"\textbf{(c)} records by range annulus", fontsize=8.1, pad=2)

    shape_handles = [
        Line2D(
            [0],
            [0],
            marker=_CENSUS_SITE_MARKERS[key],
            color="none",
            markerfacecolor=style.PENDING,
            markeredgecolor=style.PAPER,
            markersize=5.5,
            label=_CENSUS_SITE_LABELS[key],
        )
        for key in ("primary", "relay", "secondary", "mixed")
    ]
    color_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=_CENSUS_TOL_COLORS[key],
            markeredgecolor=style.PAPER,
            markersize=5.5,
            label=_CENSUS_TOL_LABELS[key],
        )
        for key in ("disciplined", "unspecified", "mixed")
    ]
    legend_ax = fig.add_subplot(gs[2, :])
    legend_ax.set_axis_off()
    shape_legend = legend_ax.legend(
        handles=shape_handles,
        loc="center left",
        bbox_to_anchor=(0, 0.49),
        fontsize=5.75,
        ncol=2,
        columnspacing=0.75,
        handletextpad=0.28,
        borderaxespad=0,
    )
    legend_ax.add_artist(shape_legend)
    color_legend = legend_ax.legend(
        handles=color_handles,
        loc="center",
        bbox_to_anchor=(0.62, 0.49),
        fontsize=5.75,
        ncol=1,
        handletextpad=0.28,
        borderaxespad=0,
    )
    legend_ax.add_artist(color_legend)
    for n_records, x_offset in zip((1, 5, 15), (0.82, 0.88, 0.95)):
        legend_ax.scatter(
            [x_offset],
            [0.62],
            s=_census_marker_area(n_records),
            marker="o",
            facecolor=style.PENDING,
            edgecolor=style.PAPER,
            linewidth=0.5,
            transform=legend_ax.transAxes,
            zorder=8,
        )
        legend_ax.text(
            x_offset,
            0.26,
            str(n_records),
            transform=legend_ax.transAxes,
            ha="center",
            va="top",
            fontsize=5.7,
            color=style.MUTED,
        )
    legend_ax.text(
        0.885,
        0.88,
        r"records at site",
        transform=legend_ax.transAxes,
        ha="center",
        fontsize=5.8,
        color=style.MUTED,
    )
    legend_ax.text(
        0.885,
        0.02,
        rf"{len(rows)} records $\vert$ {len(sites)} sites $\vert$ "
        rf"{physical_channels} physical channels",
        transform=legend_ax.transAxes,
        ha="center",
        fontsize=5.9,
        color=style.INK,
    )

    fig.suptitle(
        r"Inclusive ATSC 1.0 transmitter-census envelope within 500 miles of DRAO",
        fontsize=9.7,
        y=0.982,
    )
    fig.text(
        0.5,
        0.018,
        r"Azimuthal-equidistant vector map: source distance and bearing are "
        r"preserved; boundaries give geographic context, not terrain or propagation.",
        ha="center",
        fontsize=6.5,
        color=style.MUTED,
    )
    return style.save(
        fig,
        OUT / "fig_census_map.pdf",
        title="Conservative 500-mile DTV transmitter-census envelope",
    )


def build_all():
    return [fig_vsb_standard_model(),fig_vsb_layout(),fig_census_map()]
