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

1. regenerates every bundle-owned PDF from bundled Python source; current
   result PDFs and the 23 channel diagnostic atlases are vendored from
   `WVURAIL/pilot-proxy` and `WVURAIL/RFIsher`, with producer commits and
   immutable inputs recorded by the manifest;
2. rebuilds the dissertation in three LaTeX passes;
3. verifies the frozen data manifest, every figure source and dependency,
   vector format, embedded Latin Modern fonts, shared style conventions, and
   the hashes and reconciliation invariants of the vendored result releases;
4. runs the portable-export-import provenance regression tests;
5. verifies every Git-tracked release-bundle file against `MANIFEST.sha256`.

Use `make all` for the normal build-and-figure-audit cycle while editing. The
stricter `make verify` additionally checks the frozen release boundary.

The two architecture diagrams are native TikZ files included directly from
`figure_src/tikz/`. The generated `FIGURE_AUDIT_REPORT.md` records the exact
active, vendored, bundle-rendered, and inactive counts for the frozen release;
`figure_src/figure_manifest.csv` is the authoritative per-artifact inventory.

## Repository/dissertation separation

The dissertation is independently buildable, but it is not a second scientific
analysis repository.

- **PilotProxy owns detector and archive computation, validation, provenance,
  and small versioned data exports.**
- **RFIsher owns the masking-cost and contamination-residual tolerance workflow and results.**
- **RadioFisher is the forecast backend used by RFIsher.**
- **Kotekan owns the candidate real-time framework stage; its current CHORD
  implementation is feature-branch software, not a completed telescope
  deployment.**
- **This bundle owns dissertation-specific plotting, typography, layout, and
  explanatory TikZ.**

The current software surfaces are PilotProxy's 2.0 development line and
RFIsher 3.0. RFIsher exposes only the `rfisher` namespace, while PilotProxy
owns its archive runtime under `pilot_proxy.archive` and exposes the
`pilot-proxy` program. The retired Datatrawl repository and former package or
command aliases are not current interfaces. Historical schemas, evidence
records, and pre-v3 RFIsher data snapshots keep their recorded names and hashes;
they are not restamped to imitate the current API.

All tables consumed by bundle-owned figure generators are frozen under
`figure_src/data/frozen_export/v1/` and fingerprinted by
`frozen_data_manifest.json`. The dissertation never imports PilotProxy and
never reads a mutable checkout during a build.

The two census tables were re-imported from PilotProxy commit
`24586f54fdf41e0b77c6ab07aaf55153cd61c778`; their bytes and SHA-256 digests are
unchanged from the prior export. Several older PilotProxy commits recorded by
immutable figures and evidence releases are no longer reachable after the
upstream history was re-rooted. Those artifacts remain hash-authenticated in
this bundle, but full source recovery requires restored archival refs or a
source snapshot and must not be simulated by changing their producer pins.

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
- `CANFAR_PRODUCT_HEALTH_AUDIT.json` — machine-readable all-23 product-health
  audit, including validity, saturation/fill, and fine-designation findings
- `MANIFEST.sha256` — hashes for the complete tracked release boundary
- `scripts/release_manifest.py` — release-manifest generator and verifier
- `scripts/verify_vendored_evidence.py` — standard-library check of the
  immutable forecast and CANFAR evidence releases and their reconciliation
  invariants; runs locally (`make evidence-audit`) against the `evidence/`
  tree, which is kept outside the repository, and is skipped in CI
- `evidence/bao_forecast_completion_20260824_reconciliation/` — dated RFIsher
  forecast release for the BAO application, with four analytic families on one
  clean evaluation commit
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

Four CSV tables remain in the dissertation's frozen interface. The two census
tables are current PilotProxy exports; the two introductory wiggle tables are
explicit external-model/artwork bridges marked `replacement_required`. The
reference PDF, recovery provenance, checksums, and limitation statement are
retained so that either bridge can later be replaced without redesigning its
figure. Other data-backed active figures are vendored as vector PDFs generated
in the repository that owns their scientific inputs, with the producing commit
and provenance recorded in `figure_src/figure_manifest.csv`. Their larger
source tables are intentionally not duplicated in this bundle.

The two frozen census tables preserve the upstream
`dtv_transmitter_census_v1` schema and each row's `evidence_status`. The
inclusive 499-row map is therefore auditable as a conservative maximum
envelope: 421 rows are reported on air but await licence verification, 67 are
reported on air and licence-matched, and 11 are licence-only candidates rather
than observed carriers.

## Other important files

- `dissertation.tex` — master document and front matter
- `chapters/` — Chapters 1–11, bibliography, and Appendices A–C
- `figs/` — generated vector PDFs used by the LaTeX build
- `REVISION_NOTES.md` — substantive dissertation changes and checks
- `REVIEW_RESPONSE.md` — disposition of the supplied review
- `archive_completion_checklist.md` — measurements and release records still needed
- `evidence/` — immutable current archive-health and forecast releases plus
  curated legacy projects, fixed reference PDFs, compact data, source
  generators, provenance notes, and release manifests; Appendices B and C state
  the current/legacy reuse boundaries

## Evidence status

The exact-arithmetic detector and its exercised implementation contracts are the
strongest completed part of the work. The offline CANFAR trawl now covers all
23 ATSC allocations (channels 14--36), including channels 14 and 15, and the
dissertation carries an all-band archive and residual-chain screening result;
the first-measured ten-channel block retains the deepest calibration analysis.
Coverage is not the same as a final operations recommendation.  The completed
release audit now applies a fail-closed v1 health gate to the four all-zero
detector-invalid frames and 178 mathematically identified constant-ceiling
frames, writes an immutable reason-coded ledger, exactly repairs their
aggregate spectral contribution, and recomputes fine designated-window
  diagnostics from the retained 256-bin arrays rather than using the archived
  bin-0 ancillary CFAR fields. The threshold-free coarse-estimator transfer is
  now complete across the fully digital and controlled radio-path sweeps. The
  all-23-channel results remain screening results until the current-geometry
  full-$2048$ fine-statistic sensitivity, threshold, and representation-loss
  study, pilot-to-allocation transfer, visibility-domain transfer, empirical
  residual-template fit, and per-epoch holdout tests are completed or the
  affected claims are explicitly kept conditional. The code-side forecast gate
is now closed: the collaboration-style combined-bin estimator has been executed
over all seven DTV redshift bins for four normalized analytic residual families
and both declared time-scaling models.  Those calculations define a sensitivity
envelope; they do not select a physical template in the absence of
visibility-domain frequency, baseline, and sidereal structure.
The dated reconciliation release records those analytic results at RFIsher
commit `3c806c2e435baccc3195618f4ab1ce55aa5887c2`; its four ledgers share scientific
evaluation commit `1d7de4f0329772a18320d390bbe7eab12c3d9a0c` and RadioFisher commit
`f6bc9ea0972028ce30472dd21b25d4b21b7068c0`. The earlier undated BAO release
remains unchanged as a historical record.

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
