# Survey composition + classified-FRB stratum robustness — 2026-07-17

Closes the R7/R8/R9 survey-bias item using the event-key dump
(event_presence_keys.csv.gz, 8604 events / 77,423 product pairs — bitmask
verified LSB-first against per-channel unit counts, 23/23 exact) joined to
the datatrawl inventory (161,872 records; event -> obs_date, datasets,
per-fid n_frames).

## Unit->event assignment

Units carry capture times; inventory carries day-level obs_date. Join key
= (day +/-1, frame count): unit_frames == floor(inventory n_frames)
measured at 97.4% on singleton days (2635 pairs). Outcomes over 77,423
units: exact 49.1%, class-unique 29.4%, day-pure 0.5% (=> 79.0%
confidently classed), mixed 21.1% (excluded from strata), orphan 0.1%.
Naive day-only join is unusable (89.6% of units fall on mixed-class days).

## Results (analysis/survey_composition.py; CSVs archived alongside)

- Sampled-vs-archive composition per channel: full-depth channels match by
  construction; capped channels are NOT class-neutral (ch14: 21% FRB
  sampled vs 44% archive; crab 32% vs 18%).
- All four secular transitions PERSIST in the classified-FRB stratum:
  ch33 0.44/0.39 -> 0.01 (same quarter boundary), ch32 0.32 -> 0.03,
  ch35 0.00 -> 0.17, ch17 endpoints 0.03 -> 0.36 (all-events 0.05 -> 0.35).
  Step-transition channels (32/33/35) are full-depth (5118-8304 events) —
  cap bias cannot enter them.
- TIMING CORRECTION found: ch32's fall is 2023 April--May (monthly: Feb
  0.36, Mar 0.30, Apr 0.09, May 0.005), NOT "Q3 2023" as previously
  stated; §6.3 corrected. ch33 falls by 2020 Q2 ("by mid-2020" kept,
  repack-consistent). ch35 onset 2021 Q4 confirmed.
- ch17 is capped (2000) with NO mid-period quarters above the 40-frame
  floor: the 2020->2025 rise is an endpoint statement; text now says so.
- Compositional artifact exposed: ch33's 2020 Q4 rebound (0.42, n=66) is
  carried by non-FRB captures; absent in the FRB stratum.

## Audit 2x2 addendum (same day; audit_orig/trim_fullspan.json)

num_samples_used = 524,288 (module truncates 600k to whole 65,536-sample
segments). Direct-field 2x2:
              262,144     524,288    projection(600k)
  original    12.0239     11.5951    11.8301
  trimmed     11.4970     11.0829    11.3000 (target)
Span effect (fixed method): -0.429 / -0.414 dB. Method effect at long
span: -0.235 / -0.217 dB (windowed BELOW projection — sign flips vs the
default span). Trim shift: -0.527 / -0.512 / -0.530 dB — convention-stable.
data_power_direct identical to 9 significant digits original-vs-trimmed at
524k (0.1268696662607189 vs 0.1268696661809648): trim touched only the
pilot line. Exact half-file decomposition (using audit_v2 band/data):
window-summed pilot power second 262,144 samples = +0.841 dB over the
first (data +0.012 dB): THE GENERATED PILOT LINE IS NOT STATIONARY ACROSS
THE CAPTURE — this, not a baseline subtlety alone, is why the audit
scalar is span-dependent. Deficit convention-bounded 0.30–0.72 dB; §5.1
rewritten. Remaining optional diagnostic: per-block projection profile
(amplitude ramp vs decoherence). Sweep implication (noted, not in text):
per-trial pilot power varies with file position by ~±0.4 dB about the
trimmed mean; crossings average over the capture.

## Addendum: per-block projection profile (Dylan's run, same day)

|A|^2 by tenth-of-file block (60k samples each): 1.039e-3, 8.842e-3,
9.551e-3, 9.635e-3, 9.602e-3, 9.655e-3, 9.521e-3, 9.863e-3, 9.998e-3,
9.907e-3. Stationary mean (blocks 2-9) = 9.716e-3. Block 0 = -9.71 dB,
block 1 = -0.41 dB vs stationary: a GENERATOR STARTUP TRANSIENT
(first ~11 ms), stationary thereafter. Phase drift linear, -0.070 Hz
projection offset, coherence loss <1e-4 (no decoherence).

SWEEP IMPACT: NONE. evaluate_snr uses clean_iq[:required] (same leading
~451,400 samples every trial; only noise varies). Frame-effective
incoherent pilot over that exact span = 8.3748e-3 vs trim projection
basis 8.3688e-3: +0.003 dB. The trimmed capture presents 11.30 dB to
the detector as intended; running sweeps VALID. (Earlier "±0.4 dB
per-trial positional variation" concern retracted — trials share the
same clean segment.) Recommendation for any future regeneration:
discard the first ~120k samples at generation. §5.1 updated (rev13l);
per-block blue slot closed by measurement.

## Addendum: cell-resolved extracted-line classification (Dylan's reframe)

Ranked by snr_db with shipped-bank target-term DTFT response at each
offset: 18/19 line-bearing channels have dominant line IN the target
cell. ch33 is the unique blind-spot: only lines at -3606 Hz (21.0 dB,
guard, target response -16.7 dB) and -2843 Hz (13.1 dB, guard, -22.7).
ch24 +3121 Hz guard line: -31.8 dB response. ch31 minor guard line
(-2283 Hz, 6.5 dB, -10.4 dB) under on-target primary. Risk framing
(Dylan): strong co-channel on nominal pilot = maskable, exposure cost
only (ch24/ch30, conservative scenario); off-nominal pilot = detector-
blind DTV = the real hazard. Translator/LPTV tolerance "None specified"
in census; ch33 occupant is a translator. Full-depth integration cannot
date the guard carrier (current translator vs departed pre-repack
occupant) — epoch-split accumulation would. Re-centering documented as
possible-not-implemented. Appendix passage added (rev13m) + blue slot
asking Dylan to confirm ch33 = the a-priori off-nominal transmitter.
