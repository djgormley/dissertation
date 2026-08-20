# Tiering completeness scan + redshift translation — 2026-07-18 (rev15)

Trigger: writing the Dylan-ratified BAO redshift translation into 8.1
exposed two defects in the tiering paragraph as written into rev14.

## Defect 1: ch20 and ch22 omitted

The tiering accounted for 21 of 23 channels (8+5+4+1+1+2). ch20/ch22
belong to no named tier: nominal geometry, occupancy 0.924/0.929,
flat-quiet (overall hi-rates 1.09%/0.97%, endpoint quarters 0.2-1.7%),
but zero-point gaps -1.18e-3 / -1.35e-3 — just outside the eight's
+/-1.1e-3 envelope, formally ~40 sigma (err ~3e-5), no geometric
mechanism. Fixed: new sentence places them one notch behind the eight
(calibration rests on the measured table alone, not on agreement with
the analytic anchor). Count now 8+2+5+4+1+1+2 = 23.

## Defect 2: "flat ~1% across the 7.6 yr baseline" false for ch27, ch34

Quarterly re-derivation over ALL calibrated channels (all events + FRB
stratum, 40-frame floor; official script extension, see below):

- ch34 (full-depth, 37,474 frames): 3.4-8.3% every quarter 2018Q4-2020Q4,
  step to 1.8-2.2% through 2021, ~1% after (2022+ yearly means 0.7-1.6%).
  Step persists in the FRB stratum (2020Q4 6.2% -> 2021Q1 2.6%).
  Full-period high-tail 2.31% — under the 3% episodic criterion by
  dilution (long quiet majority). A FIFTH secular transition, below
  Fig-7's membership criterion.
- ch27 (capped): 2020Q3 = 38.0% all / 36.9% FRB (258/130 frames,
  67 units spread over Jul-Aug 2020 — not one bad capture); every
  2025-26 quarter <= 1.3%. Interior unsampled (cap). Endpoints-style
  loud interval, composition-robust.
- Completeness (verified programmatically): beyond these two, NO channel
  outside the episodic set (17,26,31,32,33,35) sustains >3% for
  consecutive quarters. Isolated single-quarter excursions exist
  (ch23 2026Q1 3.2%, ch29 2026Q2 4.3% FRB 0.7%, ch36 singles).
- 2026Q2 shows an all-events-elevated / FRB-flat pattern on several
  channels simultaneously (ch26 6.1/0.4, ch29 4.3/0.7, ch36 3.6/0.6,
  ch32 3.2/0.5, ch34 3.0/0.3): same signature as ch33's 2020Q4 rebound —
  a class-composition artifact of the newest quarter, NOT put in the
  text (transitions cited are all stratum-robust).

Text changes (rev15): 6.3 completeness paragraph (one further
transition + one loud interval + "no other" statement); Fig 7 caption
("quiet channels sit flat near 1 per cent" -> qualified); 8.1 tiering
("flat ~1%" claim replaced by six-with-no-sustained-excursion +
epoch qualification for ch27/ch34: first-adoption standing applies to
2021/2022-onward exposure, earlier archival data inherits the episodic
per-epoch treatment).

## Redshift translation (8.1, new paragraph)

z = nu21/nu - 1, nu21 = 1420.405751768 MHz (text quotes 1420.4).
Band 470-608 MHz: z 1.336-2.022 (dz 0.686). ch37 (608-614, protected)
z 1.313-1.336. First-adoption eight: 6-MHz slices from ch34
[1.383,1.407] to ch15 [1.947,1.984], summed dz 0.2515 ("0.25 of the
0.69"). ch20 [1.774,1.807], ch22 [1.711,1.742]. Refused: ch24
[1.650,1.680], ch30 [1.483,1.510]. Blind ch33 [1.407,1.432]. All
verified numerically in-session. Framing: untrusted channels subtract
narrow notches (dz ~0.02-0.03), never a contiguous redshift interval —
tiering costs depth, not reach.

## Repo reconciliation (Dylan's 224fed5 "fixing up figs")

Dylan pushed manual fig edits instead of applying delta19; delta19 is
DEAD (stale base). Reconciled state adopted:
- fig1: HIS version wholesale (equivalent to delta19's panel-b design,
  his layout tuning kept).
- fig2: his version + ch28-strip removal he ratified after this push
  ("still the same example and is redundant"); caption already matches
  (never-fires fact stated in caption, strip not drawn).
- fig3: his single-panel version was missing the ratified two-panel
  means/ncF-benchmark rebuild; merged = his base + panel (a) machinery
  (his xlim -60..-20, +/-1.5 kHz marks, dropped fixed-tau curves, GPU
  placeholder all preserved).
- delta14's data/provenance payloads never reached origin (his commit
  0160cd0 lacks them) — recarried.
- zero_point_study.py derived-criterion recode and survey_composition.py
  (never pushed at all) recarried.

delta20 = pilot-proxy-delta20-survey-scan-figs-on-224fed5.patch
(replaces delta19 entirely; apply on 224fed5; verified on pristine
worktree; syntax-checked). survey_composition.py extended with the
all-23 quarterly completeness scan -> survey_quarterly_rates_all23.csv
(243 rows, 21 calibrated channels; refused 24/30 excluded — no
calibrated zero point to rate against); existing outputs unchanged;
new CSV archived under data/provenance/survey_stratum_20260718/.
