# Archive and analysis completion checklist — revised 2026-08-20

This checklist contains only work that requires data products, analysis code,
or live telescope integration that was not present in the dissertation source
bundle. It is aligned with Chapters 7–11 and Appendix A.

Status update (2026-08-20): THE OFFLINE TRAWL IS COMPLETE. All 23 allocations
(channels 14–36) carry products, each complete against its archive holdings,
under one detector-kernel hash; the release ledger must nevertheless preserve
the two analyzer/source cohorts present in the products. Channels 15 and 14
(the last in the scan order)
finished 2026-08-19 with 8,347 and 8,788 events. Item B is closed at the
survey, epoch, and residual-chain product level (Tables 9.7/9.8 extended to the
band-edge pair). The v4 release retains the legacy classifications
provisionally; it does not claim that a new blinded, health-recomputed status
gate was run. The
attachment-supported part of the archive program is now closed in item A: the
release applies the versioned health gate, repairs the exactly reconstructible
spectral contribution, rebuilds the fine diagnostics, and publishes the
immutable ledger and all-channel figures.  The absent operations telemetry is
recorded as unavailable rather than estimated.  What remains is the cadence
campaigns or their permanent-bound fallback (item C), the pilot-to-allocation
and visibility-transfer measurements (items D and E), the empirical half of the
otherwise completed forecast gate (item F), and the per-epoch bundles and
holdout (item G). The current-geometry sensitivity and numerical
representation-loss study (item H) is running and remains mandatory before the
dissertation claims a measured current-geometry sensitivity. The sign-off
epochs measured on channels 19,
20, 26 (and, in the first-measured block, 27 and 32) supply transmitter-off
floors that unblock parts of items C and G. Channel 30's baseband collection
ceased in September 2023 (operations exclusion driven by the contamination),
which items A and C should record as an endogenous-selection boundary.
Channels 14–15 are kept-and-masked under the channel-36 inclusive-for-now
rule (both satisfy its general condition: excision preferred only at the
unverified coherence cap, bracket spread immaterial, ~75% of current-epoch
frames released at the working threshold) — this extension of the
inclusive-keep set from {36} to {14, 15, 36} is flagged for sign-off.

## A. Repair product validity and freeze the all-23-channel release ledger
### (2026-08-20: COMPLETE for the evidence retained by the three attachments)

- **Complete:** exact survey-scope, inventory, product, zero-frame, quarantine,
  duplicate, and join denominators are exported for channels 14--36.  The
  inventory records 16,327 enumerated events, 6,140 excluded by the recorded
  outrigger-label rule, 10,187 target events, 10,184 completed events, and three
  events frozen in the source inventory's pending-attempt category after two
  recorded attempts. Their three unprocessed units are the released
  quarantines, not an active retry queue; 9,214 events contribute inventory
  rows.
- **Complete, with an explicit timing denominator:** the release records
  per-channel first/last UTC and gaps and tabulates health-included exposure by
  UTC, America/Vancouver civil time, meteorological season, local mean sidereal
  hour, and triggered-versus-scheduled class.  Of 750,279 health-included
  frames, 747,790 have a finite timestamp and positive duration; no duration is
  invented for the other 2,489.
- **Complete where recorded:** the inventory preserves 28,237,618,443,352
  catalogued source bytes and three retried scope events, each with two attempts.
  It does not contain transferred bytes, peak staging storage, throughput, GPU
  time, wall time, per-attempt reason codes, or complete operations states.
  Those fields are permanently marked unavailable unless independent logs are
  later recovered.
- **Complete:** the release binds every product to the supplied detector binary,
  schema, transform, and weight metadata and preserves both analyzer-source
  cohorts.  The modern 21-product source digest is reproduced by clean
  PilotProxy commit `94b1de0`; the distinct two-product legacy digest remains
  unmatched.  The denominator behind a separate historical cross-build
  “zero mismatches” statement was not retained and is not reconstructed.
- **Complete:** the v1 gate excludes the four all-zero invalid frames and all
  178 frames at the theoretical packed-int4 power ceiling.  Equality at that
  ceiling proves a constant native excess-8 byte `0x00`, equivalently
  detector-input `0x88` after the lossless repack.  The exact acquisition-side
  cause remains unknowable without raw HDF5 or logs, but the validity decision
  does not: a constant negative-full-scale frame is not a sky measurement.
- **Complete:** every excluded row has an immutable physical key and reason;
  scalar distributions and policy inputs are regenerated on 750,279 included
  frames.  The special constant-word FFT contribution is exactly subtracted
  from 178 before-mask and 118 after-mask accumulator contributions; 60 of the
  affected rows were already rejected by the stored coarse rule.  Every repaired
  spectrum remains non-negative and satisfies the declared Parseval gate.
- **Complete as a retrospective diagnostic:** designated-window quantities are
  recomputed from the retained 256-bin fine arrays using a geometry-predicted
  acquisition neighbourhood, a gated quarterly measured-line window, circular
  bin arithmetic, and a non-selecting out-of-window sentinel.  The stored bin-0
  ancillary CFAR arrays are not promoted.  These retrospective anchors are not
  relabelled as the prospective per-epoch Q16 bundle and blocked holdout still
  required by item G.
- **Complete:** all-23 health-filtered tables and 92 diagnostic assets are
  released.  The 23 appendix plates include histograms, relative time-averaged
  before/after spectra, and fine-statistic UTC heatmaps.  They are explicitly
  not absolute PSDs or raw-voltage spectrograms, which cannot be recovered from
  the stored aggregate products.

## B. Process the remaining thirteen ATSC allocations
### (2026-08-19: COMPLETE — channels 14–26 all processed and chain-evaluated;
### the provisional legacy policy classifications are not a new blinded
### health-recomputed verdict, and the per-channel release records below remain
### part of the release ledger in item A)

For channels 14–26, produce the same immutable schema used for channels 27–36:

- anchor localization and epoch checks;
- fine and coarse statistic distributions;
- verified off-state/null populations or explicit censoring/refusal;
- masked fractions and kept-frame proxy floors;
- structure functions and measured/bounded/refused correlation times;
- per-epoch threshold sweeps and policy costs; and
- the same census and provenance records.

The blocked holdout is excluded from this completed processing item. It belongs
exclusively to item G and remains open until the decision rule is frozen before
the reserved blocks are opened.

Do not interpolate verdicts from the current high-channel block.

## C. Run contiguous cadence campaigns

**Status: requires newly scheduled telescope captures.**  The retained products
can support within-event fast-lag diagnostics and conservative sidereal-day
bounds, but they cannot reconstruct a gap-free hours-long time series or the
incumbent flaggers' native cadence.

The campaigns are specified here so the requirement is concrete whether or not
they are executed; if they are not, the sidereal-day caps stand as permanent
conservative bounds and certification shifts to the blocked holdout and the
per-channel jackknife of the final analysis (item G).

Specified acquisition (unit: one 42-ms detector frame per freq_id, ≈34 MB at
the full array; scheduled captures tagged distinctly from triggered ones):

- ch 29 (freq_id 614) and ch 21 (freq_id 736), co-priority: two 12-h sessions
  each (one calm, one warm-season ducting day), 1 frame/30 s plus three 30-s
  continuous stretches per session. These are large-null, coherence-limited
  co-priorities (8,119 and 14,647 full-era null frames); a minutes-scale tau_c moves each
  verdict by ~3 orders of magnitude.
- ch 34 (537): same specification; decides the health-filtered 1,600×-at-cap row.
- ch 36 (506): two 6-h sessions in the measured burst windows (July–August,
  ~09:00–12:00 local), 1 frame/10 s plus 5-s stretches every 30 min; decides
  the keep-and-mask override's coherence flag.
- ch 33 (552): one 12-h session at 1 frame/30 s plus three 30-s continuous
  stretches; refines the ≤5-min bound (set by the
  archive's shortest resolvable lag) toward seconds, which would move the
  24×-over screening result by ~15 dB of coherence.
- ch 32 (568): one 12-h session at 1 frame/30 s plus three 30-s continuous
  stretches; confirms the era-resolved 174 min with gap-free lags.
- ch 23 (706): one 12-h session at 1 frame/30 s plus three 30-s continuous
  stretches; same ≤5-min refinement for the lower-band chain rows.
- Free rider during every session: 1 frame/5 min on the 23 monitored pilot
  coarse channels (one per ATSC allocation), not on all 273 operationally kept
  CHIME bins. This costs about 5 GB per monitored channel per 12-h session and
  supplies sparse gap-free lag coverage for the per-epoch chain rows.

The target-channel schedule above is approximately 1.35 TB. The 23-channel
free-rider stream adds approximately 1.13 TB over the program's 120 scheduled
hours, for a baseline of about 2.5 TB before container, metadata, and staging
overhead. Sampling all 273 operationally kept CHIME bins would instead add
roughly 13.4 TB and is outside this baseline; it requires a separately approved
storage plan. The native-cadence incumbent-flagger stream below is likewise not
included until its exact representation and retention window are specified.
- Reproduce incumbent flaggers at their native few-second cadence; the
  triggered snapshot archive cannot do this honestly.
- Diagnose the broad/multiple fine-axis structures on channel 33.
- Within-event frame-to-frame coherence from the existing archive is the
  no-new-collection fallback for the burst channels' fast end.

Two orderings exist for these targets and they answer different questions. The scheduling above ranks channels whose *verdict* hangs on a measured correlation time. Ranking instead by how far a measured time would move the *operating threshold* -- the ratio between each channel's cost optimum at the two ends of the coherence bracket -- puts channels 14 (9.9x), 36 (8.3x), 18 (5.7x), 15 (4.6x) and 27 (4.0x) first, of which only 36 is scheduled here. Under the bounded basis no verdict depends on the measurement at all, since every excision is a carrier-dominance call; what it buys is cost. Revisit the ordering against whichever objective is in force when the campaign is revived.

## D. Validate the pilot proxy across each allocation

**Status: requires data not present in the attachments.**  The supplied products
contain only the pilot-containing coarse channel.  Existing simultaneous
neighbouring-channel baseband could close this by reprocessing if it is retained
and accessible; otherwise representative multi-channel captures must be newly
scheduled.  No scalar transformation of the pilot-only NPZ can measure this
transfer.

- Record simultaneous spectra across representative coarse channels spanning
  each 6-MHz allocation, not only the pilot-containing coarse channel.
- Measure the received pilot-to-shelf ratio distribution by channel, epoch,
  propagation state, and transmitter environment.
- Propagate that distribution, rather than only the nominal transmitter ratio,
  through threshold optimization and channel verdicts.

## E. Calibrate the visibility-domain residual chain

**Status: requires collaboration visibility products or new collection.**  The
attached inventory and per-pilot NPZs contain neither complex visibilities nor
baseline/phase coordinates.  If pre/post-subtraction visibilities already exist,
this is an access and reprocessing task; if they were not retained, the pipeline
must preserve them in a future observing campaign.

- Preserve contaminated complex visibilities before and after the
  per-sidereal-day mean-subtraction operation.
- Measure baseline, phase, frequency, and sidereal-time dependence.
- Fit separate stochastic added-variance and coherent systematic components.
- Replace the unity scalar-transfer closure with measured `g_var` and `g_sys`
  distributions and uncertainties.
- Validate any delay-filter credit on the same residual products used by the
  science forecast.

## F. Close the Fisher-forecast gates

Status (2026-08-20): the code-side portion is complete.  The independent
per-bin noise-normalized estimator and the joint multi-redshift-bin estimator
now run over all seven DTV bins for the noise-shaped, low-$k_\parallel$,
wedge-like, and localized-$|k|$ analytic families; the joint estimator is also
run under both declared time-scaling definitions.  The release publishes every
accepted and refused point, a conservative physical-channel mapping, and the
full authenticated bank/runtime identities.  What remains in this item is the
empirical-template half, which cannot be constructed from the scalar archive:
it requires the visibility products in item E and a response interface exposing
their frequency, baseline, and sidereal coordinates.

- **Complete:** reproduce the collaboration-style combined multi-redshift-bin
  estimator and compare its errors and bias tolerances with the independent
  per-bin implementation across all seven bins.
- **Complete at the analytic-model level:** execute the noise-shaped,
  low-`k_parallel`, wedge-like, and localized-`|k|` families.  The analytic
  envelope alone does not authorize a policy-status or ranking change.
- **Data-dependent:** construct frequency-localized, baseline-localized,
  sidereal-coherent, and empirical residual templates from item E rather than
  fabricating them in a callable that exposes none of those coordinates.
- **Complete for the combined estimator:** run both target-time-noise-normalized
  and fixed-physical-amplitude time-scaling families, with exact equality
  verified at the reference time.  The independent per-bin release uses the
  noise-normalized family only.
- **Complete:** retain the derivative sign/movement stability gate and publish
  every rejected point.

## G. Freeze per-epoch calibration bundles

**Status: partially code-supported, but not closable as a blinded validation
from the inspected attachments alone.**  The v1 release can emit provisional
quarterly anchor/refusal records and deterministic temporal splits.  It cannot
recover the three historical integer fine-power terms for exact Q16 replay, and
the full archive has already informed method development.  A certification-grade
holdout therefore requires either a genuinely unopened retained interval whose
boundary is approved before examination or a future epoch collected after the
bundle is frozen.

For every channel and stable station/transmitter epoch, release together:

- anchor and designated window;
- reference placement and census exclusions;
- null bulk and rank;
- multiplier and exact Q16 representation;
- calibration/holdout intervals and measured false-alarm rate;
- selected masked fraction, residual terms, cost, and evidence status; and
- all source and product hashes.

A bundle must never combine an anchor from one epoch with a threshold or null
model from another.

## H. Complete the current-geometry synthetic sensitivity and representation-loss study

**Status: running in code; no new telescope observation is required.**  The
current 23-profile weights, standards-chain generator, packed sample path,
fixed transform, supplied v2.1 kernel, CPU reference, and an RTX-class GPU are
available.  The final release is accepted only if its predeclared crossing,
multi-seed, false-alarm-tail, uncertainty, clipping, and literal full-frame
audit gates pass; a partially completed sweep is not promoted.

This is a dissertation-completion experiment, not an optional deployment
extension. The legacy paired injection establishes the method but uses a
superseded detector geometry; its numerical sensitivity and loss must not be
promoted to the current implementation.

- Exercise the current full geometry ($M=2048$, $K=128$, $L=128$,
  $L_F=256$) and all 23 channel weight profiles, including the channel-14 edge
  wrap, measured residual-offset distribution, and half-bin worst cases.
- Use common waveform and noise draws for paired stages: analytic ideal;
  full-precision pure-tone plus AWGN; full-precision standards-chain 8-VSB;
  int4 input quantization/clipping with a floating detector; quantized weights;
  the frozen fixed-point transform; exact Q16 decision arithmetic; and the
  complete CPU/GPU pipeline.
- Report ideal-to-float model mismatch separately from input-quantization,
  coefficient-quantization, transform, and decision-arithmetic losses. Do not
  label the entire ideal-to-end-to-end difference “fixed-point loss.”
- Sweep shelf/pilot SNR until every detection-probability crossing is bracketed;
  evaluate multiple declared false-alarm probabilities and residual offsets.
  Report detection probability at fixed false-alarm probability and horizontal
  SNR loss at fixed detection probability, with exact binomial intervals and
  paired bootstrap intervals for stage-to-stage loss.
- Include false-alarm calibration, threshold-near disagreement rates,
  overflow, saturation and clipping counts, CPU/GPU bit equality, an offset
  sensitivity map, and per-channel as well as band-summary losses.
- Use the sufficient-statistic simulator for large statistical sweeps only if a
  stratified subset also traverses the actual packed, full-frame implementation.
  Audit generator startup/transients and analyze only the declared stationary
  span.
- Release configuration, seeds or paired trial identifiers, trial counts,
  crossing tables, source/binary/toolchain/weight/transform hashes, and the
  generated figures. Replace the legacy numerical sensitivity in the main
  argument only after this release is reproducible.

## I. Complete live integration

**Status: requires the actual `kotekan` integration environment, telescope-load
test, and operations authority.**  Repository code can implement and unit-test
the stage surface, but archive products cannot measure live buffer alignment,
contention, recovery, latency, drift response, or incident capture.

- Implement the Chapter 10 stage on the actual `kotekan` buffer path.
- Verify frame identity, span, channel geometry, calibration hash, CUDA stream
  ordering, completion count, exact marginal tripwire, and downstream readiness.
- Exercise dirty mask words, invalid spans, CUDA failures, stale calibration,
  deadline misses, and restart/recovery behavior.
- Report end-to-end latency percentiles and misses under full telescope load,
  not only standalone kernel timing.
- Demonstrate monitoring, drift-triggered re-localization, and a reproducible
  incident-capture path.

## J. Final dissertation updates after the campaigns

**Status: document regeneration is code-supported; institutional submission
actions are external.**  This revision completes the attachment-supported
archive and analytic-forecast writing and will incorporate the current-geometry
synthetic release.  DOI deposition, author/collaboration sign-off, and the
submission office's accessibility acceptance require account or institutional
action outside the repositories.

- Replace all pending/bounded cells with measurements only where supported.
- Regenerate the 23-channel status matrix and channel tables.
- Incorporate the repaired archive products and the current-geometry synthetic
  sensitivity/representation-loss result; retain the legacy study only as
  explicitly labelled historical geometry.
- Update the abstract and conclusions only after all transfer and estimator gates
  have passed.
- Attach the immutable release manifest and archived analysis/code DOI.
- Complete structural PDF tagging and any submission-office accessibility checks.
