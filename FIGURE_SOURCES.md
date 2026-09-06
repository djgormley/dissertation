# Figure-source, data-interface, and style audit

Since the August 2026 reorganization the analysis repositories own every
data-backed result figure. `WVURAIL/pilot-proxy` supplies the health-corrected
census plates, worked example, provisional epoch/status views, and 23
all-channel diagnostic atlases, as well as the digital and over-the-air
estimator-transfer figures; `WVURAIL/RFIsher` supplies the forecast
figures, including the all-seven-bin analytic-template comparison. The four
current RFIsher application PDFs were rendered at commit
`2603788363c187ae37a74226d78f394a716b803d` and are byte-reproducible. The
template-comparison PDF remains attached to its immutable dated release at
commit `3c806c2e435baccc3195618f4ab1ce55aa5887c2`. They are vendored here with
their generating commits and evidence releases recorded in the manifest. The analytic
schematics, TikZ diagrams, census map, and pedagogical wiggle bridges retain
editable source inside this bundle. `fig_vsb_layout.pdf` is retained as an
unused source-backed alternative. The generated `FIGURE_AUDIT_REPORT.md`, not
this prose overview, records the exact counts for each frozen release.

RFIsher 3.0 removes the former package and compatibility namespaces, but it does
not alter the numerical arrays underlying these pinned application figures.
The frozen inputs and figures remain authenticated pre-v3 snapshots and are not
restamped merely because the current public API changed.

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
scientific exports, including the estimator-transfer rendering. The
dissertation owns self-contained integration and the analytic-schematic
rendering layer.

`figure_src/data/frozen_export/v1/frozen_data_manifest.json` is the frozen data
ledger. It records the upstream PilotProxy commit, ownership, authority, row
counts, SHA-256 hashes, and replacement status. The plotting modules read this
one directory; no value table has a second loose copy elsewhere in the bundle.

The frozen interface now carries only the tables this bundle still renders
from: the conservative 500-mile transmitter-census envelope and its 120-mile subset
(behind the census map), and the two pedagogical wiggle bridges. Every
other table moved to the repository that owns its figure, with its
regeneration commands documented beside it (`analysis/dissertation/data/`
in pilot-proxy; `scripts/dissertation/data/` in RFIsher).

The census pair was re-imported from reachable PilotProxy commit
`24586f54fdf41e0b77c6ab07aaf55153cd61c778`; both CSVs are byte-identical to
the prior frozen export. The current PilotProxy history no longer contains
several older producer commits recorded by the vendored result figures and
health release. Their artifact hashes and release ledgers remain verifiable,
but source-level regeneration requires restored archival refs or a matching
source bundle. Their manifests are intentionally not rewritten to a convenient
new commit.

The dated forecast release under
`evidence/bao_forecast_completion_20260824_reconciliation/` authenticates the
template-comparison figure. Its four analytic ledgers were built and evaluated
at RFIsher commit `1d7de4f0329772a18320d390bbe7eab12c3d9a0c` with RadioFisher commit
`f6bc9ea0972028ce30472dd21b25d4b21b7068c0`. The earlier undated release is
retained unchanged.

## Estimator-transfer figures

The digital transfer figure is vendored from
`evidence/estimator_transfer_20260825/`. It compares the floating-point CPU,
fixed-point GPU, and packed-input CPU estimators over commanded inputs from
$-60$ to $+60$ dB. Its compact points table pools the declared trial shards;
the release inventory authenticates the external raw trial tree.

The over-the-air transfer figure is vendored from
`evidence/sdr_ota_transfer_20260825/`. It covers commanded inputs from $-42$
to $0$ dB through the two LimeSDR RF ports and reports pass-bootstrap
uncertainty. Its run records and quality-control table retain the hardware,
stream, marker, clipping, and fit checks, while the raw-capture inventory
authenticates the external captures.

Both figures and their compact releases are immediately post-run archival
snapshots. The publication PDFs in `figs/` are byte-identical to their owner
copies. These figures test estimator transfer only: no decision threshold,
false-alarm target, or receiver-operating-characteristic sweep enters either
measurement.


### Figure 3.2: full transmitter field

Figure 3.2 reads the inclusive `census_full_500mi.csv` PilotProxy export (499 emitter-channel records; since August 2026 the underlying census is the workbook reduction plus dtv-station-census's ISED overlay -- licensed transmitter sites, licence-status adjudication, and ERP) and the independently frozen 120-mile subset. The rows preserve their evidence split: 421 reported-on-air/unverified, 67 reported-on-air/licence-matched, and 11 licence-only candidates. The full panel aggregates exactly coincident source range-bearing records into 162 sites, with marker area retaining multiplicity. It uses a DRAO-centred azimuthal-equidistant projection so the supplied distance and bearing remain exact; coastlines and administrative boundaries are vector context only and do not represent terrain or propagation.

## Remaining provenance limitation

Two frozen tables still require authoritative replacement:

- `intro_wiggle_correlation.csv` and `intro_wiggle_power.csv` (the
  CAMB-or-accept decision).

The other two artwork bridges moved to RFIsher with their figures:
`bao_convergence.csv` keeps its bridge status there, while
`bao_two_walls.csv` was retired as a bridge --- RFIsher's
`make_two_walls.py` regenerates it directly from the survey products.

(`worked_example_spectra.csv` was replaced in August 2026: the two frames
were located in the fid-506 archive product — frames 2606 and 1226, events
1126624080 and 1116626388 — and their per-frame fine spectra verified against
the published T[60..64] and designated-window values before export.)

They were recovered from vector paths because the authoritative arrays were not
present in the supplied dissertation archive. The retained reference PDFs,
extraction script, hashes, and recovery statement remain in the bundle. These
tables make the draft exactly reproducible and editable; they do not convert the
recovered curves into authoritative measurements.

Separately, the Kotekan feature-stage vendor manifest names a PilotProxy source
commit that is not resolvable in the current re-rooted upstream history. The
candidate stage is cited by its Kotekan commit and per-file hashes; production
adoption still requires re-vendoring from a resolvable PilotProxy release or
restoring the named source snapshot.

A future versioned PilotProxy/Fisher export can replace matching bridge tables
with `python3 -m figure_src.import_dissertation_export ...`. The plotting source,
font contract, and visual design do not need to change when that happens.
