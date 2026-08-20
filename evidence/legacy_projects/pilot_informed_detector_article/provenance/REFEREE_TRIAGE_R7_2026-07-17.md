# R7 triage (review of rev11c) — 2026-07-17

Verify-first results, then disposition. Reviewer's independent numbers all
reproduce in-session: RC correction 0.4727866 dB, conditional ratio
11.4456134 dB, offset +0.1456134 dB, displacement +0.1357192 dB, ncF
crossings −32.0903/−29.3796/−33.0404 dB, nominal Pd(−38) = 0.661063,
adjusted 0.656363 (reviewer ≈0.6564) — measured 0.662 is within 0.4σ of
both at n=1000 (σ=0.015).

## New measurement strengthening the reviewer's central T2 point

audit_atsc_signal.py extended with direct-integration fields
(band_power_integrated, data_power_direct_integration,
measured_pilot_below_data_direct_db, measured_pilot_below_data_mean_shelf_db)
and validated on a synthetic flat-spectrum capture with a known ratio of
13.0103 dB: direct field reads 13.0094 (0.001 dB accurate); the existing
median-Welch shelf estimator reads 12.6222 — a −0.39 dB bias on a FLAT
shelf, ~2.7x the inferred 0.146 dB pilot offset. The mean-shelf variant
reads 13.0009. Conclusion: R7 is right that the 11.9184 → 11.446
inference cannot be interpreted physically without the direct integral;
also note the real audit's own median-vs-mean spread is 0.457 dB.
ONE-COMMAND CLOSURE for Dylan (after applying delta4 patch):
  pilot-proxy audit-atsc --input-iq generated/atsc/atsc_8vsb_complex64.cfile \
    --output-json ~/audit_v2.json
and send audit_v2.json (or just measured_pilot_below_data_direct_db).

## Applied (rev12)

- §5.1 calibration passage: reviewer's wording adopted — "approximately
  0.146 dB pilot-amplitude offset", "0.136 dB horizontal displacement",
  no "genuine deficit", no "reproduced exactly" (both nominal 0.6611 and
  adjusted 0.6564 quoted vs 0.662 ± 0.015), int4-leading-candidate
  replaced by "unattributed pending a matched full-precision control";
  estimator-sensitivity numbers (0.457 dB median-vs-mean, 7.9 dB p-p
  flatness) cited as the reason interpretation waits. Contribution (ii)
  aligned.
- "Proposed deployment default" → "conservative scenario" at all seven
  sites (abstract, contribution v, Table 2 caption, §7 x2, §8.1, §8.2,
  conclusions); Table-2 caption and §8.2 blue slots sharpened to ask for
  the operating-point decision documentation + acceptance pair.
- Fig. 5: ordinate renamed "non-null excess among retained frames";
  "ch34 (clean)" → "ch34"; "adopted ceiling (k=0)" marked on the axvline;
  k<0 region annotated "not adopted". §5.5 corrected: the adopted ceiling
  sits at k=0 exactly, the boundary of the k<0 region (previous text
  wrongly said the operating point occupies k<0). Caption defines the
  estimator as excess-over-model (instrumental tails, non-Gaussian noise,
  and DTV all contribute).
- "Only continuous per-frame detection tracks the actual RF environment"
  → tracks-at-frame-cadence phrasing that credits CHIME's existing
  visibility-cadence dynamic rule as complementary.
- Selection coupling: "designed/intended to reduce"; both reviewer
  caveats added (1/128 statistic dilution ≠ science-band transfer; veto
  F-independent but not power-independent); magnitude → Phase 2.
- Wording cleanup: "substantial cost" dropped; "exact, cheap,
  self-calibrating" → "exact-integer detector with an internal
  consistency check"; "trusted core" → "calibrated null core";
  "no effective-degrees-of-freedom slack" → consistency check with no
  width uncertainty assigned; 0.5-invariant claim conditioned on Phase-1
  verification; abstract drops "Production-GPU values are marked where
  pending", calls 38% a preliminary archive scenario, veto tail clipped
  by construction with achieved cleanliness pending; conclusions call
  52.5 MHz preliminary and list simultaneity + boundary accounting + the
  representative full-band test.
- Preflight: Type 3 font eliminated (it was the itemize bullet resolving
  through TS1 to a PK bitmap tcrm1095; \labelitemi → $\bullet$ in the
  scratch wrapper); \usepackage{placeins} + \FloatBarrier after the
  bibliography and before Appendix B (Figs 9/10 float containment).

## Noted, not actionable by us

- "Audit JSON / IQ hash / 45k-trial bundle not attached": they are in the
  source zip (provenance/); reviewer saw the PDF only.
- Trigger/schedule composition of the 47.8% sample, per-channel exposure,
  common-strata robustness: requires archive metadata Dylan must pull;
  existing blue slot stands (composition sentence already requested).
- Phase 1/2 gates: unchanged, GPU-slotted.
- Full-width figure check in the actual RASTI/MNRAS class build: with the
  class swap item.

## Addendum (same day): T2 closure measurements

audit_v2 received (direct field 12.0239 dB -> 0.72 dB genuine pilot
deficit; RC-convention inference retracted). Matched full-precision
control computed from the archived 45k trials (cpu_float_fstat_raw):
int4-float crossing differences -0.044/-0.018/-0.063 dB -> quantization
exonerated. §5.1 and contribution (ii) rewritten with the measured
decomposition; the remaining action is the generator pilot-amplitude
correction before the deployment-scale regeneration. This also resolves
R7's "int4 leading candidate" wording item by measurement rather than
rewording.
