# Decision — fixed-threshold rule demoted (2026-07-17)

Trigger: Dylan asked where the −32 dB threshold came from. Traced: the
original draft called it "a fixed −32 dB science criterion" (uncited);
no derivation exists in any project material; "RadioFisher companion"
was the assistant's inference during early triage (name from the public
Bull et al. Fisher code) and has been removed from the text as
unfounded.

Decision (Dylan): demote, keep as BACKUP OPERATING MODE. The deployed
positive-excess rule is the operational cleaning rule and the primary
characterization (Fig. 3 solid; headline crossings). The fixed-τ rule is
presented as a calibration-free backup mode (no zero-point table needed;
usable pre-calibration or under health-check drift), evaluated at the
recorded −32 dB reference level, explicitly labeled a testbench
convention rather than a derived requirement. Ladder unaffected (both
rules' columns emitted per run; ladder figure anchors on pos-excess).
Repo change: fig3_publication.py repainted (delta5).

## Addendum: -32 dB origin, author confirmation

Dylan (2026-07-17): "I have no idea where the -32 dB came from which is
why I want to move away from it." Confirms no derivation exists; the
demotion to a recorded testbench convention / backup-mode reference
level is the final disposition.

## Operating-point recording — resolved (downgrade applied)

Dylan (2026-07-17): "A long time ago we were toying with the idea of
thresholds based on the BAO but ultimately decided to use the positive
excess." No timestamped record of the three-arm thresholds / ch24-ch30
policy exists; R8's conditional therefore resolves to the downgrade:
"recorded in the analysis plan" -> "retrospectively motivated" at all
four sites (abstract, contribution v, §5.5, conclusions), with §5.5 now
stating the informal history in one sentence. NOTE: the abandoned
"BAO-based thresholds" idea is the most plausible origin of the -32 dB
constant (matches the original draft's uncited "science criterion"
phrasing) — the -32 story and the operating-point story turn out to be
the same story. Acceptance-pair slot remains open.

## Stack robustness — measured (both blocks)

generate_results.py --stack-freq-ids <unrestricted 16> run 20260717T162658Z:
pipeline independently counts 1829 common events for the unrestricted
block; alignment keeps 1611 events / 6890 frames; stack H0 10/16; stack
tradeoff 3.528 MHz of 6.25 (vs 3.736 recorded block) — composition
effect (ch14 mask fraction 0.090 leaves the stack); full-depth 4.71 of
8.98 MHz invariant. Appendix B robustness slot replaced with the
measured statement; bundle archived as
results_bundle_chime-pilots_20260717T162658Z_stack1829.tar.gz.
Producing commit for the robustness run + parity era: 8f840b6 (pushed).

## Decision (2026-07-17, Dylan): uniform headline accounting

ch24/ch30 receive NO special treatment in the headline eligible-exposure
claim: primary figure = 3.512 MHz (39.1%), all 23 channels counted
uniformly (uncalibrated channels run the analytic-constant rule). The
R7-era "conservative scenario" (3.418 MHz / 38.0% / 52.5 MHz, ch24+ch30
excluded) is deliberately demoted to a stated sensitivity variant at all
seven sites (abstract, contribution v, §7 ladder, §8 projection, §8.1,
Table 2 caption, conclusions; deployment-path passage reworded). This
knowingly reverses the R7 hedge at author discretion; the certification
caveat is kept in-text ("retained frames on uncalibrated channels carry
no cleanliness certification until the Phase-2 measurements").
Allocation-wide primary: 0.391x138 ~ 53.9 MHz (52.5 conservative).

Same decision thread: ch24/ch30 de-dramatized in §2.2 (ordinary strong
co-channel emitters; "rogue offset emission" framing dropped; secondary
+522 Hz carrier noted as unresolved and operationally irrelevant); the
operationally distinct channel is ch33 (guard-parked carrier, Appendix
A). §2.2 triple blue slot, §5.2 ch24-identification slot, and the
rev13m appendix slot all closed.

## Decision (2026-07-17, Dylan): no scalar acceptance pair

The operating point is the parameter-free positive-excess rule; Pd(rho)
is fully determined by channel statistics + dimensionality and is
MEASURED (Phase-2 ladder), not chosen. The acceptance interface is the
retention curve P(retained|rho) itself; the paper deliberately declines
to adopt a scalar (L, p) commitment because (i) the rule has no free
threshold to engineer toward a requirement, and (ii) per §3.4 a
per-frame pair does not bound retained contamination without an
occupancy model. Floor (12e-3 mu0 = 5 measured core widths) and veto
(5 sigma_P) documented as recorded item-5 tradeoff-study conventions
with measured exposure costs. Both remaining acceptance-pair blue slots
(Table 2 caption, §8 deployment path) closed in rev13p. This answers
R7's operating-point-documentation request with a documented DECISION
rather than a pair of numbers.

## Channel confidence tiering (2026-07-18, Dylan-ratified)

Written into 8.1: first-adoption set = quiet nominal-geometry channels
15/16/18/19/23/27/29/34 (~3.1 MHz at ~50% kept); then geometric family
14/21/25/28/36 (measured-table dependence; ch14 crowded cell); episodic
26/31/32/35 (epoch-dependent; quarterly tables); ch17 (marginal, rising,
plausible future refusal); ch33 (diagnostics clean BECAUSE blind, -17 dB
to its measured occupant; kept frames uncertified pending epoch split);
refused 24/30. Universal caveat recorded: sub-width-crossing signal
retains at ~0.5 everywhere by construction -- the tiering ranks presence
probability, blindness, and calibration confidence, not immunity.
Analysis note: leak/kept >1% figures at the analytic threshold are
threshold-miscalibration artifacts (vanish at the measured ceiling);
the mirrored-core method cannot measure leak at tau=mu_hat (estimand
zero by construction) -- kept-data certification rests on G2 floor +
G4 retention curve.

## Tiering corrections + redshift translation (2026-07-18, rev15)

While writing the ratified BAO redshift translation into 8.1, the
completeness scan behind it falsified two rev14 tiering claims:
(1) ch20/ch22 were omitted from the 23-channel ordering (placed: one
notch behind the eight; -1.2/-1.4e-3 unattributed ~40-sigma shifts,
otherwise indistinguishable); (2) "flat ~1% across 7.6 yr" fails for
ch27 (38% sampled interval 2020Q3, FRB-robust) and ch34 (3-8%
2018-2020, step at 2021, FRB-robust, a fifth secular transition
diluted below Fig-7's 3% tail criterion). Text corrected in 6.3 +
Fig 7 caption + 8.1 (epoch-qualified first-adoption standing,
2021/2022-onward). Full detail: TIERING_COMPLETENESS_2026-07-18.md.
Scan archived as survey_quarterly_rates_all23.csv (script extension in
delta20, which also replaces stale delta19 after Dylan's 224fed5).
NOTE for Dylan: tiering remains 8-first-adoption BY STRUCTURE (his
ratified decision); demoting ch27/ch34 outright is his call if he
prefers — flagged in reply.

## Talk-through ratification (2026-07-18, Dylan)

Workflow: patches are now cut only AFTER discussion ("waiting for us to
talk through stuff before a patch") — talk-through, sign-off, then cut
against his current HEAD. Delta20 contents walked through explicitly;
both open calls decided: (1) Fig 2 ch28 strip REMOVED (his relabel in
224fed5 superseded; never-fires fact lives in the caption) — delta20
unchanged; (2) ch27/ch34 KEPT in first-adoption, epoch-qualified
(2021/2022-onward standing; pre-2021 archival inherits episodic
treatment) — rev15 8.1 text stands. Delta20 fully ratified for apply
on 224fed5.

## ch30 mixture-route test (2026-07-18, Dylan's proposal, measured)

Dylan: "there are two distributions so what if we just cut off the
higher one and build things based on the lower one." Measured
(analysis/ch30_offair_minority.py, byte-verified vs in-session run):
bimodal split is clean (96.3% at 11.7 x mu0; gap 1.5-10 empty at
0.26%; minority 3.46% = 314 frames). Minority = 38 WHOLE captures,
2019 Apr 6-25 + one Oct day, ZERO mixed units -> transmitter
silences, NOT fades (a 17.7 km path never fades into the gap).
Centre within 1.5e-3 of ANALYTIC mu0 -> refusal is
transmitter-caused, not instrumental (nice validation). But NOT a
calibration core: within-unit width 36.6e-3 = 15x trusted null width;
unit means +/-18e-3 rms BOTH directions (residual co-channel in
target AND reference cells when dominant is off); occupancy 0.47% vs
15% floor; f_null ~ 0.07 vs 0.20. Fails every ratified trust axis
except displacement. Operational payoff of adopting it anyway: 314
frames, all 2019 -> zero recovery in any later epoch. DECISION:
proposal declined as calibration, converted into the measured
mixture-route test in 5.2 (the estimator-scope caveat's hypothetical
is now a measurement that CONFIRMS the refusal) + refusals-bullet
cross-ref + new blue note to corroborate the 2019 Apr 6-25 off-air
window against ISED records (census candidate CHKL-1). Script staged
for delta21; CSV archived in survey_stratum_20260718/.

## Dissertation findings ledger started (2026-07-18, Dylan's request)

Living supplement (supplement/dissertation_supplement.tex, 5 pp)
collecting dissertation-grade nuggets the article compresses: ch30
dissection + census grounding (CHKL-1 Penticton 17.7 km, 79.3 dB, 25 dB
clear of runner-up; NOTE: Relay class carries +/-1 kHz in our census --
the no-tolerance class is translator/LPTV, i.e. ch33's story; ch30's
drift picket = discipline-in-practice, not rule-on-paper), ch24
contrast (no shape to cut; ALREADY FULL-DEPTH 1722/1722 -- the running
extension adds nothing; corrected Dylan's "more samples will help"),
T2 transient saga + block-profile figure, falsified PFB prototype,
criterion derivation, width-crossing universality, secular/repack
transitions + dilution lesson + composition-artifact signature, ch33
blind-spot taxonomy, spur family, survey join forensics, stack-subset
story, exact-integer thresholds, redshift tiering. Two new figures
(figS_ch30_two_population, figS_t2_block_profile). Grows per round.

## Notch audit + line-census verification (2026-07-18, Dylan's catches)

(1) Dylan flagged ch14 notch residue. AUDIT CONFIRMED and found worse:
fixed +/-3-bin pad leaves +2.3 dB (ch14), +4.4 dB / 11 bins (ch29,
7-bin-wide feature), +2.1 dB (ch34) shoulders; fs/3 pair clean. FIX:
adaptive notch in build_spectra_all23.py (grow to 0.5 dB of background,
max +/-15 bins, +3 pad) -> extents +/-8 / +/-13 / +/-9; re-audit NONE
>1 dB. Spectra variants regenerated; supplemental zip rev16a. Staged
for delta21 (with ch30_offair_minority.py). Article text unaffected
(no pad width stated; notching supplement-only).
(2) Off-nominal-line census cross-check (verify, don't assume): all 4
line-bearing channels (24/30/31/33) HAVE loose-tolerance census
candidates on-channel; no orphan lines. ch30 picket = 4 dwell lines
spanning both guards, nearest candidate CHKL-1 at 18 km (one wandering
carrier reading); ch33 nearest candidate 101 km -> attribution NOT
forced, epoch-split remains the discriminator.
(3) Ledger v2 (13 pp): tones section expanded (gallery figure,
three-leg excision justification, notch-width lesson), census
cross-check section added, full plot annex (3 fullspan variants, zoom,
excess/threshold, diurnal) embedded per Dylan's request.

## Kernel integration status of measured constants (2026-07-18, Dylan's Q)

Dylan asked whether the measured-mean comparator swap was ever actually
integrated into the kernel. VERIFIED IN CODE: NO. State of each layer:
- kernel.py exposes compute_numden_mask_rational_half(_checked):
  parameterized (num,den) u64 ceiling-sense compare + overflow counter.
  Parity (Phase 1c) exercised THIS path -- with testbench SNR-derived
  backup-tau constants (ch14, synthetic) only.
- build_empirical_thresholds.py builds App-C pairs as
  Fraction(mu_hat/2).limit_denominator(2^16) -- SAME half convention as
  the kernel entry point -> measured ceiling pairs are directly
  loadable, no conversion. The 0/339,196 verification was HOST-side;
  kernel never in that loop.
- Floor sense (mask_lo: pt*Q_lo < P_lo*pr) has NO kernel symbol --
  genuinely new kernel work; added to the Sec-8 "new, if small" list.
- Mean ESTIMATION stays offline by design (annual re-measurement ->
  constants table); kernel remains a dumb comparator (Dylan's reading
  confirmed).
Sec 8 deployment-path passage sharpened to state this plainly
(pre-empts the R9-class implemented-vs-specified gap). Proposed GPU
queue addition (after current blocks): rerun the parity spot check
with ch14's MEASURED pair from empirical_thresholds.csv -- one
constant changed in the existing harness -- to demonstrate the load
path end-to-end. Floor-sense symbol needs kernel-library source work
(kotekan side), out of patch scope here.

## Threshold-at-mean argument + three recorded options (2026-07-18)

Dylan asked for the argument for tau=mu_hat vs his advisor's
keep-left-tail-only suggestion. Derived and verified numerically
(Gaussian hazard exchange): 2-sigma-deeper cut = 22x exposure cost
(4.7x map noise at fixed survey time) for purity gains of 1.17x
(k=0.1), 1.62x (k=0.3), 5.4x (k=1) -- sub-width regime cannot be
tail-cut away; G2/G4/veto/occupancy are the linear-cost levers. Mean
uniquely selected by: no width calibration needed (width has no
assigned uncertainty); keep=1/2 symmetry powers the health check
(binomial sensitivity max at 0.5); parameter-free Pd=Phi(k) anchors
the validation chain (Phi(1)=0.84 = measured 0.833/0.841); purity
NON-monotonic in depth (reference-side contamination pushes F down --
measured on ch30 off-air scatter; band floor exists for this). Ledger
section + exchange-rate figure added (figS_threshold_exchange).
Dylan's over-engineering guardrail honored: slow-loop
self-calibration recorded as future option ONLY (one sentence in Sec 8
deployment path, per-channel, no cross-channel info); offset->Pd
exposition and ch33 re-centering noted alongside. No new machinery.

## ch24 time dissection (2026-07-18, Dylan's Q: trends like ch30?)

Measured: NO ch30-style structure. F confined to 0.93-1.3 x mu0
(0.2% above 1.3; nothing above 2), TWO-SIDED (26% of frames below
0.99 = >4 sigma under null -> reference-cell contamination measured;
empirical leg of the purity-non-monotonicity argument). Quarterly
medians 1.02-1.05 STATIONARY 2018Q4-2026Q2, no step, no repack
signature. Silences: 4 isolated quiet captures /1722 (scattered
single days = deep fades), vs ch30's 38-capture 3-week window.
Census: committee led by CHKL-DT+CHBC-DT share (62.8 km, 84.5 dB)
+ relay/translator members -- committees are never all off at once.
Genealogy note: CHKL-DT (ch24 share parent, Kelowna) is the parent of
CHKL-1 (ch30 Penticton relay) -- same family plausibly holds both
refused channels (candidate framing; ISED pending); parent shows no
interruption during relay's 2019-04 silence. Archive coverage holes
for ch24 (2021-2024Q2, 2025) noted as archive property. Ledger
updated with figS_ch24_vs_time + extended contrast paragraph.

## ch33 drift-oscillator hypothesis (2026-07-18, Dylan's recollection: fid 552)

Dylan recalls fid 552 (= ch33's pilot coarse channel; his first message
said 522, corrected) carrying a DRIFTING oscillator tracked 2019-2023.
Free cross-check from per-frame cells STRONGLY SUPPORTS cell-crossing
behavior in the loud era: quarterly LOW-tail rate (reference-cell
power -> F depressed) = 29% (2018Q4), 13-26% (2019Q4-2020Q4) vs
uniform 2.3-5.4% in 2022Q4+; hi-rate spikes 33-47% interleaved
(2019Q1, 2019Q4, 2020Q1, 2020Q4). Reading: a narrowband occupant
wandering across the lower reference (-6.1 kHz), guard, and target
cells through 2018-2020, settled in the guard by the trusted era. This
offers an ALTERNATIVE mechanism for the ch33 "repack-consistent"
rate collapse (oscillator walked out of the sensitive cells vs
occupant departed) and bears directly on the epoch-split question: a
drift track alive through 2023 would kill the "departed-occupant
ghost" reading. Article text NOT changed (candidate mechanisms;
decided by data). Targeted job prepared (36 events, 1/quarter +
3/quarter through the transition, largest units; 640 frames total):
ch33_drift_events.txt + _detail.csv + ch33_drift_spectra.py
(discover/unpack/FFT via pilot_proxy.chime API, batch-resumable,
CPU-only). Note: the RUNNING SCAN adds nothing here (fid 552 already
full-depth). Plotter to follow when spectra land. medPt secular
decline 2023->2026 (-1.2 dB) noted, unattributed.
