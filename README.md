# The Pilot-Proxy Method — revised dissertation bundle

This directory contains the revised LaTeX source, compiled dissertation, a
fully source-backed figure system, and a frozen scientific-data interface for
Dylan Gormley. The document entry point is `dissertation.tex`; the compiled
output is `dissertation.pdf`.

The revision preserves the dissertation's pedagogical voice while narrowing
claims to the evidence actually available. No missing survey, visibility,
calibration, or Fisher-analysis results were invented. Quantities that require
analysis products or code are labeled as pending, conditional, bounded, or
refused in the dissertation and evidence appendix.

## Rebuild everything

```bash
make all
```

This command:

1. regenerates every bundle-owned PDF from bundled Python source; current
   result PDFs and the 23 channel diagnostic atlases are vendored from
   `WVURAIL/pilot-proxy` and `WVURAIL/bao-noise-tolerance`, with producer
   commits and immutable inputs recorded by the manifest;
2. rebuilds the dissertation in three LaTeX passes;
3. verifies the frozen data manifest, every figure source and dependency,
   vector format, embedded Latin Modern fonts, shared style conventions, and
   the hashes and reconciliation invariants of the vendored result releases.

The two architecture diagrams are native TikZ files included directly from
`figure_src/tikz/`. The generated `FIGURE_AUDIT_REPORT.md` records the exact
active, vendored, bundle-rendered, and inactive counts for the frozen release;
`figure_src/figure_manifest.csv` is the authoritative per-artifact inventory.

## Repository/dissertation separation

The dissertation is independently buildable, but it is not a second scientific
analysis repository.

- **PilotProxy owns scientific computation, validation, provenance, and small
  versioned data exports.**
- **This bundle owns dissertation-specific plotting, typography, layout, and
  explanatory TikZ.**

All figure tables are frozen under `figure_src/data/frozen_export/v1/` and
fingerprinted by `frozen_data_manifest.json`. The dissertation never imports
PilotProxy and never reads a mutable checkout during a build.

A newer PilotProxy export can be imported atomically with:

```bash
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1 --dry-run
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1
make all
```

The importer verifies the upstream schema, commit record, hashes, and row counts
before replacing matching tables. Unavailable tables remain explicit bridges
rather than being silently synthesized.

## Figure and data reproducibility

- `FIGURE_SOURCES.md` — human-readable figure/data ownership overview
- `FIGURE_AUDIT_REPORT.md` — machine-generated source, font, vector, and data audit
- `BUILD_VERIFICATION.md` — clean-room build and rendering checks
- `figure_src/figure_manifest.csv` — complete figure-to-source/data mapping
- `figure_src/data/frozen_export/v1/frozen_data_manifest.json` — table ownership,
  authority, hashes, and replacement status
- `figure_src/import_dissertation_export.py` — verified upstream-import tool
- `figure_src/style.py` — shared Matplotlib font, sizing, palette, and line rules
- `figure_src/tikz/figure_styles.tikz` — matching TikZ conventions
- `figure_src/README.md` — figure editing and export-import workflow
- `requirements-figures.txt` — Python dependencies
- `CANFAR_PRODUCT_HEALTH_AUDIT.json` — machine-readable all-23 product-health
  audit, including validity, saturation/fill, and fine-designation findings
- `scripts/verify_vendored_evidence.py` — standard-library CI check for the
  immutable BAO and CANFAR evidence releases and their reconciliation invariants
- `evidence/legacy_projects/pilot_informed_detector_article/provenance/` — the
  retained PilotProxy patch, producing commit, decision records, and compact
  legacy provenance

All active external graphics use PDF containers. Bundle-rendered plots and
repository result figures are vector PDFs; the 23 diagnostic atlases
deliberately embed declared raster heatmaps alongside vector histogram and
spectrum panels. Their labels are rendered through LaTeX using T1-encoded
Latin Modern, the same family as the dissertation body.
The build fails rather than silently substituting a different font. No font
files are bundled. Figure and dissertation PDF metadata are fixed so that the
same inputs and toolchain produce byte-for-byte reproducible PDFs.

The dissertation-local frozen interface currently contains four CSV tables.
Two are authoritative PilotProxy census exports
(`census_full_500mi.csv` and `census_inner_120mi.csv`); two are pedagogical
external-model bridges (`intro_wiggle_correlation.csv` and
`intro_wiggle_power.csv`). Only the two bridge tables are marked
`replacement_required`. Data behind the vendored result PDFs remain owned and
validated by their analysis repositories rather than being duplicated in this
local interface. The reference PDF, recovery provenance, checksums, and
limitation statement are retained so that either bridge can later be replaced
without redesigning its figure.

## Other important files

- `dissertation.tex` — master document and front matter
- `chapters/` — Chapters 1–11, bibliography, and evidence appendix
- `figs/` — generated vector PDFs used by the LaTeX build
- `REVISION_NOTES.md` — substantive dissertation changes and checks
- `REVIEW_RESPONSE.md` — disposition of the supplied review
- `archive_completion_checklist.md` — measurements and release records still needed
- `evidence/` — immutable current archive-health and BAO-forecast releases plus
  curated legacy projects, fixed reference PDFs, compact data, source
  generators, provenance notes, and release manifests; Appendices B and C state
  the current/legacy reuse boundaries

## Evidence status

The exact-arithmetic detector and its exercised implementation contracts are the
strongest completed part of the work. The offline CANFAR trawl now covers all
23 ATSC allocations (channels 14--36), including channels 14 and 15, and the
dissertation carries an all-band archive and residual-chain screening result.
Coverage is not the same as a final operations recommendation.  The completed
release audit now applies a fail-closed v1 health gate to the four all-zero
detector-invalid frames and 178 mathematically identified constant-ceiling
frames, writes an immutable reason-coded ledger, exactly repairs their
aggregate spectral contribution, and recomputes fine designated-window
diagnostics from the retained 256-bin arrays rather than using the archived
bin-0 ancillary CFAR fields.  The all-23-channel results remain screening
results until the current-geometry synthetic sensitivity/fixed-point-loss
study, pilot-to-allocation transfer, visibility-domain transfer, empirical
residual-template fit, and per-epoch holdout tests are completed or the
affected claims are explicitly kept conditional.  The code-side forecast gate
is now closed: the collaboration-style combined-bin estimator has been executed
over all seven DTV redshift bins for four normalized analytic residual families
and both declared time-scaling models.  Those calculations define a sensitivity
envelope; they do not select a physical template in the absence of
visibility-domain frequency, baseline, and sidereal structure.

## Integrated legacy evidence

Appendix B and the associated main-text cross-references integrate the valuable
legacy content into this dissertation rather than leaving it as an unexplained
sidecar archive. The integrated results include the standards-chain paired
floating-point/int4 injection study, the generator-startup audit, threshold-tail
economics, the off-nominal blind spot, instrument-tone attribution, physical-key
archive joins, recorded-versus-optimal subset selection, and exact rational
threshold checks. Numerical results from earlier detector geometries are labelled
as such and are paired with the current-geometry closing test.
