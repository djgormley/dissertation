# Build and figure verification

This document records the checks performed for the full 500-mile Figure 3.2
revision. The unchanged figures retain the source-backed verification recorded
in the preceding bundle; the changed map, Chapter 3 text, and repository export
interface were regenerated and checked again here.

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
