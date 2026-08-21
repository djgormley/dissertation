# Build and figure verification

## Current consolidated release (2026-08-21)

This release consolidates three lines of work onto one branch: the suite-audit
release boundary, the completed-archive correctness revision, and the vendored
archive-health and forecast-completion evidence releases. It was rebuilt from
the WSL worktree with the repository's fixed source epoch: the bundle-scope
figures were regenerated, followed by three consecutive `pdflatex` passes, the
figure/frozen-data audit, the vendored-evidence audit, four standard-library
regression tests, the cross-repository number gate against its pinned upstream
inputs, and the top-level release-manifest verifier.

```text
compiled output: dissertation.pdf
pages: 171
page size: US letter
file size: 7,324,608 bytes
SHA-256: 4c8bfde12530de932cbbd6a3e64be71dfcbe5000c7a05f45a73c27ed54ec2e82
number gate: 67/67 passed; baseline 0
vendored evidence: 676 checks passed
release manifest: 390/390 tracked bundle files verified
```

The final pass reports no undefined reference or citation and no overfull or
underfull box. The 17 bundle-scope vector PDFs regenerate byte-identically
under `SOURCE_DATE_EPOCH`, so the audited hashes are reproducible from source.

The number gate was run against the immutable upstream inputs pinned by CI:

```text
bao-noise-tolerance: 99a48ef1a0173c05bc1e3799a3b0fca26a2338f6
pilot-proxy:         62ae33ba9e1b303ea7432730f2c09fb59787946c
summary:             data/provenance/dissertation_summary_v3.json
result:              67/67 checks passed; baseline 0
```

Both candidate pin sets were tested against the merged text and both pass
67/67. The pinned pair above was chosen because each commit is reachable from
its upstream `master`, so neither can be lost to a deleted or rebased feature
branch. The newer `bao-noise-tolerance@db89d626` and `pilot-proxy@2cf4d8cd`
still appear as figure provenance in `figure_src/figure_manifest.csv`; those
commits are not yet on their upstream default branches.

The vendored-evidence audit passes 676 checks across 12 BAO artifacts, four
CANFAR core files, ten dissertation data products, three archive result PDFs,
92 diagnostic figures, 27 active figure copies, and 182 ledger rows.

The figure audit reports **PASS** for every manifest artifact, the active
external vector PDFs and named TikZ figures, the frozen CSV tables, and the
embedded Latin Modern font contract. Figure 3.2 was regenerated from 499
inclusive census rows (36 within 120 miles), aggregated at 162 distinct source
range--bearing sites; the frozen data preserve 421 reported-on-air/unverified,
67 reported-on-air/licence-matched, and 11 licence-only candidate records. Its
one-page vector output has SHA-256
`7a6e0e37d5c7e06edaf98e8faf0e803e8ea6c1b9c9416da53ccb35bdb8671959`.

Page-level visual inspection was not repeated for this consolidation build. The
contact-sheet reviews recorded in the chronology below cover the constituent
revisions, and the merge introduces no new figure or table artwork beyond the
Appendix C diagnostic atlases, which are generated and hash-verified.

## Historical verification chronology

> The records below describe earlier dissertation bundles and are retained as
> a build chronology. Their page counts, hashes, and census counts are
> superseded by the current release record above.

The first record below documents the earlier full 500-mile Figure 3.2 revision.
The unchanged figures retained the source-backed verification recorded in its
preceding bundle; the changed map, Chapter 3 text, and repository export
interface were regenerated and checked again for that historical release.

### Completed-archive correctness build (2026-08-20)

The completed-archive integration was built from the WSL worktree with the
repository's fixed source epoch.  All source-backed figures were regenerated
using the declared figure requirements, followed by three consecutive
`pdflatex` passes and a fresh figure/frozen-data audit.

```text
compiled output: dissertation.pdf
pages: 135
page size: US letter
SHA-256: aed86d25f1e468ef9d6a2109af488c30d482ad37f9e6b0a8211c7bb236327ead
```

The final pass contains no unresolved references or citations, no warning
patterns, and no overfull, underfull, or oversized-float diagnostics.  All
fonts are embedded; the PDF is searchable and reports PDF 1.5.  The figure
audit reports **PASS** for 28 manifest artifacts, 25 active external vector
PDFs, two active TikZ figures, one generated unused figure, and four frozen
CSV tables (two still explicitly marked for authoritative replacement).
All 135 pages were rendered as whole-document contact sheets; the revised
abstract, research-question map, survey health gate, BAO footprint, lower-band
completion, conclusion, status matrix, and closing-program pages were also
inspected individually at higher resolution.  No clipping, collision, missing
glyph, malformed table, unintended blank page, or misplaced float was found.

The dissertation number gate was run against immutable upstream inputs:

```text
bao-noise-tolerance: a7ee77eec63604ccf2560410887f5a86bae168d6
pilot-proxy:        1d74e096855c4c9bef92c32a82723a3f50a2210b
summary:            data/provenance/dissertation_summary_v3.json
result:             67/67 checks passed; baseline 0
```

JSON parsing, frozen-data hash/row verification, Python bytecode compilation,
CSV structure, `git diff --check`, and the comprehensive tracked-file manifest
verification were also run on the final tree.  Generated LaTeX auxiliaries
were removed after validation; the regenerated dissertation and changed
footprint PDF are retained.

### Full 500-mile Figure 3.2 revision

The records below document the earlier full 500-mile Figure 3.2 revision.
The unchanged figures retained the source-backed verification recorded in
its preceding bundle; the changed map, Chapter 3 text, and repository export
interface were regenerated and checked again for that historical release.

## Dissertation build

The updated map was generated directly from its bundled Python source and
frozen census tables. The dissertation was then compiled with three consecutive
`pdflatex` passes under the fixed build epoch, followed by the complete figure
and frozen-data audit.

```text
compiled output: dissertation.pdf
pages: 117
SHA-256: 353b63b1e7754707197403fee1ddc492b571758489ede077048e651b658f829f
```

The final LaTeX log contains no unresolved references or citations, no overfull
or underfull boxes, and no final-pass warning patterns. The PDF is searchable,
unencumbered, US-letter sized, and uses embedded fonts.

The text reflow caused by the revised Chapter 3 discussion and larger figure was
confined to the surrounding five-page window. PDF pages 34--38 were rendered
and inspected individually. The table, map, caption, surrounding prose, and
following section show no clipping, collision, missing glyph, black box, or
unintended empty page.

## Figure 3.2 checks

- generator: `figure_src/broadcast_figures.py::fig_census_map`;
- full data table: `census_full_500mi.csv`, 490 rows;
- inner-detail table: `census_inner_120mi.csv`, 39 rows;
- aggregation: 151 distinct source range--bearing sites;
- output: one-page vector PDF with no embedded raster-image objects;
- output SHA-256: `defe2228b987b5e310de42a963612ca698dda0f90d519f46d5789cff39f55457`;
- typography: embedded Latin Modern only, with no Type 3 or DejaVu substitution;
- projection: DRAO-centred azimuthal equidistant; source range and bearing are
  plotted directly, while cartographic boundaries are contextual only.

The standalone figure and its dissertation page were both rendered and
inspected at full-page resolution. Two consecutive source regenerations
also produced the same figure SHA-256 shown above.

## Figure and frozen-data audit

The generated audit reports **PASS** with:

- 27 manifest artifacts;
- 24 active external vector PDFs;
- two active named TikZ figures;
- one generated but unused source-backed PDF;
- 12 frozen CSV tables, all matching their recorded SHA-256 and row count;
- five current tables represented by the PilotProxy version-1 export boundary;
- seven bridge tables still marked for authoritative replacement;
- common `0.98\linewidth` inclusion width; and
- matching Python/TikZ palette and Latin Modern font contracts.

## PilotProxy follow-up patch

The original export-boundary patch has been applied and pushed by the author. A
small follow-up patch was prepared against repository commit
`5a698c0fd07d7250913aa282c14f5db448c8cc21` so future repository exports also
contain the complete 500-mile census. It changes the exporter, its focused test,
and its documentation.

```text
focused tests: 4 passed
patch SHA-256: 495cc5588c8da1926eeb3cb966a1bbbb9374351154c5715e3f45214cef193034
```

The patch was applied to an isolated baseline tree, checked with `git diff
--check`, and exercised with `tests/core/test_dissertation_exports.py`. No
repository branch, commit, push, or pull request was created in this session.

## Remaining provenance limitation

Seven active outputs still use editable CSV tables recovered from vector paths
in the supplied earlier draft because the authoritative analysis arrays were not
present in the dissertation archive. The reference PDFs, extraction script,
hashes, and per-table provenance are retained. These remain reproducible artwork
bridges, not substitutes for scientific regeneration, and remain marked
`replacement_required` until direct PilotProxy, survey, cosmology, or Fisher
exports replace them.

## Integrated legacy-evidence release (supersedes the earlier build record)

The 2026-08-13 release integrates the curated legacy evidence into the canonical
dissertation source, adds Appendix B, and replaces the sidecar archive layout
with `evidence/`. The final document was compiled with two stable `pdflatex`
passes after the last source edit.

```text
compiled output: dissertation.pdf
pages: 123
page size: US letter
SHA-256: 97fe67c8a682bc94e3b95324d8942527ab546fc4b5b40a5f2ccbd7fc8220a5fa
```

The final log contains no warning, overfull-box, or underfull-box patterns. The
complete figure and frozen-data audit reports PASS. All 123 pages were reviewed
as contact sheets; the newly integrated Chapter 6, Chapter 8, Chapter 10,
Chapter 11, and Appendix B pages were then inspected individually at higher
resolution. No clipping, collision, missing glyph, malformed table, unintended
blank page, or misplaced legacy-evidence float remains.

## v2 data-export import build (2026-08-18)

The PilotProxy v2 dissertation export (snapshot `dissertation-draft-2026-08-18`,
producing commit `2fd683e4`) was imported through
`figure_src.import_dissertation_export` with schema, hash, and row-count
verification, all 26 figures were regenerated from source, and the document was
compiled with three consecutive `pdflatex` passes under the fixed build epoch.

```text
compiled output: dissertation.pdf
pages: 126
page size: US letter
SHA-256: 6ac18981316ce4bd500c14a042cea5eb72c952b0dc1cf81b1549c1dd6d97503e
```

The final log contains no warning, overfull-box, underfull-box, or float
patterns. The figure and frozen-data audit reports **PASS** with:

- 28 manifest artifacts;
- 25 active external vector PDFs (adding `fig_census_psd_lower.pdf`,
  SHA-256 `5b43cd44b2b8919cfa9f7e3e85b97474f9748408c04f3a163f090cf492fa4378`);
- two active named TikZ figures;
- one generated but unused source-backed PDF;
- 12 frozen CSV tables, all matching their recorded SHA-256 and row count;
- seven tables represented by the PilotProxy v2 export boundary
  (`census_psd.csv` and `bao_time_vs_masking.csv` newly direct);
- five bridge tables still marked for authoritative replacement; and
- common `0.98\linewidth` inclusion width with matching palette and font
  contracts.

The regenerated census-spectra figures, the new lower-band companion, the
status matrix, the observing-time figure, and their dissertation pages were
rendered and inspected individually. The earlier "Remaining provenance
limitation" section is superseded: five (not seven) active outputs still read
recovered bridge tables, and `FIGURE_SOURCES.md` carries the current list.

## WVU brand-palette build (2026-08-18)

Cosmetic rebuild after switching the semantic palette to the WVU
visual-identity colors (see `REVISION_NOTES.md`). All 26 figures regenerated,
three `pdflatex` passes under the fixed epoch, audit **PASS** with the updated
palette contract, 126 pages, no warning/overfull/float patterns. The status
matrix, policy case, two-walls, claim chain, and a TikZ-derived page were
rendered and inspected for color separation and small-text legibility.

```text
compiled output: dissertation.pdf
pages: 126
SHA-256: c2ad62a5ff6a10d2e8f66719fb6d0cb45b4f5742d3c6934f7ecc7177228d9fe6
```
