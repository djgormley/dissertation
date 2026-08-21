# Archive and analysis completion checklist — revised 2026-08-19

This checklist contains only work that requires data products, analysis code,
or live telescope integration that was not present in the dissertation source
bundle. It is aligned with Chapters 7–11 and Appendix A.

Status update (2026-08-19): THE TRAWL IS COMPLETE. All 23 allocations
(channels 14–36) carry products, each complete against its archive holdings,
under one kernel cohort; channels 15 and 14 (the last in the scan order)
finished 2026-08-19 with 8,347 and 8,788 events. Item B is closed at the
survey, epoch, and residual-chain level (Tables 9.7/9.8 extended to the
band-edge pair; every screening status survived the chain). What remains of
the archive program is the release ledger (item A, now for all 23 channels),
the cadence campaigns or their permanent-bound fallback (item C), the
transfer/visibility/estimator validations (items D–F), and the per-epoch
bundles and holdout (item G). The sign-off epochs measured on channels 19,
20, 26 (and, in the first-measured block, 27 and 32) supply transmitter-off
floors that unblock parts of items C and G. Channel 30's baseband collection
ceased in September 2023 (operations exclusion driven by the contamination),
which items A and C should record as an endogenous-selection boundary.
Channels 14–15 are kept-and-masked under the channel-36 inclusive-for-now
rule (both satisfy its general condition: excision preferred only at the
unverified coherence cap, bracket spread immaterial, ~75% of current-epoch
frames released at the working threshold) — this extension of the
inclusive-keep set from {36} to {14, 15, 36} is flagged for sign-off.

## A. Freeze the current 23-channel release ledger

- Export exact discovered, eligible, processed, skipped, failed, quarantined,
  duplicated, and joined event/frame counts for channels 14–36, retaining the
  historical first-block boundary at channels 27–36 as an explicit cohort.
- Record first/last valid UTC, gaps, trigger classes, operations states, and
  coverage by UTC, local time, season, and sidereal time.
- Record raw bytes discovered/transferred, peak staged storage, retained-product
  bytes, retry counts, throughput, GPU time, and end-to-end wall time.
- Attach source, binary, CUDA/toolkit, schema, weight-bank, transform, and
  calibration hashes for every cohort.
- Report the exact denominator behind the cross-era “zero mismatches” result.

## B. Process the remaining thirteen ATSC allocations
### (2026-08-19: COMPLETE — channels 14–26 all processed, chain-evaluated,
### and policy-evaluated; the per-channel release records below remain
### required for the release ledger, item A)

For channels 14–26, produce the same immutable schema used for channels 27–36:

- anchor localization and epoch checks;
- fine and coarse statistic distributions;
- verified off-state/null populations or explicit censoring/refusal;
- masked fractions and kept-frame proxy floors;
- structure functions and measured/bounded/refused correlation times;
- per-epoch threshold sweeps and policy costs; and
- the same census, provenance, and holdout records.

Do not interpolate verdicts from the current high-channel block.

## C. Run contiguous cadence campaigns

The campaigns are specified here so the requirement is concrete whether or not
they are executed; if they are not, the sidereal-day caps stand as permanent
conservative bounds and certification shifts to the blocked holdout and the
per-channel jackknife of the final analysis (item G).

Specified acquisition (unit: one 42-ms detector frame per freq_id, ≈34 MB at
the full array; ≈1.1 TB total; scheduled captures, tagged distinct from
triggered ones):

- ch 29 (freq_id 614) and ch 21 (freq_id 736), co-priority: two 12-h sessions
  each (one calm, one warm-season ducting day), 1 frame/30 s plus three 30-s
  continuous stretches per session. The survey's two best-floored coherence
  hostages (8,119 and 14,647 null frames); a minutes-scale tau_c moves each
  verdict by ~3 orders of magnitude.
- ch 34 (537): same specification; decides the 1,603×-at-cap row.
- ch 36 (506): two 6-h sessions in the measured burst windows (July–August,
  ~09:00–12:00 local), 1 frame/10 s plus 5-s stretches every 30 min; decides
  the keep-and-mask override's coherence flag.
- ch 33 (552): one 12-h session; refines the ≤5-min bound (set by the
  archive's shortest resolvable lag) toward seconds, which would move the
  24×-over screening result by ~15 dB of coherence.
- ch 32 (568): one 12-h session; confirms the era-resolved 174 min with
  gap-free lags.
- ch 23 (706): one 12-h session; same ≤5-min refinement for the lower-band
  chain rows.
- Free rider during every session: 1 frame/5 min on all kept DTV freq_ids
  (~5 GB per channel per session) for gap-free lag coverage feeding the
  per-epoch chain rows.
- Reproduce incumbent flaggers at their native few-second cadence; the
  triggered snapshot archive cannot do this honestly.
- Diagnose the broad/multiple fine-axis structures on channel 33.
- Within-event frame-to-frame coherence from the existing archive is the
  no-new-collection fallback for the burst channels' fast end.

## D. Validate the pilot proxy across each allocation

- Record simultaneous spectra across representative coarse channels spanning
  each 6-MHz allocation, not only the pilot-containing coarse channel.
- Measure the received pilot-to-shelf ratio distribution by channel, epoch,
  propagation state, and transmitter environment.
- Propagate that distribution, rather than only the nominal transmitter ratio,
  through threshold optimization and channel verdicts.

## E. Calibrate the visibility-domain residual chain

- Preserve contaminated complex visibilities before and after the
  per-sidereal-day mean-subtraction operation.
- Measure baseline, phase, frequency, and sidereal-time dependence.
- Fit separate stochastic added-variance and coherent systematic components.
- Replace the unity scalar-transfer closure with measured `g_var` and `g_sys`
  distributions and uncertainties.
- Validate any delay-filter credit on the same residual products used by the
  science forecast.

## F. Close the Fisher-forecast gates

- Reproduce the collaboration's published combined multi-redshift-bin estimator.
- Compare absolute errors, bias tolerances, policy rankings, and selected
  operating points with the current per-bin implementation.
- Repeat the bias calculation for noise-shaped, frequency-localized,
  low-`k_parallel`, wedge-like, sidereal-coherent, and empirical residual
  templates.
- Run both target-time-noise-normalized and fixed-physical-amplitude time-scaling
  families.
- Retain the derivative sign/movement stability gate and publish rejected points.

## G. Freeze per-epoch calibration bundles

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

## H. Complete live integration

- Implement the Chapter 10 stage on the actual `kotekan` buffer path.
- Verify frame identity, span, channel geometry, calibration hash, CUDA stream
  ordering, completion count, exact marginal tripwire, and downstream readiness.
- Exercise dirty mask words, invalid spans, CUDA failures, stale calibration,
  deadline misses, and restart/recovery behavior.
- Report end-to-end latency percentiles and misses under full telescope load,
  not only standalone kernel timing.
- Demonstrate monitoring, drift-triggered re-localization, and a reproducible
  incident-capture path.

## I. Final dissertation updates after the campaigns

- Replace all pending/bounded cells with measurements only where supported.
- Regenerate the 23-channel status matrix and channel tables.
- Update the abstract and conclusions only after all transfer and estimator gates
  have passed.
- Attach the immutable release manifest and archived analysis/code DOI.
- Complete structural PDF tagging and any submission-office accessibility checks.
