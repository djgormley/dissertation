# Revision notes

## 2026-08-20 — completed-archive integration and correctness cleanup (v13)

The attached CANFAR bundle was independently inventoried before its results
were promoted in the dissertation.  All 23 allocation products load and pass
their declared structural and exact-arithmetic checks.  The denominator ladder
is 16,327 enumerated events, 6,140 recorded-outrigger exclusions, 10,187 survey
targets, 10,184 completed dispositions, and three events in the pending-attempt
category after two recorded attempts.  Of the completed events, 9,214 are
represented in the inventory and 8,983 contribute originally valid frames.
The 23 per-channel products contain
750,461 frames (750,457 denominator-valid and four explicit all-zero invalid
frames) plus three quarantined raw objects.  The audit also found 178
denominator-valid rows in eight events whose mean decoded complex-int4 power is
exactly 128, the representation ceiling.  The v1 health gate now excludes
those provably constant native-`0x00` rows and the four detector-invalid rows,
leaving 750,279 science frames from 8,980 events.  Their immutable identifiers
and reason-coded disposition are recorded in
`CANFAR_PRODUCT_HEALTH_AUDIT.json`; because the constant input has a DC-only
spectrum, the before/after aggregate spectra are repaired exactly and checked
against the health-included frame-power sums.

- Chapters 1, 2, 3, 7, 8, 9, and 11 now describe the completed all-23 archive
  consistently, distinguish archive-average spectral peaks from per-epoch
  anchors, and separate historical ten-channel evidence from the current
  screening result.  Chapter 1 adds five explicit research questions and an
  evidence map.
- The obsolete $f_s/2$ quarterly cost record is retained only as historical
  provenance; the all-23 current/latest-observed calculation governs the
  current Chapter 9 cost claims.  Channel 30 is explicitly latest-observed,
  not measured after collection ended in September 2023.
- Mathematical corrections include the coarse integer cross-product's removed
  factor of two, the conditional assumptions behind the central/noncentral
  $F$ models, a bounded-influence statement for the order statistic, the
  zero-dB reference-count asymptote, the Fisher-bias block inverse and sign
  convention, and the distinction between RMSE and statistical uncertainty.
  The norm ratio $\mu_0$ is now consistently a static, exact rational scale
  under the declared white/isotropic null model, not an empirically calibrated
  finite-sample mean.
- The $K=128$ window claim is limited to configured in-span targets.  The
  stronger out-of-span channel-33 carrier is now a configuration sentinel,
  requiring an alternate target/weight bank or an unsupported-channel status.
  Pilot-to-shelf contrast is quoted only in a declared finite bandwidth.
- The operational footprint now distinguishes the continuous 353.28-channel
  bandwidth ratio from the inclusive 354-bin `freq_id=492--845` handover.
  The corresponding vector figure was regenerated.
- The archive checklist now makes the current-geometry paired synthetic study
  mandatory.  It separates ideal-to-float model mismatch from input,
  coefficient, transform, and decision-arithmetic losses and requires
  fixed-$P_{\rm fa}$ detection curves, paired uncertainty, offset sweeps,
  clipping/overflow accounting, and full-pipeline bit checks.
- CI now pins the immutable archive-health and forecast-completion producer
  commits.  It retains the 67-check historical-number gate against
  `dissertation_summary_v3.json`, and adds a repository-local verifier for the
  12 forecast artifacts, four archive-health core products, 92 diagnostic
  figures, 182 exclusion-ledger rows, and their principal reconciliation
  invariants.  The older v2 snapshot is intentionally historical and contains
  the superseded channel-33 population comparison.
- The release manifest now covers every tracked repository path plus the new
  product-health audit (excluding only the manifest itself), so source,
  workflow, frozen-data, figure, and compiled-PDF changes are checked together.

## 2026-08-19 — worked-example bridge retired (v12)

The two worked-example frames were never lost: ch05's own prose identifies
them as channel-506 (freq_id 506, DTV 36) frames, and both were located in
the archive product and verified against the published values before their
recovered-artwork table was replaced with the direct per-frame export:

- panel (a), exemplar masked frame 2025-07-31: frame 2606, event 1126624080 —
  T[60..64] = (1.066, 8.730, 18.615, 7.598, 1.083) reproduced
  digit-for-digit, F/mu0 = 1.258;
- panel (b), weakest valid frame 2025-05-16: frame 1226, event 1116626388 —
  designated-window maximum T[62] = 2.585 -> 2.59 as published,
  F/mu0 = 0.897 (the published bulk medians are usable-bulk statistics, a
  subset of the 256 bins, and are consistent).

`worked_example_spectra.csv` is now a direct export (512 rows, both panels'
full fine spectra); the frozen manifest, figure manifest, README, and
FIGURE_SOURCES updated. Three of the original seven bridges remain
(both intro-wiggle curves counted as two, plus convergence and two-walls),
all with agreed regeneration or retirement paths.

## 2026-08-18 — the lower band through the residual chain (v11)

Source of facts: the released chain-table generator
(`tools/make_chain_table.py` in PilotProxy, commit 278646a), whose self-test
reproduces Table 9.6's published first-block constants from the raw products
to the printed digit (ch33: floor −44.95 dB from 1,388 nulls, 24×; ch29
6,617×; ch32 43.5×; ch34 1,603×; ch35's full-archive row including its
45-minute τ_c; shares, filters, masked fractions, null census). The author
could no longer trace Table 9.6's original analysis; the reproduction now
*is* its provenance, and the lower-band extension runs on the validated
basis ("when in doubt, rebuild").

- New Table 9.x (tab:bao:lowerchain): channels 16–26 through the identical
  chain — deployed-rule basis, component budget, τ measured-or-cap, binding
  r_tol = 1.5e-3 — with the sign-off channels (19, 20, 26) evaluated on
  their transmitter-off eras (conservative all-frame p90 floors, so their r
  values are bounds even where τ is measured), and channel 17's 20-frame
  floor parenthesized per the ch28 convention.
- Historical v11 headline: every one of the eleven legacy screening labels was
  carried through the then-current chain. The later health-filtered v4 release
  retains those classifications only provisionally rather than claiming a new
  blinded verdict. Channel 21 emerges as the survey's best-constrained
  full-archive coherence
  hostage (14,647 detection-defined null frames, the largest population not
  constructed from a transmitter-off epoch; −43.2 dB
  floor; ≤22,100× at the cap) and joins channel 29 at the head of the
  cadence priority (ch11 near program and checklist item C updated).
  Channel 23 is the inverse case (τ ≤ 5 min bounded, floor unmeasured; its
  unlock is the fine-stage null re-decision). Channel 20's off-era row is
  the cheapest refinement: health-filtered τ is measured at 165 min, only the floor
  basis conservative.
- The era-mixture trap demonstrated on data, reported as a demonstration and
  not a verdict: evaluated era-blind, channels 19 and 26 land near 4× and
  formally pass the dilation tier because the sign-off step masquerades as
  filterable DC/inter-day power, and ch19's era-straddling record returns a
  spurious "measured" τ of 19 minutes.
- The lowerband section's "deliberately does not extend Table 9.6" framing
  replaced by the generator-validated extension; ch11's synthesis and near
  program updated to match. No published first-block digit changed.
- Figure audit (author's direction: question all figures, data and
  conception): the ch01 band figure's caption claimed a ten-channel marking
  the artwork never drew — the figure now actually marks the coverage
  (channels 16–36 with products and chain; 14–15 hatched, queued) and the
  caption states it. All architecture schematics, both TikZ diagrams, and
  every export-fed figure verified current. Remaining bridges unchanged
  (intro wiggles, worked example, convergence, two-walls), with two audit
  recommendations recorded: regenerate two-walls from the current sweeps
  (retiring its bridge on the gate-validated basis), and when the Pres-bank
  work happens, produce the convergence figure under the current
  fixed-target tolerance convention rather than reproducing the legacy
  noise-normalized family.

## 2026-08-18 — working-threshold limits, per-channel disposition, generalization (v10)

Three additions at the end of ch09, all from the completed-archive analysis
(per the author's direction to fold the operational results in and state the
threshold's limitations explicitly):

- \emph{The working threshold: development and limits} — the four-step
  threshold ladder (idealized F>1; calibrated exact per-channel null F>mu0,
  values 0.98533–1.01111, step-1→2 shifts of tens of percentage points on
  quiet channels; tolerance-priced eta=1.4 with the +1.46 dB kept-excess cap;
  pending per-channel rho-hat thresholds) and six stated limitations:
  cost-axis-only selection, band-wide non-optimality with bracket-degenerate
  per-channel optima, the occupancy gate and channel 36's exception,
  in-sample tuning pending the blocked holdout, coarse-rule-only, and
  epoch-scoped validity.
- \emph{The per-channel disposition} — the 354-channel CHIME handover
  (273 keep / 81 discard), presented as a policy recommendation at screening
  level layered on unchanged evidence: discard table, six pilot monitoring
  taps, the both-excised edge rule, channel 36's flagged keep-and-mask
  (+0.55% at the cap), the inclusive-posture asymmetry argument (masks are
  software; excision irreversible, applied only where recoverable is 0–2%),
  and the 8-VSB skirt geometry of the ten kept edges (nine skirt-only; the
  22/23 edge freq_id 707 flagged at 57 kHz of shelf overlap; nominal-rolloff
  caveat with the edge-scan as the measurement). This supersedes v9's note
  that the operational override lived only in the policy brief — it now
  appears here, explicitly labeled as policy on top of evidence.
- \emph{Beyond this survey's observable} — the tolerance machinery stated as
  an interference-tolerance framework with a pluggable Fisher backend; the
  BAO bank is the demonstrated instantiation, and the science-specific
  content enters only through the forecast. (No software rename is asserted;
  naming is pending.)

## 2026-08-18 — channel 16 completion and campaign specification (v9)

Source of facts: the completed channel-16 product (freq_id 813, finished
2026-08-18: 9,045 events, 36,385 frames, archive masked fraction 91.6%,
current-epoch 6.6% at the working threshold; its dominant carrier lands
exactly at synthesis) and the regenerated report/policy analysis on the
complete 21-product set.

- Inventory (ch07): 9,192 events probed / 8,962 usable, 153,239 units,
  681,211 frames, per-channel event range 1,543–9,045; "channel 16 still
  processing" removed; channels 14–15 stated as queued in the scan (their
  freq_ids are in the inventory).
- ch09 lower band: channel 16's row updated to its final values and the
  partial-product markers removed from the table, caption, and section text;
  survey-rule survival across the fourteen no-live-carrier channels corrected
  to 12.9% → 93.8% on the complete data; channel 36's 33.7% at the working
  threshold stated explicitly as the burst-type exception rather than left
  inside the no-live-carrier range.
- Campaign honesty (per the author): the ch29 contiguous scan is now
  "specified first," not "scheduled first," and both ch09 and the ch11 near
  program state the fallback posture if the campaigns are never executed:
  the sidereal-day caps stand as permanent conservative bounds and
  certification shifts to the blocked holdout and per-channel jackknife.
  The concrete acquisition specification (channels, sessions, durations,
  cadences, volumes) is recorded in checklist item C.
- Frozen data: v2 export regenerated from the complete products and
  re-imported (census_psd.csv now carries channel 16's final spectrum; the
  channel-status note no longer says partial); fig_census_psd_lower's
  "(partial)" label removed.
- Not changed: evidence statuses (channel 36 remains an excision candidate on
  the chain screen; the operational keep-and-mask override lives in the
  policy brief, not in this document's evidence claims).

## 2026-08-18 — WVU brand palette

Cosmetic only; no data, prose, or layout change. The five semantic role colors
(measured / model / conditional / failure / pending) are now drawn from the
WVU visual-identity color system: safety blue `#0062A3`, old gold `#7F6310`,
hemlock `#6A724F`, woodburn `#8D4638`, seneca gray `#988E8B`. The two
additional series colors are WVU sunset `#F58672` and WVU gold `#EEAA00`;
the flagship gold is reserved for lines and fills because its contrast on
white (~2:1) is too low for the figures' small colored text, so the
model/transfer role uses the darker old gold. Light fills are pale tints of
the new role colors. Updated in lockstep (the audit enforces agreement):
`figure_src/style.py`, the `ppXxx` definitions in `dissertation.tex` (TikZ
derives its tints from these), `figure_src/audit_figures.py`, and the palette
table in `FIGURE_SOURCES.md`. All 26 figures regenerated; audit PASS;
126 pages, no warnings.

## 2026-08-18 — v2 data-export import and figure regeneration

Source of facts: the PilotProxy v2 dissertation export (snapshot
`dissertation-draft-2026-08-18`, producing commit `2fd683e4`), generated from
the same 21-product trawl snapshot as the survey-completion update below plus
the released bao-noise-tolerance forecast bank. This supersedes the statement
below that figure data was not re-imported.

- Frozen data: imported the v2 export through
  `figure_src.import_dissertation_export` (schema, hashes, and row counts
  verified). Seven of the twelve tables are now export-represented; two of
  them are newly authoritative: `census_psd.csv` (26,439 rows, all 21 measured
  channels, direct from the products' stored integrated spectra) and
  `bao_time_vs_masking.csv` (63 rows, computed from the released forecast
  code). `channel_status.csv` now carries all 21 measured channels with the
  lower-band statuses and the epoch splits on 19/20/26/27/35;
  `epoch_operating_points.csv` gains the four sign-off channels' epoch pairs.
  Five tables remain explicit bridges (both intro-wiggle curves,
  `worked_example_spectra`, `bao_convergence`, `bao_two_walls`).
- Census-spectra figures: `fig_census_psd` regenerated from the direct export;
  panels are now centred on the synthesized pilot (transmitted-frequency
  sense) rather than re-centred on the dominant emitter, and the ch03 caption
  was rewritten against the data: channel 33's dominant carrier at
  -3.6 kHz in the skipped guard (the Appendix B blind spot, now visible in the
  main text's own figure), channel 28's strongest in-window feature at
  -12.6 kHz, sideband structure noted on 27/30-32. New companion figure
  `fig_census_psd_lower` (channels 16-26, channel 16 marked partial) added to
  the ch09 lower-band section with a data-verified caption; every lower-band
  dominant carrier sits inside the fine span within 0.6 kHz of synthesis.
- Status matrix: auto-label now reports 21 channels with archive products;
  per-cell "epoch split" callouts replaced by half-filled cells plus one
  explanatory line (five split channels would have collided); ch11 caption
  updated to describe the 21-channel export and the sign-off splits.
- Observing-time figure: curve values now computed, not artwork-recovered;
  the 50%-masked annotation anchor derives from the data.
- ch08 epoch-figure caption notes the export's additional epoch pairs.
- Bookkeeping: figure manifest provenance rows updated; README and
  FIGURE_SOURCES counts corrected (26 generated / 25 active PDFs; 7
  export-represented / 5 bridge tables); generate_all inventory extended;
  audit PASS (fonts, vector-only, manifest/TeX/frozen-data consistency);
  126 pages, no warnings.
- Not changed: worked-example, convergence, and two-walls figures still read
  bridge tables; their replacement requires the named frames and the
  bias-bank conventions, recorded as pending in the export manifest.

## 2026-08-18 — August 2026 survey-completion update

Source of facts: the 2026-08-17 `_per_pilot` trawl snapshot (21 products,
single kernel cohort), the monthly occupancy/era analysis and exact
rethresholding computed from those products, and the released forecast bank.
Scientific data for figures was NOT re-imported: all figures still reflect the
frozen ten-channel export, and captions in ch01/ch11 now say so explicitly.
No residual-chain or tolerance verdicts were added for the new block; the new
section reports survey- and epoch-level quantities only.

- ch07: inventory updated to the near-final snapshot (21 of 23 allocations,
  9,184 events probed / 8,953 usable, 146,599 units, 654,810 frames, two
  quarantined units, per-channel event range 1,543–8,959); added the measured
  endogenous-selection instance (collection curtailed on the most contaminated
  channels; channel-30 captures cease after September 2023).
- ch09: coverage statement updated (scope section); new section
  `sec:bao:lowerband` with the eleven lower-band allocations at survey/epoch
  level (survey-rule masked fractions, dated transitions — ch19 sign-off
  Dec 2024, ch26 sign-off Apr 2023, ch20 step-down Sep 2022 — correlation-time
  outcomes 62/167/5 min on ch24/20/23, transmitter-off floors −33.5/−26.1/−32.3
  dB on ch19/20/26 and −24.4/−31.5/−26.2 dB on ch27/32/35-early, current-epoch
  rethresholding at F > 1.4 μ0 with survival 13.2%→93.8% across the fourteen
  no-live-carrier channels, and screening costs ×1.08 survey / ×1.59 worst bin
  versus ×1.20 / ×5.4 at the survey rule, labeled cost-axis screening only);
  era section gains ch27's bounded sign-off, the ch32 sharpening, and the ch30
  collection boundary; verdicts coverage limit updated to point at the
  confirmation.
- ch08: anchor summary extended to the lower band (−0.70 to +1.26 kHz) and
  ch17's two-epoch anchor motion added alongside ch32/35.
- ch01: band-figure caption and chapter-arc sentence updated (figure artwork
  unchanged, labeled as the ten-channel export).
- ch11: status-matrix figure caption qualified; the "remaining thirteen"
  paragraph replaced with the measured outcome; matrix rows 27 and 30 amended
  (era-split with measured off-epoch floor; collection-curtailed/unmonitored);
  future-work item 1 narrowed to ch14–15 + ch16 completion + lower-band
  chain rows; new future-work item: periodic spot-collection on
  collection-excluded channels.
- appA: status-map row updated to 21-of-23 coverage.
- archive_completion_checklist.md: status header and item B annotation.

## 2026-08-12

## Deliverable summary

- 118-page compiled dissertation
- 11 substantive chapters plus an evidence/closing-test appendix
- 26 figure environments and 24 included graphics
- 8 new explanatory figures generated from a reproducible Python script
- 14 tables
- Three-pass LaTeX build with no unresolved references, citations, overfull
  boxes, or LaTeX/package warnings

## Major substantive revisions

### Front matter and document architecture

- Rebuilt the title and abstract pages around the WVU ETD structure.
- Suppressed numbering on the title and abstract pages, used Roman front-matter
  numbering, and restarted Arabic numbering at Chapter 1.
- Rewrote the abstract as problem, engineering solution, and scientific verdict.
- Added a List of Acronyms and Abbreviations.
- Completed the former scaffold chapters for survey evidence, calibration,
  real-time integration, and conclusions.
- Added Appendix A, an evidence matrix that distinguishes specified, analytic,
  verified, measured, modelled, conditional, and pending claims.

### Standards and scientific framing

- Retained the exact ATSC symbol-rate and pilot-frequency relations while
  separating them from the standard's nominal RRC roll-off value.
- Removed the false claim that one exact integer identity simultaneously proves
  exact 6-MHz allocation fill and exact placement at the transition midpoint.
- Distinguished the continuously present pilot from the standard's other
  deterministic synchronization structures.
- Narrowed the pilot's role from a universal detector-optimality claim to a
  matched-filter benchmark under a declared known-tone Gaussian model.
- Softened overly broad statements about recombination, galaxy surveys, and
  information lost or retained by intensity mapping.

### Statistical detector model

- Displayed the null and signal hypotheses explicitly.
- Defined the complex-normal variance convention and the factor of two in the
  noncentrality parameter.
- Marked feed independence, local smoothness, and Gaussianity as model
  assumptions rather than instrument facts.
- Clarified that symmetric references cancel odd Taylor terms only for a common,
  locally smooth, symmetrically sampled response; even-order curvature and
  narrow/asymmetric features remain.
- Added a visual boundary between analytic detector theory, empirical
  calibration, and holdout validation.

### Exact-arithmetic and GPU contracts

- Replaced ambiguous real/imaginary superscripts with lane subscripts.
- Specified the signed right-shift language mode, compile-time assertion, and
  negative rounding edge tests.
- Named the exact Q15 tie direction.
- Added explicit 192-bit product/carry proof obligations and maximal carry
  vectors.
- Made stream-ordered mask-word zeroing the responsibility of the public host
  wrapper and documented the dirty-word failure mode.
- Separated bit reproducibility from scientific correctness: exact equality
  verifies the implemented arithmetic on exercised cases, not the signal model
  or calibration transfer.

### Survey and calibration evidence

- Replaced survey scaffolding with a selection-aware account of triggered
  baseband captures, bounded-storage processing, product schemas, provenance,
  quarantine semantics, and exact reproduction records.
- Distinguished archive masked fractions from unconditional time occupancy.
- Added blocked, per-epoch holdout requirements rather than random frame splits.
- Added explicit release-ledger fields for events, frames, failures, storage,
  throughput, and join completeness; values unavailable in the source bundle
  remain marked “not supplied.”
- Formalized floor refusal for always-on or inadequately sampled channels.
- Split operating points by transmitter/station epoch and added an epoch visual.

### Residual chain and cosmology forecast

- Separated the measured scalar pilot proxy from visibility-domain quantities.
- Replaced one overloaded residual variable with distinct stochastic-variance
  and coherent-systematic terms.
- Stated that scalar intra-day shares are screening proxies, not measured
  attenuation of complex visibilities after sidereal filtering.
- Made the pilot-to-6-MHz transfer and scalar-to-visibility transfer explicit
  closing tests.
- Added required alternative residual templates: frequency-localized,
  low-`k_parallel`, wedge-like, sidereal-coherent, and empirical.
- Made reproduction of the published combined multi-redshift-bin Fisher
  estimator a quantitative validation gate.
- Formalized the derivative stability gate and the handling of sign crossings.
- Corrected the integration-time discussion by distinguishing a residual
  normalized to target-time noise from a fixed physical contaminant.
- Separated statistical time cost from coherent parameter bias.
- Reconciled the channel counts: ten measured channels, thirteen unmeasured,
  five current excision candidates, two measurement-limited channels, and three
  dilation-tier forecast-feasible candidates including an epoch split.

### Deployment and conclusions

- Removed language that could be read as claiming an already operating
  production `kotekan` stage.
- Added the proposed stage interface, buffer/alignment contracts, stream
  synchronization, fail-closed semantics, monitoring, runbook, and end-to-end
  performance acceptance criteria.
- Replaced a blanket recovery verdict with a channel-status evidence map and a
  table that distinguishes forecast-feasible, measurement-limited, epoch-split,
  excision-candidate, and unmeasured states.

## New visuals

1. `fig_claim_chain.pdf` — evidence chain and claim boundary
2. `fig_vsb_standard_model.pdf` — normative ATSC values versus geometric model
3. `fig_model_calibration_layers.pdf` — analytic model and calibration boundary
4. `fig_survey_evidence_flow.pdf` — archive selection, trawl, holdout, and ledger
5. `fig_epoch_operating_points.pdf` — pre/post station-epoch policy changes
6. `fig_residual_chain_audit.pdf` — pilot statistic to cosmological residual gates
7. `fig_deployment_lifecycle.pdf` — real-time stage lifecycle and failure paths
8. `fig_channel_status_matrix.pdf` — current 23-channel evidence/status map

Those eight framework visuals are now part of the dissertation-wide source system
in `figure_src/`.  They are regenerated with `python3 -m figure_src.generate_all`
alongside every other external figure and are included as vector PDFs for immediate
LaTeX builds.  The superseded first-pass generator is retained in `legacy/` only for
provenance.

## Results deliberately not invented

The dissertation source bundle does not contain the underlying survey ledger,
raw products, visibility products, or Fisher-analysis code needed to produce
several requested numbers. The revision therefore does not fabricate:

- exact discovered/eligible/processed/failed event and frame denominators;
- storage volume, transfer throughput, retry counts, or end-to-end trawl time;
- final Q16 threshold values for every channel and epoch;
- correlation times where the snapshot cadence forces a refusal;
- kept-frame floors for channels without a defensible off-state population;
- direct pilot-to-allocation or scalar-to-complex-visibility transfer functions;
- the combined-bin estimator comparison or residual-template sensitivity bank;
- results for the remaining thirteen channels; or
- live `kotekan` end-to-end latency and failure-injection results.

These are retained as explicit closing tests in Chapters 7–11 and Appendix A.

## Build and visual quality checks

- Regenerated all 25 external vector PDFs from the bundled Python source; 24 are
  active and one is retained as an editable design alternative.
- Rebuilt the two active architecture diagrams from named TikZ source files.
- Compiled with three consecutive `pdflatex` passes.
- Confirmed 117 US-letter pages, valid metadata, and no unresolved references,
  citations, overfull boxes, underfull boxes, or final-pass LaTeX warnings.
- Rendered all 117 pages at 100 dpi and inspected thirteen numerically ordered
  contact sheets, then inspected the densest scientific and architecture figures
  at full-page resolution.
- Confirmed no clipping, overlaps, broken glyphs, replacement characters, or
  black/empty-square glyph substitutions.
- Ran the bundled source/style audit over all 27 manifest artifacts.  The audit
  confirms source coverage, vector-only active external graphics, embedded Latin
  Modern fonts, no Type 3 or DejaVu substitution, matching Python/TikZ palettes,
  and a common physical inclusion width.
- The PDF is searchable and its fonts are embedded. It is not structurally
  tagged for accessibility; tagging remains a final-submission task if required
  by the submission date.

## Reproducible and coherent figure system

A second revision pass replaced the mixed-origin figure set with a single
source-backed system. Every active visual now maps to a bundled Python function
or named TikZ file, and the mapping is recorded in
`figure_src/figure_manifest.csv`. All active external graphics are vector PDFs;
the former raster transmitter map is now a scripted range--bearing figure.

The Matplotlib generator renders text through the same T1/Latin Modern LaTeX
stack used by the dissertation. TikZ figures inherit that font and use a shared
semantic palette. The build-time audit rejects missing source, missing data,
raster includes, Type 3 fonts, DejaVu substitution, non-embedded fonts, palette
drift, or inconsistent inclusion width.

Where direct arrays were absent from the supplied dissertation archive, the
prior vector paths were recovered into ordinary CSV tables with a documented
extraction script and retained reference PDFs. This creates an editable and
reproducible bridge without representing the recovered tables as authoritative
analysis exports. Their replacement by direct PilotProxy, survey, and Fisher
outputs remains an archival completion item.

## Repository export boundary and frozen-data consolidation

A further reproducibility pass removed the remaining ambiguity between the
PilotProxy repository and the dissertation bundle.

- Added a single frozen data directory,
  `figure_src/data/frozen_export/v1/`, with no second loose copy of any active
  CSV elsewhere in the bundle.
- Added `frozen_data_manifest.json`, recording each table's scientific owner,
  authority class, upstream source, row count, SHA-256 hash, and whether an
  authoritative replacement is still required.
- Moved the epoch-operating-point, channel-status, and channel-33 policy values
  out of plotting code and into versioned tables.
- Added `figure_src.import_dissertation_export`, which verifies a PilotProxy
  export and imports all matching available tables atomically while preserving
  unavailable bridge data.
- Extended the figure audit so every frozen CSV must match its manifest hash and
  row count and the frozen-table inventory must exactly match the figure
  dependency inventory.
- Kept dissertation-specific plotting and TikZ in this bundle; no PilotProxy
  analysis logic was copied into the thesis.
- Preserved seven legacy-artwork/external-model bridge tables with explicit
  `replacement_required` status rather than relabeling them as authoritative.

A companion repository patch adds the producing side of this interface:
`pilot_proxy.dissertation_exports`, a curated summary snapshot, documentation,
and tests. Generated repository exports remain gitignored; the dissertation
freezes the exact export it uses together with the producing commit.

## Full 500-mile transmitter-field revision

- Replaced the inner-only Figure 3.2 with a full 500-mile, DRAO-centred
  azimuthal-equidistant vector map.
- Added the complete authoritative `census_full_500mi.csv` export: 490
  emitter-channel records spanning physical channels 14--36.
- Aggregated exactly coincident source range--bearing records into 151 map
  sites, with marker area preserving the number of records at each site.
- Retained the original 120-mile individual-record view as a dedicated inset.
- Added an annular count panel that reports both emitter-channel records and
  distinct source range--bearing sites by 100-mile interval.
- Used marker shape for service composition and the dissertation semantic
  palette for frequency-tolerance evidence.
- Added vector coastlines and administrative boundaries for orientation only;
  the caption explicitly excludes terrain-screening or propagation claims.
- Clarified in Chapter 3 that the 132-record station-list summary and the
  normalized 490-row emitter-channel export are different products and should
  not be compared as though they were the same denominator.
- Added Basemap and its boundary dataset to the reproducible figure
  dependencies.
- Added a follow-up PilotProxy patch so the repository exporter emits both
  `census_full_500mi.csv` and `census_inner_120mi.csv`.

## Integrated legacy-evidence revision

- Consolidated the four restored legacy projects and their fixed reading PDFs
  under `evidence/`, removing the obsolete sidecar-package metadata.
- Added Appendix B to classify the retained results by evidence type, map each
  project to its current use, and record large externally held artifacts.
- Added the standards-chain 45,000-trial paired float/int4 study to Chapter 6,
  including bootstrap crossing intervals, the 200-trial CPU/GPU equality gate,
  and the generator startup-transient audit.
- Distinguished the older prototype's vertical shelf-equivalent bias from the
  paired horizontal detection-curve loss metric and from the present
  transform-only residual.
- Added the width-crossing coordinate and quantitative left-tail exposure trade
  to Chapter 8 without promoting the old positive-excess rule to the current
  science operating point.
- Added the measured guard-region blind spot and instrument-tone attribution
  logic to the deployment-monitoring rationale in Chapter 10.
- Added a current full-frame, two-stage paired-injection regeneration to the
  closing measurement program and to the evidence matrix.

## v13 (2026-08-19): repository-owned figures and the ISED-corrected census

- Moved every data-backed figure to the repository that owns its data:
  pilot-proxy renders the census-PSD plates, worked example, epoch operating
  points, and status matrix (`analysis/dissertation/`); bao-noise-tolerance
  renders the four `bao_*` forecast figures (`scripts/dissertation/`). The
  bundle vendors their PDFs (byte-reproducible in the owning repository under
  `SOURCE_DATE_EPOCH`; generating commits recorded in the figure manifest)
  and keeps editable source only for the analytic schematics, TikZ, the
  census map (renderer scheduled to move to dtv-station-census with the map
  tool), and the wiggle bridges. The frozen-data interface shrank to the four
  tables those bundle-scope figures read.
- Refreshed the census interface from the ISED-corrected census
  (dtv-station-census overlay): 499 emitter-channel records at 162 sites
  (was 490/151); the 120-mile subset is 36 rows. Figure 3.2, its caption, and
  the chapter-3 reduction narrative updated, including the verification
  finding that the compilation had anchored several Canadian rows on the
  community rather than the transmitter site (CHKL-1: 37.8 km, not 17.7).
- Open item recorded: the 132-record regional station-list summary
  (Table tab:census) is a separate hand-built compilation; its facility
  counts and nearest-facility distances (e.g. channel 27's "CHBC-DT at
  60 km", the "within 130 km" proximity set) pre-date the ISED re-siting and
  did not match the 490-row census either; re-deriving that table from
  licensed sites belongs to the planned census-table generator.
- MANIFEST.sha256 regenerated: the v12 manifest was stale for 57 files and
  omitted `figs/fig_census_psd_lower.pdf` and `last_import.json`; the v13
  manifest covers every bundled file except itself.

## v14 (2026-08-19): the complete 23-channel survey

- Integrated the final two channels (14 and 15, freq_ids 844/829, completed
  2026-08-19): the trawl now covers all 23 ATSC allocations. The 21
  previously published products are byte-identical to the prior snapshot;
  only the two new products and the aggregate numbers changed. New inventory:
  16,327 events enumerated / 6,140 outrigger-labelled exclusions / 10,187
  survey targets / 10,184 completed dispositions / 9,214 completed events
  represented in inventory / 8,983 with valid frames / 170,374 processed
  event--channel units / 750,461 frames; a
  third quarantined unit (one 844 capture with an unreadable header) joins
  the two truncated ones.
- Chapter 7 inventory, Chapter 9 snapshot framing (products now span
  z = 1.336-2.022), Table 9.7 (+2 rows), Table 9.8 (+2 columns), the
  occupancy/rethreshold numbers, Chapter 11's synthesis, Appendix A's status
  row, the checklist, and the intro band figure/caption all updated from the
  regenerated exports. The stale "residual-chain rows await evaluation"
  sentence in Chapter 9's opening (left over from v7) was corrected in
  passing.
- Channel 14 is a trace-family channel at the survey's extremes (52.6%
  intra-day share through a 2.7 dB ground filter; measured -48.8 dB floor
  from 1,151 null frames; <=9,470x at the cap). Channel 15 is a steady faint
  excess (~1.0 dB median) with zero null frames in eight years. Both carriers
  sit at/within 0.3 kHz of synthesis. Both correlation times refuse (episodic
  shelf).
- POLICY DECISION FLAGGED FOR SIGN-OFF: channels 14-15 satisfy the channel-36
  inclusive-for-now condition exactly (excision preferred only at the
  unverified coherence cap; bracket ends within 0.6% of survey time; ~75% of
  current-epoch frames released at eta = 1.4). The bundle and the regenerated
  policy adopt keep-and-mask (INCLUSIVE_KEEP extended {36} -> {14, 15, 36} on
  the pilot-proxy `complete-23` branch), consistent with the stated
  excision-only-where-recoverable-rounds-to-zero posture; the excised set and
  the 273/81 CHIME-channel disposition are unchanged. Under the previous
  locked rule the pair would instead be excised (8 excised; survey x1.0962 vs
  x1.1013 inclusive; the 0.47% difference is the price of keeping both at the
  cap). All headline numbers in this bundle use the inclusive policy.
- New policy numbers: deployed rule x1.2238 survey / x5.3701 worst bin;
  working threshold x1.1013 / x1.5854; kept-set current-epoch survival
  10.7% -> 89.6% over 265,152 frames (seventeen no-live-carrier channels).
- Figures regenerated: fig_census_psd_lower now renders channels 14-26
  (13 panels, 5-row grid), fig_channel_status_matrix shows all 23 product-covered
  (summary snapshot v3: 14/15 measurement-bound), fig_census_psd re-exported
  from the 23-product census_psd.csv, fig_intro_band drops the hatched
  queued-pair marking.

## Number-gate pass (2026-08-19/20): the encoded correction backlog, executed

The repository's number-gate CI (bao-noise-tolerance
`scripts/check_dissertation_numbers.py`) encodes the known content
corrections as machine checks; this pass drives its 39 open failures to
green. Content corrections, each per the gate's stated source of truth:

- Abstract rewritten to the completed 23-channel survey (was "Ten
  contiguous channels ... measure the remaining thirteen").
- Eisenstein et al. 2005 detected the feature in 46,748 SDSS LRGs (with
  ~221,000 2dFGRS galaxies contemporaneously), not "half a million".
- The archive span is 7.6 years everywhere (was "eight-year" /
  "eight years" in five places).
- 41.94 ms is the detector frame, not a CHIME integration property (the
  X-engine integrates ~31 ms); Ch. 1 reworded.
- The measured shelf range is system-noise level to 44 dB below it (was
  "10-35 dB"); the untreated tolerance excess spans ~3x10^2 (ch 33) to a
  few 10^6 (ch 30), not "three hundred thousand to five hundred thousand".
- Five transmitter sign-offs or station departures (19, 20, 26, 27, 32)
  were recorded on collected channels, not three.
- The survey archive is 8,983 usable snapshots (was "~8,500").
- Station distances are great-circle to the verified licensed site from
  the ISED-corrected census: CKVU-DT 241 km, CBUT-DT 242 km, KZJO 277 km
  (the old 389/451 km were road distances); tab:census caption updated
  and its export reference corrected to the 499-row census.
- SS9.3 quarterly-table provenance rewritten: the generating rule IS now
  identified (survey_composition.py, 2026-07-18, F > mu-hat + 0.012 mu0,
  legacy-halfband weight bank b0dce17a, fs/2-mistuned, pilots suppressed
  39-47 dB except channel 30's, which self-cancels 847 Hz from fs/4);
  "unrecorded" claims removed, table caption updated.
- Channel-33 chain ledger: the +30.5 dB is the NET chain gain (the
  ground filter's -7.6 dB is already inside it); the stale "+22.9 dB
  net" decomposition removed.
- Frame-stage r_proxy list on 35/34/36 corrected to the Table 9.6
  on-air shelves (0.085 / 3.9e-4 / 1.35e-3) with penalties recomputed.
- The BAO hand-back of the 200-ns cut's incidental DTV suppression is
  3.2-7.8 dB, not 5.9-7.8.
- SS6.2 encoding story corrected: native samples are excess-8; the
  ingest adapter repacks losslessly to two's complement (per byte,
  XOR 0x88); the kernel sign-extends nibbles. The transform-only cost
  of 5.9e-4 relative is -0.0026 dB (both quotes were 10x off).
- Fig. 9.4 / SS9.7 policy case put on one population: keep-everything
  regenerated on the acquisitions>=8 base (1566x residual multiple,
  3.35x time; pilot-proxy time penalty 3.4x on the same base); summary
  snapshot, figure table, and vendored Fig. 9.4 all updated.
- Table 8.1's pending cells filled from the epoch-restricted fine
  operating-point rerun (per-channel pairs: ch 31 1.50/98304, ch 32
  1.15/75366, ch 35 7.61/498656) with the calendar-late residuals
  (0.008 / 0.016 / 0.237) quoted in the text; captions updated to name
  the authoritative CSV.
- Table 11.1 extended from channels 27-36 to all 23 channels.
- Evidence anchors: the deployed positive-excess rule's false-alarm
  price is stated (48.5% of verified-quiet time in the candidate
  record; 44.2% recomputed on the full 11,199-frame ch 35 off-era null)
  and the committed coarse-vs-fine ROC / Youden-J analysis
  (pilot-proxy analysis/youden_j.py) is cited; the coherent-gain credit
  cites the committed fine-gain Monte Carlo evidence.
- Editor's-note phrasing removed throughout ("supplied for this
  revision", "not invented here", "the present draft", "left pending",
  "remembered analysis", "dissertation-source bundle", "the revised
  analysis").
- Repository hygiene: line endings normalized to LF byte-exactly and
  pinned with .gitattributes (the Overleaf import's blobs were already
  byte-exact; the CRLF came from an autocrlf checkout), restoring the
  frozen-table hashes; the gate itself gained TeX-aware normalization
  ({,} digit-group commas, -- and --- dashes) in bao-noise-tolerance.

## 2026-08-20 — suite audit cleanup

- The dissertation number gate now reads PilotProxy's explicit 23-channel v3
  summary and pins both scientific dependency checkouts to the immutable
  commits reviewed by the suite audit.
- The README and the first-block closeout in Chapter 9 now distinguish the
  historical ten-channel analysis freeze from the subsequently completed
  23-channel trawl. The census figure manifest records the current 499 rows at
  162 source range--bearing sites. The refreshed frozen census tables preserve
  `schema_version` and per-row `evidence_status`, keeping the 11 licence-only
  candidates auditable as an inclusive scenario rather than observed carriers.
- The top-level release boundary is now defined as every Git-tracked file
  except `MANIFEST.sha256` itself. A single generator/verifier enforces both
  inventory and SHA-256 content, `make verify` and CI run the check, and the
  manifest is regenerated only after the final source and PDF build.
- Frozen-data imports now require a full immutable Git SHA and record the
  portable upstream repository/commit and export-manifest hash instead of an
  absolute checkout path. Standard-library regression tests enforce both
  properties. The producing PilotProxy exporter now also refuses dirty tracked
  inputs, mismatched commit assertions, and source changes during export.
- The legacy 132-record station summary is explicitly historical: its
  pre-overlay distances no longer support active proximity claims in Chapters
  3 or 9. The current discussion uses the evidence-labelled 499-row envelope
  only for geometric plausibility and leaves propagation attribution to the
  measured spectra. The abstract's recovery/excision partition is reconciled
  to the 23-channel v3 status matrix with the channel-27 and channel-35 epoch
  qualifications preserved.
- Figure 3.2 now calls itself an inclusive census envelope, de-duplicates city
  labels, and fans out the inner-field annotations. The figure-manifest reader
  rejects malformed CSV row widths, and every vendored-figure producer is
  recorded with a full 40-character commit.
- The build-verification record now leads with the current release and marks
  its older hashes/counts as historical. CI has read-only token permissions,
  every checkout disables credential persistence, and routine LaTeX/Python
  scratch is ignored and removed by `make clean`.
