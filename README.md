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

## Rebuild and verify everything

```bash
make verify
```

This command:

1. regenerates the 17 bundle-scope vector PDFs from bundled Python source
   (nine further active PDFs are vendored, rendered byte-reproducibly by
   `WVURAIL/pilot-proxy` and `WVURAIL/bao-noise-tolerance`; the manifest
   records the generating commit of each);
2. rebuilds the dissertation in three LaTeX passes;
3. verifies the frozen data manifest, every figure source and dependency,
   vector format, embedded Latin Modern fonts, and shared style conventions;
4. runs the portable-export-import provenance regression tests;
5. verifies every Git-tracked release-bundle file against `MANIFEST.sha256`.

Use `make all` for the normal build-and-figure-audit cycle while editing. The
stricter `make verify` additionally checks the frozen release boundary.

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

All tables consumed by bundle-owned figure generators are frozen under
`figure_src/data/frozen_export/v1/` and fingerprinted by
`frozen_data_manifest.json`. The dissertation never imports PilotProxy and
never reads a mutable checkout during a build.

A newer PilotProxy export can be imported atomically with:

```bash
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1 --dry-run
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1
make all
```

The importer verifies the upstream schema, immutable commit record, hashes, and
row counts before replacing matching tables. Its `last_import.json` audit
record uses the portable repository/commit identity and upstream manifest hash,
not the importing machine's absolute path. Unavailable tables remain explicit
bridges rather than being silently synthesized.

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
- `MANIFEST.sha256` — hashes for the complete tracked release boundary
- `scripts/release_manifest.py` — release-manifest generator and verifier
- `evidence/legacy_projects/pilot_informed_detector_article/provenance/` — the
  retained PilotProxy patch, producing commit, decision records, and compact
  legacy provenance

All active external graphics are vector PDFs. Their labels are rendered through
LaTeX using T1-encoded Latin Modern, the same family as the dissertation body.
The build fails rather than silently substituting a different font. No font
files are bundled. Figure and dissertation PDF metadata are fixed so that the
same inputs and toolchain produce byte-for-byte reproducible PDFs.

Four CSV tables remain in the dissertation's frozen interface. The two census
tables are current PilotProxy exports; the two introductory wiggle tables are
explicit external-model/artwork bridges marked `replacement_required`. Other
data-backed active figures are vendored as vector PDFs generated in the
repository that owns their scientific inputs, with the producing commit and
provenance recorded in `figure_src/figure_manifest.csv`. Their larger source
tables are intentionally not duplicated in this bundle.

The two frozen census tables preserve the upstream
`dtv_transmitter_census_v1` schema and each row's `evidence_status`. The
inclusive 499-row map is therefore auditable as a conservative maximum
envelope: 421 rows are reported on air but await licence verification, 67 are
reported on air and licence-matched, and 11 are licence-only candidates rather
than observed carriers.

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
strongest completed part of the work. All 23 ATSC allocations (channels 14--36)
now have survey-, epoch-, and residual-chain products; the first-measured
ten-channel block retains the deepest calibration analysis. These remain
screening results until the pilot-to-allocation transfer, visibility-domain
transfer, combined-bin Fisher estimator, residual-template bank, and per-epoch
holdout tests are completed.

## Release-bundle boundary

`MANIFEST.sha256` covers every path reported by `git ls-files` except the
manifest itself, whose self-exclusion avoids an impossible self-referential
digest. Untracked and ignored build scratch is outside the release bundle. Run
`make manifest` only after final source edits and generated PDFs are complete;
it rebuilds the document, regenerates the manifest, and verifies it. Run
`make manifest-check` for a non-mutating inventory and digest check. CI applies
the same verifier.

## Integrated legacy evidence

Appendix B and the associated main-text cross-references integrate the valuable
legacy content into this dissertation rather than leaving it as an unexplained
sidecar archive. The integrated results include the standards-chain paired
floating-point/int4 injection study, the generator-startup audit, threshold-tail
economics, the off-nominal blind spot, instrument-tone attribution, physical-key
archive joins, recorded-versus-optimal subset selection, and exact rational
threshold checks. Numerical results from earlier detector geometries are labelled
as such and are paired with the current-geometry closing test.
