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

1. regenerates the 17 bundle-scope vector PDFs from bundled Python source
   (nine further active PDFs are vendored, rendered byte-reproducibly by
   `WVURAIL/pilot-proxy` and `WVURAIL/bao-noise-tolerance`; the manifest
   records the generating commit of each);
2. rebuilds the dissertation in three LaTeX passes;
3. verifies the frozen data manifest, every figure source and dependency,
   vector format, embedded Latin Modern fonts, and shared style conventions.

The two architecture diagrams are native TikZ files included directly from
`figure_src/tikz/`. Twenty-five external PDFs and both TikZ figures are
active in the document (sixteen rendered here, nine vendored from the
analysis repositories); one additional generated PDF is retained as an
editable unused alternative.

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
- `evidence/legacy_projects/pilot_informed_detector_article/provenance/` — the
  retained PilotProxy patch, producing commit, decision records, and compact
  legacy provenance

All active external graphics are vector PDFs. Their labels are rendered through
LaTeX using T1-encoded Latin Modern, the same family as the dissertation body.
The build fails rather than silently substituting a different font. No font
files are bundled. Figure and dissertation PDF metadata are fixed so that the
same inputs and toolchain produce byte-for-byte reproducible PDFs.

Twelve CSV tables feed the active figures. Eight are represented by the
current PilotProxy export boundary (the August 2026 v2 export replaced the
recovered census-spectra, observing-time, and worked-example tables with
direct result exports — the worked-example frames were located in the archive
products and verified against the published values digit-for-digit); four
remain explicit legacy-artwork or external-model bridges. The reference PDFs,
recovery script, checksums, and limitation statement are retained. Those four
tables are marked `replacement_required` and can be replaced without
redesigning the figures.

## Other important files

- `dissertation.tex` — master document and front matter
- `chapters/` — Chapters 1–11, bibliography, and evidence appendix
- `figs/` — generated vector PDFs used by the LaTeX build
- `REVISION_NOTES.md` — substantive dissertation changes and checks
- `REVIEW_RESPONSE.md` — disposition of the supplied review
- `archive_completion_checklist.md` — measurements and release records still needed
- `evidence/` — curated legacy projects, fixed reference PDFs, compact data,
  source generators, provenance notes, and a release manifest; Appendix B states
  the reuse boundary

## Evidence status

The exact-arithmetic detector and its exercised implementation contracts are the
strongest completed part of the work. The present ten-channel cosmology results
remain screening results until the pilot-to-allocation transfer,
visibility-domain transfer, combined-bin Fisher estimator, residual-template
bank, and per-epoch holdout tests are completed. Eleven of the remaining
thirteen ATSC allocations (channels 16--26) gained survey- and epoch-level
products in the August 2026 completion; channels 14 and 15 still have none.

## Integrated legacy evidence

Appendix B and the associated main-text cross-references integrate the valuable
legacy content into this dissertation rather than leaving it as an unexplained
sidecar archive. The integrated results include the standards-chain paired
floating-point/int4 injection study, the generator-startup audit, threshold-tail
economics, the off-nominal blind spot, instrument-tone attribution, physical-key
archive joins, recorded-versus-optimal subset selection, and exact rational
threshold checks. Numerical results from earlier detector geometries are labelled
as such and are paired with the current-geometry closing test.
