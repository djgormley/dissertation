# Figure-source, data-interface, and style audit

The dissertation contains 25 active external vector PDFs and two active TikZ
figures. Since the August 2026 reorganization the analysis repositories own
every data-backed figure: nine active PDFs are rendered by
`WVURAIL/pilot-proxy` (`analysis/dissertation/`: both census-PSD plates, the
worked example, the epoch operating points, the status matrix) and
`WVURAIL/bao-noise-tolerance` (`scripts/dissertation/`: the four `bao_*`
forecast figures), and are vendored here as finished, byte-reproducible
PDFs whose generating commit is recorded in the manifest. The remaining
sixteen active visuals -- the analytic schematics, the TikZ diagrams, the
census map (its renderer moves to `WVURAIL/dtv-station-census` when that
repository's map tool lands), and the pedagogical wiggle bridges -- have
editable source inside this bundle. One additional generated PDF,
`fig_vsb_layout.pdf`, is retained as an unused design alternative and is
also source-backed.

The authoritative machine-readable figure inventory is
`figure_src/figure_manifest.csv`. It records, for every artifact:

- the chapter and whether it is active;
- the exact Python function or TikZ source;
- every required frozen data table;
- whether the visual is analytic, repository-export based, curated, or an
  artwork-recovery bridge; and
- the required font and common design conventions.

## Font contract

The dissertation body uses Latin Modern through `lmodern`. Every Matplotlib
figure is generated with `text.usetex=True` and the same T1/Latin Modern
preamble. The generator exits if the TeX toolchain is unavailable; it never
substitutes DejaVu in a production build. TikZ figures inherit the document
typography.

The audit runs `pdffonts` over every generated PDF and requires all fonts to be
embedded Latin Modern fonts. Type 3 fonts and DejaVu are rejected. It also
checks that active chapter figures are PDFs rather than PNG/JPEG files.

## Coherent visual conventions

All Python figures share `figure_src/style.py`; all TikZ figures share
`figure_src/tikz/figure_styles.tikz`. The two sources use the same palette:

The palette is drawn from the WVU visual-identity color system
(scm.wvu.edu/brand/visual-identity/):

| Meaning | Color |
|---|---|
| measured/instrument evidence | WVU safety blue `#0062A3` |
| model/calibration/transfer | WVU old gold `#7F6310` |
| conditional/feasible | WVU hemlock `#6A724F` |
| failure/excision | WVU woodburn `#8D4638` |
| pending/context | WVU seneca gray `#988E8B` |

Two additional series colors (WVU sunset `#F58672` and WVU gold `#EEAA00`)
appear only where a figure needs more than the five roles. The flagship WVU
gold is reserved for lines and fills: at small text sizes its contrast on
white is too low, so the model/transfer role uses the darker old gold.

Line weights, grid treatment, panel labels, text canvas width, and vector export
are centralized rather than chosen independently by each figure.

## Repository/dissertation boundary

The dissertation is self-contained, but it is not the scientific source of
truth. PilotProxy owns the detector, archive reductions, validation, and small
scientific exports. The dissertation owns the rendering layer.

`figure_src/data/frozen_export/v1/frozen_data_manifest.json` is the frozen data
ledger. It records the upstream PilotProxy commit, ownership, authority, row
counts, SHA-256 hashes, and replacement status. The plotting modules read this
one directory; no value table has a second loose copy elsewhere in the bundle.

The frozen interface now carries only the tables this bundle still renders
from: the conservative 500-mile transmitter-census envelope and its 120-mile subset
(behind the census map), and the two pedagogical wiggle bridges. Every
other table moved to the repository that owns its figure, with its
regeneration commands documented beside it (`analysis/dissertation/data/`
in pilot-proxy; `scripts/dissertation/data/` in bao-noise-tolerance).


### Figure 3.2: full transmitter field

Figure 3.2 reads the inclusive `census_full_500mi.csv` PilotProxy export (499 emitter-channel records; since August 2026 the underlying census is the workbook reduction plus dtv-station-census's ISED overlay -- licensed transmitter sites, licence-status adjudication, and ERP) and the independently frozen 120-mile subset. The rows preserve their evidence split: 421 reported-on-air/unverified, 67 reported-on-air/licence-matched, and 11 licence-only candidates. The full panel aggregates exactly coincident source range-bearing records into 162 sites, with marker area retaining multiplicity. It uses a DRAO-centred azimuthal-equidistant projection so the supplied distance and bearing remain exact; coastlines and administrative boundaries are vector context only and do not represent terrain or propagation.

## Remaining provenance limitation

Two frozen tables still require authoritative replacement:

- `intro_wiggle_correlation.csv` and `intro_wiggle_power.csv` (the
  CAMB-or-accept decision).

The other two artwork bridges, `bao_convergence.csv` and
`bao_two_walls.csv`, moved to bao-noise-tolerance with their figures and
keep their bridge status there.

(`worked_example_spectra.csv` was replaced in August 2026: the two frames
were located in the fid-506 archive product — frames 2606 and 1226, events
1126624080 and 1116626388 — and their per-frame fine spectra verified against
the published T[60..64] and designated-window values before export.)

They were recovered from vector paths because the authoritative arrays were not
present in the supplied dissertation archive. The retained reference PDFs,
extraction script, hashes, and recovery statement remain in the bundle. These
tables make the draft exactly reproducible and editable; they do not convert the
recovered curves into authoritative measurements.

A future versioned PilotProxy/Fisher export can replace matching bridge tables
with `python3 -m figure_src.import_dissertation_export ...`. The plotting source,
font contract, and visual design do not need to change when that happens.
