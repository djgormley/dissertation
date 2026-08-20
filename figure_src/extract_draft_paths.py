#!/usr/bin/env python3
"""Recover editable data tables from vector artwork in the supplied draft.

The August 2026 bundle did not include the authoritative arrays or original
programs for several scientific plots.  This one-time bridge extracts the
Matplotlib vector paths from those PDFs and writes ordinary CSV files.  Normal
figure regeneration uses the CSVs and does not depend on PyMuPDF or the legacy
PDFs.  Artwork recovery is explicitly not a substitute for archiving direct
analysis outputs; see ``data/frozen_export/v1/frozen_data_manifest.json``.
"""
from __future__ import annotations

import csv
import hashlib
import math
from pathlib import Path
from typing import Iterable

import fitz
import numpy as np

HERE = Path(__file__).resolve().parent
REF = HERE / "legacy_reference"
DATA = HERE / "data" / "frozen_export" / "v1"
DATA.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def polyline(page: fitz.Page, drawing_index: int) -> np.ndarray:
    d = page.get_drawings()[drawing_index]
    pts: list[tuple[float, float]] = []
    for item in d["items"]:
        if item[0] == "l":
            p0, p1 = item[1], item[2]
            if not pts:
                pts.append((p0.x, p0.y))
            pts.append((p1.x, p1.y))
        elif item[0] == "c":
            if not pts:
                p0 = item[1]; pts.append((p0.x, p0.y))
            p3 = item[-1]; pts.append((p3.x, p3.y))
    if len(pts) < 2:
        raise RuntimeError(f"drawing {drawing_index} has no polyline")
    return np.asarray(pts, dtype=float)


def linear(values, p0, p1, v0, v1):
    return v0 + (np.asarray(values)-p0)*(v1-v0)/(p1-p0)


def log_map(values, p0, p1, v0, v1):
    return 10 ** linear(values, p0, p1, math.log10(v0), math.log10(v1))


def y_linear(values, ptop, pbottom, vlo, vhi):
    return vhi - (np.asarray(values)-ptop)*(vhi-vlo)/(pbottom-ptop)


def y_log(values, ptop, pbottom, vlo, vhi):
    return 10 ** (math.log10(vhi) - (np.asarray(values)-ptop)
                  * (math.log10(vhi)-math.log10(vlo))/(pbottom-ptop))


def write(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def extract_intro_wiggle() -> None:
    page = fitz.open(REF / "fig_intro_wiggle_original.pdf")[0]
    p = polyline(page, 133)
    x = linear(p[:, 0], 41.2000008, 222.430771, 30.0, 210.0)
    y = y_linear(p[:, 1], 21.0750122, 197.331009, -5.0, 70.0)
    write(DATA / "intro_wiggle_correlation.csv", ["separation_mpc", "r2_xi"],
          ({"separation_mpc": f"{a:.9g}", "r2_xi": f"{b:.9g}"} for a,b in zip(x,y)))
    p = polyline(page, 260)
    x = log_map(p[:,0], 284.049225, 465.279999, 0.035, 0.5)
    y = y_linear(p[:,1], 21.0750122, 197.331009, 0.94, 1.065)
    write(DATA / "intro_wiggle_power.csv", ["k_mpc_inv", "p_over_psmooth"],
          ({"k_mpc_inv": f"{a:.9g}", "p_over_psmooth": f"{b:.9g}"} for a,b in zip(x,y)))


def extract_worked_example() -> None:
    page = fitz.open(REF / "fig_worked_example_original.pdf")[0]
    specs = [
        ("a", 58, (45.2000008,21.1999817,402.320007,126.799988),1.009,18.62),
        ("b",382,(45.2000008,175.375992,402.320007,280.975983),0.833,2.59),
    ]
    rows=[]
    for panel,idx,(x0,y0,x1,y1),med,peak in specs:
        p=polyline(page,idx)
        x=linear(p[:,0],x0,x1,-0.5,255.5)
        z=(y1-p[:,1])/(y1-y0)
        zm=float(np.median(z)); zx=float(np.max(z))
        a=(math.log(peak)-math.log(med))/(zx-zm)
        yy=np.exp(a*z + math.log(med)-a*zm)
        rows.extend({"panel":panel,"fine_bin":f"{xx:.9g}","T":f"{v:.9g}"} for xx,v in zip(x,yy))
    write(DATA/"worked_example_spectra.csv",["panel","fine_bin","T"],rows)


def extract_census_psd() -> None:
    page=fitz.open(REF/"fig_census_psd_original.pdf")[0]
    indices=[38,73,101,148,175,206,252,310,378,450]
    boxes=[
        (38.5125008,61.1999512,190.989243,196.827881),
        (224.534134,61.1999512,377.010864,196.827881),
        (410.555756,61.1999512,563.032471,196.827881),
        (38.5125008,210.390686,190.989243,346.018585),
        (224.534134,210.390686,377.010864,346.018585),
        (410.555756,210.390686,563.032471,346.018585),
        (38.5125008,359.581360,190.989243,495.209290),
        (224.534134,359.581360,377.010864,495.209290),
        (410.555756,359.581360,563.032471,495.209290),
        (38.5125008,508.772064,190.989243,644.399963),
    ]
    yranges=[(-2,34),(-.5,11),(-.8,6.3),(-2,42),(-2,28),(-2,38),(-1,21.5),(-.5,6.5),(-1.5,25),(-1,16)]
    rows=[]
    for ch,idx,(x0,y0,x1,y1),(lo,hi) in zip(range(27,37),indices,boxes,yranges):
        p=polyline(page,idx)
        x=linear(p[:,0],x0,x1,-15,15); y=y_linear(p[:,1],y0,y1,lo,hi)
        rows.extend({"channel":ch,"offset_khz":f"{a:.9g}","db_rel_median":f"{b:.9g}"} for a,b in zip(x,y))
    write(DATA/"census_psd.csv",["channel","offset_khz","db_rel_median"],rows)


def extract_bao_time() -> None:
    page=fitz.open(REF/"fig_bao_time_vs_masking_original.pdf")[0]
    rows=[]
    for idx,name in [(156,"dilation"),(157,"bin_amplitude"),(158,"survey_amplitude")]:
        p=polyline(page,idx)
        x=linear(p[:,0],66.1253433,453.117,0.0,1.0)
        y=y_log(p[:,1],60.457,274.922,0.03,10.0)
        rows.extend({"series":name,"masked_fraction":f"{a:.9g}","time_year":f"{b:.9g}"} for a,b in zip(x,y))
    write(DATA/"bao_time_vs_masking.csv",["series","masked_fraction","time_year"],rows)


def extract_bao_convergence() -> None:
    page=fitz.open(REF/"fig_bao_convergence_original.pdf")[0]
    rows=[]
    p=polyline(page,164)
    x=log_map(p[:,0],68.610,181.134,0.1,10.0)
    y=log_map(p[:,1],127.286,33.712,1e-3,1e-2)
    rows.extend({"panel":"clean_sigma","series":"clean","time_year":f"{a:.9g}","value":f"{b:.9g}"} for a,b in zip(x,y))
    for idx,name in [(456,"keep_everything"),(457,"mad"),(458,"spectral_kurtosis"),(459,"pilot_proxy")]:
        p=polyline(page,idx)
        x=log_map(p[:,0],273.675,386.199,0.1,10.0)
        y=y_log(p[:,1],22.294,155.926,1e-3,1e6)
        rows.extend({"panel":"bias_sigma","series":name,"time_year":f"{a:.9g}","value":f"{b:.9g}"} for a,b in zip(x,y))
    write(DATA/"bao_convergence.csv",["panel","series","time_year","value"],rows)


def extract_two_walls() -> None:
    page=fitz.open(REF/"fig_bao_two_walls_original.pdf")[0]
    mapping={665:(30,"stated"),666:(28,"stated"),667:(29,"measured"),668:(27,"stated"),
             669:(31,"measured"),670:(32,"measured"),671:(33,"measured"),
             672:(34,"stated"),673:(35,"measured"),674:(36,"stated")}
    rows=[]
    for idx,(ch,evidence) in mapping.items():
        p=polyline(page,idx)[::-1]
        x=linear(p[:,0],57.6599998,481.739990,0.0,1.04)
        y=y_log(p[:,1],21.6687317,287.780731,2e-3,3e4)
        rows.extend({"channel":ch,"evidence":evidence,"order":i,
                     "masked_fraction":f"{a:.9g}","r_over_rtol":f"{b:.9g}"}
                    for i,(a,b) in enumerate(zip(x,y)))
    write(DATA/"bao_two_walls.csv",
          ["channel","evidence","order","masked_fraction","r_over_rtol"],rows)


def provenance() -> None:
    refs=sorted(REF.glob("*.pdf"))
    text=[
        "# Recovered draft-figure data provenance","",
        "The supplied dissertation contained scientific curves whose authoritative",
        "arrays and original plotting programs were not included.  The CSVs in this",
        "directory were recovered from vector paths by `extract_draft_paths.py`.",
        "They preserve the supplied draft artwork and make every figure editable;",
        "they are not a replacement for direct exports from the analysis pipeline.","",
        "When direct result tables are archived, replace the corresponding CSV while",
        "keeping the generator and styling layer unchanged.","",
        "## Reference PDFs","","| file | SHA-256 |","|---|---|",
    ]
    text += [f"| `{p.name}` | `{sha256(p)}` |" for p in refs]
    text += ["","## Recovered tables","",
        "- `intro_wiggle_*.csv`: CAMB-derived pedagogical curves.",
        "- `worked_example_spectra.csv`: the two plotted fine spectra; the vertical",
        "  transform is anchored to the medians and maxima printed in the draft.",
        "- `census_psd.csv`: ten archive-averaged spectra in Chapter 3.",
        "- `bao_time_vs_masking.csv`: the three mask-cost curves.",
        "- `bao_convergence.csv`: clean-error and bias-significance curves.",
        "- `bao_two_walls.csv`: ten threshold-sweep curves.",""]
    (DATA/"legacy_recovery_provenance.md").write_text("\n".join(text),encoding="utf-8")


def main() -> None:
    extract_intro_wiggle(); extract_worked_example(); extract_census_psd()
    extract_bao_time(); extract_bao_convergence(); extract_two_walls(); provenance()
    print(f"Recovered editable CSVs in {DATA}")

if __name__ == "__main__":
    main()
