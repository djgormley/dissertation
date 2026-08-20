# R10 triage (review of rev13p) — 2026-07-18

All checkable claims verified; applied in rev13s + delta14 unless noted.

## Decisions (Dylan, this round)
- HEADLINE RECONCILED via a new documented rule: a channel whose
  null-core calibration refuses (trust flags; no measurable pilot-free
  population) is RECOVERY-INELIGIBLE — detector runs and masks, output
  does not gate recovery, channel stays fully masked. Expected minority
  (2/23: ch24, ch30 — persistent transmitters, no quiet frames).
  Accounting split: 39.1%/3.512 MHz = the rule's MEASURED RETENTION
  (uniform over 23); 38.0%/3.418 MHz/52.5 MHz = DEPLOYMENT-ELIGIBLE
  (leads all eligibility claims incl. abstract + conclusions). Answers
  R10 item 1 with Dylan's own policy; closes the deployment-default
  blue slot. (Dylan initially kept 39.1 primary; the ineligibility rule
  he articulated implies 38.0 for eligibility — reconciliation adopted
  explicitly.)
- SWEEPS: current G3 block runs to completion (becomes a cross-check of
  the 0.003 dB effective-pilot argument); citable numbers come from the
  stationary-span protocol (G3b: crop -> retrim -> audit -> sweep), per
  R10's ordering (crop-after-trim would leave the stationary pilot
  ~0.6 dB strong — reviewer correct, matches our block profile).

## Contradictions fixed
- §5.5 vs §8.2 acceptance conflict: operating point now consistently
  "exploratory, evaluated against predetermined Phase-2 validation
  criteria"; ceiling parameter-free; floor/veto = tunable recorded
  conventions; retention curve = downstream interface. §5.5 slot now
  asks for predetermined validation criteria (not an acceptance pair).
- float/int4 sentence: reviewer's wording adopted (widest interval
  permits 0.24 dB = 75% of the residual; "under half" was false).
- §8 veto sentence: "F-independent" corrected (baseline frames selected
  via F core; deployed causal tracker would restore independence);
  "exact fixed-point compares" qualified (decisions exact; tracker
  cadence/scatter/warm-up/quantization unspecified).
- CI claim: public CI is CPU-only, CUDA test skips without device, one
  geometry when enabled; A100 artifact supports exactly its tested
  configuration.
- "pending the k<0 arm" removed (Fig 5 includes k<0).

## T2
- Quality-gate qualifier added (±2 dB pilot-level tolerance = no
  closure evidence).
- Stationary-span protocol written into §5.1 (replaces "just discard
  11 ms" — R10's ordering adopted with the 0.6 dB reason).
- trim_report staleness documented in the repo provenance README
  (gain_db 0.265 vs implied 0.530092; script fixed; report to be
  regenerated with the stationary retrim).
- 2x2 audits + block profile ARCHIVED: delta14 adds
  data/provenance/t2_convention_20260718/ (both fullspan audits, block
  profile, README listing what Dylan still adds: audit_v3.json,
  regenerated trim_report, stationary set).

## ch33 / sampling tempering
- "invisible"/"cannot key on" -> strongly attenuated / responds only
  weakly (−17 dB); mask fractions quoted (0.69/0.98 analytic) instead
  of "essentially always"; census tolerance = blank source field, not
  absent regulation; "reference cells clean" -> no persistent line
  above extraction threshold; floor bound marked prospective
  (Phase 1a pending).
- Stratification: 79%-assigned caveat + provisional-pending-archiving
  added in §6.3; survey_assignment_quality.csv (per-channel
  denominators) now produced by the script; ch17 drawn endpoints-only
  (no line across its coverage hole); all products archived in
  delta14's data/provenance/survey_stratum_20260718/.

## Presentation
- \FloatBarrier before §7 (fixes the pp.18–20 split) and before §4
  (Fig 2 containment).
- Reviewer note on stale supplement copies: outputs were already
  regenerated (extracted-spectral-lines title; action=
  notched_in_supplement_only) — rev13r/rev13s zips carry current
  versions.

## Still open (gates)
- G3 crossings (running) + G3b stationary rerun (protocol issued).
- Phase 1a controls, Phase 2 injection, matched comparator.
- GPU boxes, [gap]/[X]/[Y] slots, reference TODO (Metzger), draft
  banner: pending their artifacts/confirmations.

## Addendum: G3b stationary calibration executed (Dylan, 2026-07-18)

crop 600000->468928 (drop first 131072). Stationary-span projection on
the ORIGINAL capture: 11.1641 dB — the STEADY-STATE pilot is 0.136 dB
ABOVE nominal; the entire 0.53–0.72 dB "deficit" was the startup
transient diluting the full-capture mean. Retrim: amplitude x0.98447
(gain_db -0.1359: delta12 formula fix confirmed live) -> 11.300 exact.
audit_v4 (stationary trimmed, default 262144 span): direct 11.404,
shelf-extrapolated 11.411 — estimator agreement 0.007 dB (was 0.4+ dB
on the transient capture). PREDICTION MISS owned: predicted 11.33+/-
0.05, measured 11.404 (+0.07); attribution: audit span reads the
earlier/cooler portion of the stationary region (blocks 2-6.5 mean
9.59e-3 vs whole-span trim basis) + method bias; residual ~0.1 dB slow
drift remains inside the stationary span (harmless to sweeps: evaluator
consumes 96% of the cropped file; effective pilot = trim basis to
<0.02 dB). Consistency check: predicted stationary ratio from block
profile = 11.830-0.648 = 11.182 vs measured 11.164 (0.02 dB).
Manuscript updated (rev13t): §5.1 records the executed protocol and
the transient-dominated reframing; contribution (ii) now says
"startup transient that mimicked a 0.3–0.7 dB deficit".
Pending: stationary five-sweep block after the in-flight G3 completes;
audit_v4.json + trim_report_stationary.json into
data/provenance/t2_convention_20260718/.
