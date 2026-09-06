# Build and figure verification

## Current consolidated release (2026-09-01, v21)

This release scopes the trawl accounting to the August 2026 v3 archive, records
the discovery-layer survey reproduction, removes the datatrawl repository
references ahead of that repository's deletion, and repairs three
cross-references that pointed at a lettered checklist which is not part of the
document. Two sentences in Section 7.4 that implied the v5 reprocessing run had
already consumed the frozen discovery result are corrected to the prospective
voice; the run has not been executed. The ordered-statistic CFAR reference is
now cited where the fine rule is introduced rather than printing uncited, and
the remaining-programme list in Chapter 11 regains its lead-in sentence and
loses a doubled conjunction.

Four further corrections separate statements that had been read as one. The
Table~9.x footer named its no-feasible-$\eta$ rows "excision candidates", which
collided with the science-side excision class counted later in the same chapter;
it is now labelled as the optimizer screen it belongs to, and the science-side
count of six is given with its membership. The two introduction figure captions
claimed the curves came from the Chapter 9 forecast spectrum; the frozen
manifest records both backing tables as recovered artwork bridges that are not
authoritative for the draft, so the captions now say what the curves are. The
$14$--$19\times$ null inflation in Chapter 4 carries the qualifier Chapter 6
already attaches to it: these are raw width ratios on the calibration-era
cohort, not portable constants.

No scientific result changed, and the number gate is unmoved at 96/96.

A page-level visual inspection was run for the first time: every one of the
rendered pages was examined for layout defects that the reference, box, digest
and number gates cannot see. It found two systemic faults, both now fixed.
Table captions sit above the table and the bundle sets no clearance, so the
`\toprule` was drawn through the caption's last line of descenders on fourteen
pages; `\abovetopsep` is now 6pt. The diagram helper placed a box's title and
body centred on fixed fractions of the box height and made no attempt to fit
either to the box, so on Figures 1.1, 8.1, 9.3 and 10.1 the title collided with
the first body line and the body ran out through the box rules into the
connecting arrows. The helper now anchors the two blocks to opposite edges,
re-wraps the body to the box width, and shrinks both together if the wrapped
text still exceeds the box.

The seven schematic diagrams were then redrawn. Each was rendered and examined
as an image, and the pass repeated until an independent check found no text
crossing or escaping a shape, no rule drawn through a word, no connector
reduced to a bare arrowhead, and no type below the 5.6pt floor. The changes are
structural rather than cosmetic: boxes now sit on real grids with gaps wide
enough for a connector to show a shaft; `style.diagram_box` fits its text to the
box, wrapping before it shrinks and shrinking both blocks together when
wrapping is not enough; the decision diamonds fit their labels; and edge labels
are placed off the strokes and node borders they used to sit on. Two TikZ
sources were rewritten on the same principles. Three statements the figures or
captions made but did not deliver are corrected: the Figure 1.1 deck line no
longer promises arrow labels that do not exist, Figure 7.1 now draws the dashed
boundary its caption calls load-bearing, and the Figure 5.1 caption lists the
lower-layer terms the diagram actually shows.

The page count moves from 185 to 186 on the added table clearance. The three
LaTeX passes report no undefined reference, no undefined citation, and no
overfull or underfull box.

```text
compiled output: dissertation.pdf
pages: 186
page size: US letter
file size: 7,380,130 bytes
SHA-256: a17e7de9d922dee0b80f67eab94313dd1b8628beaf5bb16ed0858cfdeb9b3e72
number gate: 96/96 passed at the CI pins; baseline 0
vendored evidence: 924 checks passed
repository tests: 4/4 passed
PDF freshness: 71/71 tracked inputs verified
release manifest: 464/464 tracked bundle files verified
```

CI pins are unchanged at RFIsher `594b15a17ae0841121e8a0acc811163e11dbbb95` and
PilotProxy `36b8232f65c48f3f3808a13e986c31a704692bc7`.

## Consolidated release of 2026-08-26 (v20; superseded by v21)

This release aligns the dissertation with PilotProxy 2.0 development,
RFIsher 3.0, the retired Datatrawl boundary, and the unmerged Kotekan CHORD
feature stage. It corrects the channel-14 frame-origin language, records the
implemented software integration without claiming telescope acceptance,
separates historical survey-v3 products from the forward PilotProxy v5
contract, and preserves every scientific result: the current cross-repository
number gate still passes, 96/96 at the advanced CI pins and 89/89 at the
earlier pair.

The two census tables were imported through the dissertation's verified
portable interface from PilotProxy
`24586f54fdf41e0b77c6ab07aaf55153cd61c778`. They remain byte-identical at
SHA-256 `5ebc30658003233ed4550d18ed188938aeb8ac0278f0316207f3baad7d06b2be`
and `5e7e9aa3f87178ecf3ec4b25e7f04d03ac92545ff2f7eaf699cc9fd7a1037964`;
only the source manifest changed.

The source-reachability claim made in the 2026-08-21 release no longer holds
after PilotProxy's history was re-rooted. Historical producer commits including
`2cf4d8c`, `b533632b`, `639d03ff`, and `62ae33ba` are absent from current
upstream refs. The `bao-noise-tolerance` history was re-rooted separately when
that work moved to RFIsher, so the producer commits it recorded, including
`3b5fc5e1` and `ca6f74a2` behind `evidence/bao_forecast_completion/`, are
absent as well; the RFIsher pins this bundle still cites remain reachable.
Their immutable vendored artifacts remain hash-authenticated and
pass the evidence audit, but source regeneration requires restored archival
refs or an exact source bundle. The Kotekan candidate is therefore cited at its
own commit `097f0bfdaaa0b13370c6d3fad7e5aa47ff60919f` and by its vendor-file
hashes; its presently unresolvable PilotProxy vendor pin is an explicit
re-vendoring gate, not silently replaced provenance.

The fixed-epoch build regenerated all bundle-owned figures and ran three
consecutive `pdflatex` passes, the figure and frozen-data audit, the vendored
evidence audit, the standard-library tests, the current cross-repository number
gate, the PDF freshness check, and the release-manifest verifier. The log has no
overfull box, underfull box, oversized float, undefined citation, or undefined
reference warning.

```text
compiled output: dissertation.pdf
pages: 185
page size: US letter
file size: 7,354,062 bytes
SHA-256: 6d13ceb8b557e0e672e14b95bd3a6dc1ce64c3b8077a0163a9895f7bf9615f49
number gate: 96/96 passed at the CI pins; baseline 0
vendored evidence: 924 checks passed
repository tests: 4/4 passed
PDF freshness: 71/71 tracked inputs verified
release manifest: 464/464 tracked bundle files verified
```

The current integration pair is RFIsher
`5279fbddb6b729f35706147a7f4a24b03311c72e` and PilotProxy
`24586f54fdf41e0b77c6ab07aaf55153cd61c778`; it passes 89/89. CI now runs the
current gate rather than a frozen one: the pair was advanced to RFIsher
`594b15a17ae0841121e8a0acc811163e11dbbb95` and PilotProxy
`36b8232f65c48f3f3808a13e986c31a704692bc7`, which passes 96/96 against this
release. The earlier pair, RFIsher `4f449b8cb2b070820ac0d59900b73f86378d6b39`
and PilotProxy `21ca3da65ade8ff9c20a24c17b315f577461a4f0`, passes 89/89 and
remains the recorded result for the releases below. Both refs are commits, not
branches, so CI stays reproducible and only moves when the pins are advanced.
The seven additional checks recompute the Table 9.1 historical rows, the
flagger comparison table, and the channel 33 eta sweep; the two that need the
archive per-pilot products skip in CI, where those products are absent.

The four tolerance-layer figures retain their authenticated pre-v3 RFIsher
producer pin at `2603788363c187ae37a74226d78f394a716b803d`; the template
comparison remains attached to its immutable dated release at
`3c806c2e435baccc3195618f4ab1ce55aa5887c2`.

## Consolidated release of 2026-08-26 (v19; superseded by v20)

This release records the pre-archive implementation boundary. Schema v5 now
retains receiver configuration identity, the exact residual-score bridge is
implemented, and the stability assessment resamples whole acquisition or
sidereal-day blocks. The text keeps the remaining empirical controls, transfer
measurements, stability margins, and accepted channel products open. It also
records that archive launch awaits CADC certificate renewal and explicit
authorization.

The fixed-epoch build regenerated all bundle-scope figures and ran three
consecutive `pdflatex` passes, the figure and frozen-data audit, the vendored
evidence audit, the standard-library tests, both cross-repository number-gate
checks, the PDF freshness check, and the release-manifest verifier.

```text
compiled output: dissertation.pdf
pages: 185
page size: US letter
file size: 7,348,368 bytes
SHA-256: ffe6aaa943c445f800cfca293040103f49b12a02909b5515a0c963dda151c5ff
number gate: 89/89 passed; baseline 0
vendored evidence: 924 checks passed
repository tests: 4/4 passed
PDF freshness: 71/71 tracked inputs verified
release manifest: 464/464 tracked bundle files verified
```

The immutable CI pair remains RFIsher
`4f449b8cb2b070820ac0d59900b73f86378d6b39` and pilot-proxy
`21ca3da65ade8ff9c20a24c17b315f577461a4f0`. It passes 89/89. The then-current
pushed integration pair, RFIsher
`23d7c9a221255026a41f436aea419f249dccdcea` and pilot-proxy
`12cbf5cce8bac1f7948c7c49eefbf952dcaa6f5d`, also passes 89/89.

The four tolerance-layer figures retain their historical producer pin at
`2603788363c187ae37a74226d78f394a716b803d`; the template comparison remains
attached to its immutable dated release at
`3c806c2e435baccc3195618f4ab1ce55aa5887c2`.

## Consolidated release of 2026-08-26 (v18; superseded by v19)

This release aligns Chapter 9 with the executable prepared-selector contract.
It distinguishes the latest accepted station-state era from a general
stability claim, treats era dates as provenance rather than selector inputs,
and states that the historical floating summaries cannot reproduce exact Q16
decisions. It also records the complete candidate-surface drift screen,
support-ordering behavior, provisional coherence treatment, and the remaining
evidence required before an operational threshold claim. No historical figure
or screening result was relabelled as a calibrated operating point.

The fixed-epoch build regenerated all bundle-scope figures and ran three
consecutive `pdflatex` passes, the figure and frozen-data audit, the vendored
evidence audit, the standard-library tests, both cross-repository number-gate
checks, the PDF freshness check, and the release-manifest verifier.

```text
compiled output: dissertation.pdf
pages: 185
page size: US letter
file size: 7,347,052 bytes
SHA-256: c918ecb66925992c2345d1c9a40a430c48479ccfe37cd7ae1beceb488b74b5e1
number gate: 89/89 passed; baseline 0
vendored evidence: 924 checks passed
repository tests: 4/4 passed
PDF freshness: 71/71 tracked inputs verified
release manifest: 464/464 tracked bundle files verified
```

The immutable CI pair remains RFIsher
`4f449b8cb2b070820ac0d59900b73f86378d6b39` and pilot-proxy
`21ca3da65ade8ff9c20a24c17b315f577461a4f0`. It passes 89/89. A second check
against the current pushed integration pair, RFIsher
`cb1cab291c2f12a5e8972a21a928d73cc565e0d9` and pilot-proxy
`f9ab7d7cfb136808985090b7f6ee3ec0e1e7c317`, also passes 89/89.

The four tolerance-layer figures retain their historical producer pin at
`2603788363c187ae37a74226d78f394a716b803d`; the template comparison remains
attached to its immutable dated release at
`3c806c2e435baccc3195618f4ab1ce55aa5887c2`.

## Consolidated release of 2026-08-26 (v17; superseded by v18)

This release defines the calibrated threshold-selection boundary used in
Chapters 2, 6, 7, 8, and 9. Preparation now owns stable-era selection, frame
validity, correlation, transfer calibration, and complete residual-score
histograms. The selector receives only that histogram family and the science
tolerance, then returns the rank and multiplier under the declared support,
feasibility, cost-plateau, and tie-break rules. Historical screening results
remain labelled as such. The release also retains the estimator-transfer
evidence added immediately before this revision.

The fixed-epoch build regenerated all bundle-scope figures and ran three
consecutive `pdflatex` passes, the figure and frozen-data audit, the vendored
evidence audit, the standard-library tests, the cross-repository number gate,
the PDF freshness check, and the release-manifest verifier.

```text
compiled output: dissertation.pdf
pages: 183
page size: US letter
file size: 7,336,295 bytes
SHA-256: d93f3fe32f08bfc47ad1ea1deaec03f01c3abbc6c51f4e564e6939c9f5b91290
number gate: 89/89 passed; baseline 0
vendored evidence: 924 checks passed
release manifest: 464/464 tracked bundle files verified
```

The number gate was run against the immutable upstream inputs pinned by CI:

```text
RFIsher:     4f449b8cb2b070820ac0d59900b73f86378d6b39
pilot-proxy: 21ca3da65ade8ff9c20a24c17b315f577461a4f0
summary:     data/provenance/dissertation_summary_v3.json
result:      89/89 checks passed; baseline 0
```

The four tolerance-layer figures retain their historical producer pin at
`2603788363c187ae37a74226d78f394a716b803d`; no figure result was relabelled as
an output of the new selector. The template comparison remains attached to its
immutable dated release at `3c806c2e435baccc3195618f4ab1ce55aa5887c2`.

## Consolidated release of 2026-08-25 (superseded by 2026-08-26)

This release aligns the dissertation with the RFIsher 2.0 interface and
terminology while retaining the reconciliation evidence completed in v15. It
updates masking-cost and contamination-residual wording, scenario labels,
current figure provenance, and the pinned number gate. It was rebuilt from the
WSL worktree with the repository's fixed source epoch:
bundle-scope figures regenerated, three consecutive `pdflatex` passes, the
figure/frozen-data audit, the vendored-evidence audit, the standard-library
regression tests, the cross-repository number gate against its pinned upstream
inputs, and the top-level release-manifest verifier.

```text
compiled output: dissertation.pdf
pages: 175
page size: US letter
file size: 7,292,144 bytes
SHA-256: 4e3e546b5607334fcdda15ece5cf7b626e348812559b5ad97492ae502af6e8e5
number gate: 89/89 passed; baseline 0
vendored evidence: 719 checks passed
release manifest: 406/406 tracked bundle files verified
```

The number gate was run against the immutable upstream inputs pinned by CI:

```text
RFIsher:     2603788363c187ae37a74226d78f394a716b803d
pilot-proxy: 21ca3da65ade8ff9c20a24c17b315f577461a4f0
summary:     data/provenance/dissertation_summary_v3.json
result:      89/89 checks passed; baseline 0
```

Vendored figure provenance: four tolerance-layer figures are rendered by
`WVURAIL/RFIsher` `scripts/dissertation/figures.py` at
`2603788363c187ae37a74226d78f394a716b803d`. The template comparison remains
attached to its immutable dated release at
`3c806c2e435baccc3195618f4ab1ce55aa5887c2`. All five PDFs are byte-reproducible
with stable font subset tags. The dated release records clean scientific
evaluation commit
`1d7de4f0329772a18320d390bbe7eab12c3d9a0c` and RadioFisher commit
`f6bc9ea0972028ce30472dd21b25d4b21b7068c0`; the earlier undated release is
retained unchanged.

## Consolidated release of 2026-08-24 (superseded by 2026-08-25)

The v14 release reconciled the refusal booking and floor discipline, corrected
the channel-35 boundary, rebuilt the Fisher banks from clean published trees,
and refreshed the Chapter 8 and 9 tables and prose.

```text
compiled output: dissertation.pdf
pages: 174
page size: US letter
file size: 7,288,774 bytes
SHA-256: 8105bbe748ae8ce351a89aad6281fc8d654d64281e96967f463acc20642ac3f5
number gate: 69/69 passed; baseline 0
vendored evidence: 676 checks passed
release manifest: 392/392 tracked bundle files verified
```

Its CI inputs were RFIsher
`70be39cb73bd576da7d17f40a671b6c12e22a147` and pilot-proxy
`21ca3da65ade8ff9c20a24c17b315f577461a4f0`.

## Consolidated release of 2026-08-21 (superseded; source reachability corrected in v20)

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
file size: 7,296,574 bytes
SHA-256: c65076f07f548ec30681d6fc6d9b9705964d9392c33eb67f55c87820f179adb9
number gate: 67/67 passed; baseline 0
vendored evidence: 676 checks passed
release manifest: 390/390 tracked bundle files verified
```

The final pass reports no undefined reference or citation and no overfull or
underfull box. The 17 bundle-scope vector PDFs regenerate byte-identically
under `SOURCE_DATE_EPOCH`, so the audited hashes are reproducible from source.

The number gate was run against the immutable upstream inputs pinned by CI:

```text
bao-noise-tolerance: ca6f74a24c10c2db24bd4bcd35f486aecd23bd0d
pilot-proxy:         c76a4a8305e6dc67630ed88575a4772725b54d7f
summary:             data/provenance/dissertation_summary_v3.json
result:              67/67 checks passed; baseline 0
```

At the time of this release, both pins were the tip of their upstream `master`
and were reachable from the default branch. They were advanced from `99a48ef1`
and `62ae33ba` once those upstream branches settled, and the gate was re-run
against every intermediate combination; all of them passed 67/67. PilotProxy's
history was subsequently re-rooted, and the `bao-noise-tolerance` history was
re-rooted separately when that work moved to RFIsher, so the claim that these
objects remain reachable or cannot be lost is no longer true; the v20 audit
above supersedes that source-reachability status.

Advancing the `bao-noise-tolerance` pin changes what CI reads but not how it
reads it: `scripts/check_dissertation_numbers.py` is byte-identical between the
two commits, and the newer tree simply adds the forecast-completion release
artifacts under `out/`. It also aligns the checkout with `ca6f74a2`, the commit
this bundle now vendors its template-tolerances assets from. Advancing the
`pilot-proxy` pin is a no-op for the gate itself, since
`data/provenance/dissertation_summary_v3.json` is byte-identical between
`62ae33ba` and `c76a4a83`; it is moved so both pins track the same default
branches that the provenance table below resolves against.

At the time of the 2026-08-21 release, every upstream commit cited as figure
provenance in `figure_src/figure_manifest.csv` resolved from its upstream
`master`:

```text
bao-noise-tolerance@d56d3251  on master
bao-noise-tolerance@99a48ef1  on master
bao-noise-tolerance@db89d626  on master (merged before the consolidated release)
pilot-proxy@b533632b          on master
pilot-proxy@639d03ff          on master
pilot-proxy@2cf4d8cd          on master (merged as pull request #5)
```

`pilot-proxy@2cf4d8cd` is the commit behind `evidence/canfar_archive_health_v1/`.
Its branch had been closed unmerged and deleted during an unrelated cleanup,
which left the citation resolvable only through the pull request head. The pull
request was reopened and merged with a merge commit, preserving the cited SHA
rather than rewriting it, so at that release the archive-health evidence was
attributed to work on the upstream default branch. The later repository re-root
removed that reachability from current refs without changing the immutable
vendored evidence.

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

## Re-vendored template-tolerances figure (2026-08-21)

`bao-noise-tolerance@ca6f74a2` made the embedded-font subset tags of the
forecast template assets deterministic, superseding the `db89d626` rendering
that this bundle had vendored. The three changed release artifacts
(`forecast_completion_channel_tolerances.pdf`, its `.png`, and the release
manifest recording them) were re-vendored from that commit; the remaining nine
BAO artifacts are byte-identical, so the scientific content is unchanged and
only the font-subsetting differs. The figure shrank from 768,723 to 204,178
bytes.

The re-vendored PDF subsets its fonts, so `pdffonts` reports them as
`ABCDEF+LMRoman9-Regular`. The bundle's font contract compared that raw string
against the Latin Modern family and rejected it. The audit now strips the
six-letter subset tag before applying the family contract and before recording
the font name, matching the equivalent upstream fix in
`bao-noise-tolerance@3fb123b`. No other audited artifact carries a subset tag,
so the only report rows that changed are this figure and the re-attribution
below.

`figs/fig_bao_the_case.pdf` was attributed to `bao-noise-tolerance@d56d3251`.
That commit predates `485bd4f`, which revised the channel-33 policy case to a
single acquisitions>=8 population, and the checked-in figure plots the revised
values (keep-everything at 1,566x over and 3.4x time, pilot proxy at 3.4x time)
rather than the superseded ones. The cited commit therefore could not have
produced the vendored bytes. The attribution is corrected to
`bao-noise-tolerance@a7ee77ee`, the first pinned commit on the upstream default
branch whose inputs match the plotted values. `fig_bao_convergence.pdf` and
`fig_bao_two_walls.pdf` keep their `d56d3251` attribution: their input tables
are unchanged across that range, so the earlier commit remains the precise one.

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
