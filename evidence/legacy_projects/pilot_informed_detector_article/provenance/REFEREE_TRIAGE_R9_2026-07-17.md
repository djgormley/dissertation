# R9 triage (review of rev13h) — 2026-07-17

Verify-first results. The reviewer is CORRECT on every independently
checkable point; all seven required spectral corrections applied
(rev13i + delta12).

## Verified in-session

- Mask provenance of all_spectra.npz: mean masked fraction computed from
  the dump meta = 0.475984 -> 4.70796 MHz retained of 8.984, matching
  the 4.708 MHz ANALYTIC positive-excess rung of the Section-7 ladder,
  not the 3.512 MHz three-arm result. "After mask" relabelled everywhere
  (figure titles, legends, appendix) as the original analytic
  positive-excess production mask.
- Tone-to-cell distance: my ">140 kHz" claim in rev13h was WRONG — I
  took ch28 (-142.77 kHz) as nearest and overlooked ch14/ch34 at
  +81.19 kHz. True minima: 75.086 kHz from a cell centre, 73.561 kHz
  from cell support (reviewer's numbers reproduce exactly). Fixed to
  ">73 kHz from detector-cell support".
- Rational-fraction offsets: 4.8 / 7.9 / 7.9 / 9.5 / 9.5 Hz — all
  within 9.5 Hz (< half a 23.84 Hz bin). Wording now "within 9.5 Hz".
- Search domain: |off_pilot| > 10 kHz and |f_bb| > 100 Hz — the
  7.63–10 kHz annulus IS excluded; appendix now states the domain.
- Census: 42 nonblank detectability_db in the merged census (43
  pre-merge; one channel-share merge collapses two). Fig-1 caption and
  data/census/PROVENANCE.md corrected.
- CI claim: "|Δ| ≲ 0.1 dB at 95%" was incompatible with the widest
  paired-bootstrap interval [-0.24, +0.12]; contribution (ii) now
  quotes the intervals themselves.
- Backup mode: prose claimed per-channel analytic-mu0 normalization;
  the tested curves and testbench use the unnormalized raw-F ch14
  threshold. §5 now states as-implemented (unnormalized, ch14) vs
  deployment specification (per-channel analytic-mu0 rescale, shape
  unchanged).
- Veto: threearm_fulldepth.py baseline = per-capture median power of
  F-core frames (retrospective; core selection uses F). "Running/slowly
  updating" language replaced with retrospective slow-tracker-emulation
  wording; non-causality and F-informed selection stated. Deployment
  sentence (§8) already said "causal slow-tracked threshold" — kept.

## T2 sample-span finding (new, from the committed trim_report.json)

Committed trim_report.json: coherent projection over the FULL 600 000
samples reads 11.8301 dB (deficit +0.5301); audit v2 direct field reads
12.0239 (deficit +0.72) from the FIRST 262 144 samples
(DEFAULT_AUDIT_MAX_SAMPLES) with a ±10 kHz pilot window minus a
median-shelf baseline. Gap = 0.194 dB = sample span + estimator
convention (median-shelf baseline exact on flat synthetic — validated
0.001 dB — but plausibly over-subtracts under the pilot on the VSB
band-edge shoulder). §5.1 rewritten to present both estimators and the
0.53–0.72 dB convention-dependent deficit. The trim applied
amplitude ×1.06293 = +0.530 dB power (its report's "gain_db: 0.265"
was a formula bug — 10log10 instead of 20log10 — fixed in delta12; the
capture itself is correct).

EXPECTATION CORRECTION for G3: on the trimmed capture the audit's
direct field should read ≈ 11.49 dB (11.30 + 0.19 convention gap), NOT
11.30 ± 0.05 as earlier instructed. Span-isolation diagnostic (optional):
  python -m pilot_proxy.testbench.audit_atsc_signal \
    --input-iq generated/atsc/atsc_8vsb_complex64.cfile \
    --max-samples 600000 --output-json ~/audit_fullspan.json
(the module accepts --max-samples; the CLI wrapper does not expose it).
Closure verdict comes from the regenerated sweep crossings, not the
audit scalar.

## Other applied changes

- Δ column redefined as prominence-vs-local-background change under the
  analytic mask (each stream has its own running-median background);
  no absolute-amplitude or three-arm invariance claim.
- Notching declared cosmetic (supplementary plotting copies only); CSV
  action value "removed" -> "notched_in_supplement_only"; columns
  renamed prominence_db_before / prominence_db_after_analytic_mask.
- Attribution softened to "consistent with instrumental or
  digital-processing spurs, pending operations confirmation".
- Zoom title: "census lines" -> "extracted spectral lines".
- Layout: spur table [t]->[b] (now renders after the Appendix A
  heading, p.25); \FloatBarrier before §6.3 (Table 2 / Figs 6–7 no
  longer interrupt the author note). 27 pp, 0 overfull, no Type 3.

## Noted, still open (reviewer's central blockers)

- Phase 1a control floor, Phase 2 injection, matched comparator: G2/G4
  in flight on CANFAR.
- Six detections/prominences "provisional because spectral arrays not
  supplied": all_spectra.npz (5.3 MB) can be shipped to the reviewer or
  archived in provenance if wanted.
- Reviewer's approximate quantized-filter worst contribution (~-38 dB
  rel. local detector noise): to be reproduced from raw arrays before
  any use in the manuscript (not added).

## Addendum (same day): convention-gap prediction VERIFIED

audit_v3 on the trimmed capture (Dylan's console output, 2026-07-17):
measured_pilot_below_data_direct_db = 11.497 — prediction was ~11.49
(11.30 projection target + 0.19 gap). Gap before trim 0.1938, after
trim 0.197: stable through the trim, closing the estimator-convention
question by measurement. Shelf-extrapolated field 11.391; quality 5/5;
pilot placement error 0.44 Hz. §5.1 blue slot replaced with measured
text (rev13j); remaining optional slot: --max-samples 600000 span
isolation on the original capture. No re-trim needed; G3 sweeps proceed
on the trimmed capture as planned.
