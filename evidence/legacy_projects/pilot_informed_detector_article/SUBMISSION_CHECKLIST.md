# Submission checklist v5 — pilot-proxy paper (RASTI) — 2026-07-16 (post round-3 review)

R3 status: title retitled per R3 ("A pilot-informed F-statistic detector for
digital television in CHIME baseband data"); abstract/contributions synced
with the cautious body (rate language, 38–39%, eligibility, evidence
classes, frozen-not-preregistered); status quo now states the allocation-wide
DTV occupancy rule per 2511.19620 App. A; authors/affiliations/acks drafted
(NSF 2307581 + CANFAR/CADC + GBO + NRAO; ORCIDs + CHIME boilerplate + award
title pending); ch24/ch30 trust-flag terminology rewritten (see memo).

Build: `latexmk -pdf draft_article.tex` (compiles anywhere; now 20 pp).
Submission build: `main.tex` (MNRAS class family — swap in the RASTI class).
Appendices in `appendices.tex`, input after the bibliography in both builds.
Red slots = GPU-gated numbers. **Blue slots (`\needsdylan`) = 21 author-input
items; grep `needsdylan`.** Companion docs: `REVIEW_2026-07-16.md`,
`REFEREE_TRIAGE_2026-07-16.md` (R1), `REFEREE_TRIAGE_R2_2026-07-16.md` (R2,
includes the null-width erratum).

## -1. ERRATUM (R2, acknowledged)

v2's T2 framing contained a factor-of-ten transcription error (ideal null
width is 2.39×10⁻³ = 0.239 per cent, NOT 0.24×10⁻³). The measured on-sky
core width AGREES with the ideal independent-row width to 0.3%. There is no
effective-DOF slack; the input-correlation hypothesis is retracted. §5.2
corrected. Quoted dB values removed from abstract and conclusions until T2
closes.

## 0. MINIMUM GATE before the next referee-ready draft (R2 list, owners)

1. [x] **T2 CLOSED (2026-07-16, from the repo source).** Shelf SNR = shelf
       PSD over the full 6 MHz allocation vs noise PSD (dtv_units.py;
       spreading 32.94 dB, pilot −11.3 dB ⇒ C = 145.7 = +21.64 dB — the
       referee's reading A). The publication sweep runs
       `--num-input-streams 4 --frame-size-samples 16384` ⇒ **R = 512
       rows/trial**, not 262,144 (docs/PUBLICATION_VALIDATION.md §2). All
       four Fig. 3 crossings match the R=512 ideal prediction within
       0.4–0.5 dB (int4 quantization loss); the referee's "~13 dB
       inconsistency" = 10log10(√(262144/512)) = 13.55 dB exactly. The
       threshold rule = deployed rational threshold at the F-level of a
       −32 dB shelf. R5 label (agreed): "dimensionality and arithmetic
       closed; 512-row summary independently reproduced; physical SNR
       calibration and exact run provenance provisional." The paper's
       "single 41.94 ms frame" claim was the identified error. NEW (R5):
       audit reports pilot 11.9 dB below data vs the 11.3 dB constant —
       0.47 dB is the audit's flat-6-MHz extrapolation (RC ENBW
       5.381 MHz); ≲0.15 dB possibly genuine. [ ] Attach the sweep's
       atsc_waveform_audit.json, input-IQ hash, raw per-trial CSV, eval
       JSON, command/seed/backend, producing commit to provenance/;
       recalibrate or regenerate if a genuine deficit remains → **MEASURED
       (2026-07-16d): full-precision audit 11.918447 dB ⇒ genuine pilot
       deficit +0.146 dB; predicts +0.136 dB of the +0.27–0.32 dB
       residuals; remainder unattributed (full-precision control
       pending). Deployment-scale run must correct pilot amplitude or
       fold 11.446 dB into the axis.** [x] Provenance bundle received &
       verified: 45,000 raw trials re-aggregate to the summary exactly;
       hashes + commit included (shard eval JSONs absent; seeds in shard
       logs). [x] Delta patches pushed (aa8368d, 7d5ae68) — public fig3
       script verified in-session to reproduce the bundled figure
       (text-identical, CM Type 1 fonts).
       R6 refinements adopted: μ0-corrected benchmark (ch14 μ0 = 1.00206;
       predictions −32.09/−29.38/−33.04; residuals near-uniform
       +0.27/+0.30/+0.32), named the "ideal independent-Gaussian
       benchmark" (not the packed-int4 exact distribution); C convention
       defined (allocation-averaged; plateau convention would be 130.714);
       reviewer's no-deficit-assigned calibration paragraph adopted;
       Fig. 3 inset now one-decimal (delta2 patch to push). Provenance
       memos REWRITTEN clean (no correction banners). [ ] Raw 45k-trial
       CSV + eval JSON + command/seed/backend + IQ/weight hashes +
       producing commit + sweep audit JSON still wanted.
       UPDATE 2026-07-16b: fresh 1000-trial sweep received and verified —
       reproduces all archived crossings to 0.01 dB and the R=512 ideal
       prediction (0.662 vs 0.665 at −38 dB). Fig. 3 REGENERATED from it
       with LaTeX (CM Type 1) fonts and the "design benchmark" label;
       installed in the manuscript. Those matrix rows: [E] → regenerated
       at per-trial scale.
       REMAINING (repo): [ ] deployment-scale sweep (spec in
       SWEEP_VERIFICATION memo: --num-input-streams 2048, grid −52…−40 dB,
       or the {1,16,64,256}-stream scaling ladder + one 2048 point);
       [ ] −60 dB PFA/no-injection point (pos-excess rate should sit at
       ≈0.5); [ ] fitted crossing CIs in the inset — then headline numbers
       return to the abstract.
2. [ ] Real-baseband injection with unambiguous pilot/shelf convention +
       retention-probability calibration P(retained | ρ_shelf). — GPU Ph. 2.
3. [ ] Genuinely DTV-free, geometry-matched controls (add out-of-allocation
       channel to runbook). — Dylan + GPU Ph. 1a.
4. [ ] Matched comparison vs the ACTUAL CHIME DTV occupancy rule
       (emulate per 2511.19620 App. A; else rename comparator "simple
       radiometer") — **at a common cadence**: aggregate both detectors'
       decisions and compare retained clean exposure + residual
       contamination under identical injections, not false-mask rate
       alone. — Dylan reads App. A; GPU Ph. 2.
5. [ ] Held-out calibration/evaluation split + event/day block-bootstrap
       intervals; epoch/hardware stability; per-channel exposure columns;
       trigger composition. — Dylan, repo.
6. [ ] Simultaneity-controlled allocation-exposure calculation on the
       common stack, untrusted channels EXCLUDED (52.5 MHz is the
       internally consistent archive-weighted figure; 53.9 incl. untrusted
       is quoted for transparency only). — Dylan, repo.
7. [ ] Limited quantitative full-allocation expansion validation: exact
       pilot-channel→allocation mapping, expanded spectrogram, one
       representative full-band test. — Dylan, repo.
8. [ ] GPU parity + production-relevant throughput/latency. — GPU Ph. 1c+.
9. [ ] Remove/restore causal transmitter claims only with FCC/ISED records
       + telemetry cross-check of tail frames (packet loss, gain states).
       — Dylan.
10. [ ] Rewrite title/abstract/conclusions AFTER numbers are final; title
        decision (both reviewers favor detector-scoped; R2 suggestion in
        main.tex comment). — Dylan + me.

## 1. GPU slots (red boxes; unchanged, plus runbook amendments)

| slot | runbook phase | fills |
|---|---|---|
| Control certification | 1a | control-channel gap, mask fraction 0.45–0.55, kept excess ≤ Y dB (quoted §5.2 + §8.1). **Amendment suggested: add one out-of-allocation control** (current candidates 637/760/714 are pilot-free but in-allocation — external review is right) |
| CPU/GPU parity | 1c | max abs difference (0 expected), §5.1 |
| Injection–recovery | 2 | linearity + real-noise threshold agreement (§5.3); **also validates the §3.4 pilot→shelf conversion constant** |
| Radiometer baseline | 2 | sensitivity advantage X dB at P_d = 0.9 (§5.4). **Amendment suggested: run at matched false-mask rate emulating current-pipeline practice** (cf. arXiv:2511.19620) so the comparison answers the "vs current CHIME detector" objection |
| Provisional CPU floor | (no GPU) | floor_from_raw.py output — §5.2 provisional sentence fallback |

Submission decision rule (agreed v1): no submission with red slots; the
provisional path rescues slot 1a only.

## 2. Claim → evidence matrix (v5: evidence categories replace "final")

Categories: **[A]** independently recomputed arithmetic · **[S]**
synthetic/testbench results (regenerated 2026-07-16: fresh 1000-trial
sweep reproduces all archived crossings to 0.01 dB; CSV + T2/verification
memos in `provenance/`) · **[E]** archive-derived empirical, reproducible
from archived products but NOT yet regenerated or held-out validated
(provisional) · **[R]** gated on deployment-scale regeneration ·
**[GPU]** gated on GPU runs. Per R4: T2 is "calculation closed;
implementation provenance provisional" for anyone without the bundle —
hence `provenance/`; avoid categorical no-bug wording in the paper.

| claim | artifact | evidence |
|---|---|---|
| P50 −31.82 / P90 −29.08 dB (per-512-row trial) | fig3 + provenance/dtv_snr_summary.csv | [S]+[R]: regenerated at 1000 trials; crossings 0.2–0.5 dB above the Gaussian approximation (mechanism unattributed pending full-precision control); full frame −13.6 dB deeper in pos-excess sensitivity |
| Pos-excess (deployed) P90 −32.72 dB primary; fixed-τ backup mode P50/P90 −31.8/−29.1 at the recorded −32 dB reference level (testbench convention, demoted 2026-07-17 — see DECISIONS memo) | same | [S]+[R] |
| Capture loss +1.71/+1.70 vs sinc² +1.59 dB | same | prediction [A] (1.5923 dB); measured shifts [S], regenerated |
| Zero points: 16 nominal + 5-family + 2 refusals | empirical_zero_points.csv + fig | [E]; partition arithmetic [A]; **ch28 −3.6 vs −3.7: check CSV** |
| Core width 2.4×10⁻³ consistent with ideal 2.392×10⁻³ | §6.2 margins | ideal [A]; measured [E] (rounded, no uncertainty — "consistent with", not "0.3% agreement") |
| PFB prediction falsified | fig_pfb (App. A, embedded) | [E] |
| Estimator non-circularity (2 refusals; ch33 = 0.528) | zero-point study | [E]; ch24/ch30 physical attributions provisional |
| Tails common-mode (diagonal; ×3.5/×13 clustering) | fig_tail_decomposition | [E]; mechanism attribution open pending telemetry cross-check |
| Rate transitions ch33/32/35/17 | fig_secular_rates | [E]; "consistent with" until FCC/ISED corroboration |
| Seasonal residual ≤1.24× | fig_seasonal (App. A, embedded) | [E] |
| One-sided aggression fails | fig_aggressive_masking_tradeoff | [E] |
| Ladder 4.708→4.230→3.784→3.512 MHz | threearm_fulldepth.csv | rungs 1–2 [E] only; rungs 3–4 [A]-verified from Table 2 (whose inputs are themselves [E]) |
| **Deployment-default rung 3.418 MHz / 38.0% → 52.5 MHz eligibility projection** (53.9 incl. refused channels = diagnostic only) | derived | [A] from Table 2 [E] inputs; stack recompute + boundary accounting pending |
| Veto clips kept tail → ~+0.01 dB | fig_threearm_veto | [E]; +0.01 dB is by construction (veto threshold), not independent cleanliness evidence |
| Exact constants: 0/339,196, ≤2¹⁶, 9-bit headroom | empirical_thresholds.csv | [E]; headroom arithmetic [A] |
| Residual ≤ Y dB above pilot-free floor | control scan | **[GPU]** (session live; parity gate PASSED 2026-07-17) |
| Sensitivity advantage X dB at matched false-mask rate | injection ladder + comparator emulation | **[GPU]** |
| End-to-end cosmological safety | — | explicitly NOT claimed; future CHIME pipeline/overview update per arXiv:2511.19620 standard |

### R8 items (2026-07-17; triage memo in provenance/)

- [x] All R8 wording/preflight items applied in rev13: parity claim
      configuration-scoped + overflow/decisions reported + artifact gaps
      stated; int4-float bound now carries paired-bootstrap 95% CIs;
      audit wording convention-qualified ("extended audit", no "audit
      v2", placement claim fixed to 164-Hz resolution); reviewer's
      -0.38 dB projection stated; backup mode analytic-mu0-normalized
      per channel (1.31 dB spread verified); Appendix B heuristic
      naming + 219-event alignment explanation; 77,423 = channel-event
      records + unique counts; p.20 parity mention removed; Fig 3
      caption "Annotated"; FloatBarrier before section 7; appendix figs
      [t]; overfull fixed (0 remaining).
- [x] Operating-point recording RESOLVED 2026-07-17: Dylan confirms no
      timestamped record (early BAO-threshold idea abandoned informally
      in favour of positive excess — also the likely origin of the
      -32 dB constant). Downgrade applied at all 4 sites; §5.5 states
      the history; acceptance pair still open (blue slot).
- [x] Weight-bank hash received 2026-07-17 (b0dce17a…) — EXACT match to
      the notebook1 fig3-era hashes.sha256: CPU sweep and GPU parity used
      byte-identical banks. Commit 8f840b6 recorded.
- [x] Parity artifact committed + pushed 2026-07-17
      (data/provenance/parity_gpu_20260715seed, with .gitignore carve-out
      mirroring data/census). **Phase 1c fully closed by R8's own
      criterion** ("once the paired artifact is archived").
- [x] 1829-stack robustness run DONE 2026-07-17 (bundle received +
      verified; pipeline confirms 1829; aligned 1611/6890; stack
      tradeoff 3.53 vs 3.74 MHz composition effect; full-depth
      invariant). Appendix B carries the measured statement.
- [ ] Audit schema bump (v1 → v2 naming) + CPU-side integer columns +
      commit/weight-hash fields in eval schema — small repo patch,
      deferred until after the G3/G4 campaign to avoid mid-campaign
      version skew.

### R7 items (2026-07-17; triage memo in provenance/)

- [x] audit_v2 DONE 2026-07-17: direct field = 12.0239 dB -> genuine
      0.72 dB generator-level pilot deficit; RC inference (11.446)
      retracted. Archived as provenance/atsc_waveform_audit_v2.json.
- [x] delta4 applied + pushed (audit direct-integration fields + Fig 5
      relabels).
- [x] **Matched full-precision control DONE 2026-07-17** from the
      archived 45k trials: int4-float crossings differ -0.044/-0.018/
      -0.063 dB -> int4 exonerated; §5.1 quotes the measured
      decomposition.
- [ ] **Dylan:** correct the generator pilot amplitude (+0.72 dB) in
      generate-atsc, verify measured_pilot_below_data_direct_db =
      11.30 ± 0.05 with audit v2, THEN regenerate deployment-scale
      curves. (The running ladder is unaffected for its purpose — the
      1/sqrt(R) slope is common-mode in the axis offset — but absolute
      placements carry the +0.3 dB envelope until regeneration.)
- [ ] **Dylan:** operating-point decision documentation — when/why the
      three-arm thresholds and ch24/ch30 handling were chosen, plus the
      acceptance pair (max tolerable shelf level, allowed false-retention
      probability). Until then the text says "conservative scenario".
- [ ] **Dylan:** trigger/schedule composition of the 47.8% sample,
      per-channel exposure columns, and a common-strata robustness check
      (R7 survey-bias item; block bootstrap covers within-capture
      dependence only).
- [x] All R7 wording items applied in rev12 (scenario renaming, Fig 5
      metric rename + k=0 marker, selection-coupling caveats, cleanup
      list, abstract/conclusion edits, Type 3 font, float barriers) —
      see REFEREE_TRIAGE_R7_2026-07-17.md.
- [x] **−32 dB origin RESOLVED 2026-07-17 (author decision):** no
      derivation exists in any project material (original draft: uncited
      "science criterion"; "RadioFisher companion" was the assistant's
      unfounded inference, now removed from the text). Demoted to a
      recorded testbench convention; fixed-τ rule retained as a
      calibration-free BACKUP OPERATING MODE; the deployed
      positive-excess rule is the operational cleaning rule and primary
      characterization (§5 restructured, Fig. 3 repainted, captions
      updated; fig3_publication.py change goes in delta5). Blue slot
      remains only to cite a future science-derived level if one is
      established.
- [ ] **Dylan:** apply + push pilot-proxy delta5 (fig3_publication.py
      repaint: pos-excess primary, backup-mode labeling).

## 3. Dylan to supply / verify (updated)

- [ ] T2 (top of file).
- [x] 2511.19620 VERIFIED 2026-07-17 against the uploaded PDF: Appendix A
      occupancy rule confirmed verbatim (6 MHz bands from 398 MHz; >half
      bins over a lowered per-bin threshold matched in single-sample
      false-positive rate -> whole TV channel masked per time sample;
      omitted in the fringe-rate variant). 65.6% night-time masked
      (400-800 MHz, 94 nights, Table 1) and analysis band 608.2-707.8 MHz
      (z=1.01-1.34, 12.5 sigma) confirmed; NEW: analysis sub-band total
      38.7%, static mask 31.6% band-wide vs 3.5% in-band. Intro rewritten
      with verified figures; bib title already exact.
- [x] ch28 gap RESOLVED 2026-07-17: dumps give −3.65×10⁻³ → −3.6 as in Table 2 and the (already corrected) text.
- [ ] Fig. 7 channel identifications (ch33/32/35/17) + FCC/ISED corroboration.
- [ ] Pathological transmitters ↔ ch24/ch30 mapping (§2.2 blue slot).
- [ ] Untrusted channels: confirm "fully masked in deployment" default (§8.2, Table 2).
- [x] Which 8 channels at 100% depth RESOLVED 2026-07-17 from the archive
      inventory: ch24, ch30, ch31-36 (capped channels sit at 23-38% of
      their per-channel archives; ch29 extended to 3200 = 38.2%). Archive
      composition measured and in §6.1: 98.2% triggered / 1.8% scheduled;
      classified FRB 42.4%, Crab commissioning 19.9%, SGR 8.1%, pulsar
      ~20%. Remaining: per-channel sampled composition for capped
      channels + quarterly exposure columns + FRB-stratum robustness
      (needs the event-key dump).
- [ ] Stack-based exposure aggregate for §7's projection paragraph.
- [x] **Stack 1548 vs 1829 RESOLVED 2026-07-17 (corrected same day):**
      full pipeline regeneration on the complete staging reproduces 1548,
      falsifying the staging hypothesis; root cause is the recorded
      procedure's signature-seeded search family vs the unrestricted
      optimum (1829). Dylan chose **keep 1548, procedure-as-recorded**;
      §6.1 quotes 1548 + aligned 1329 events/5638 frames; Appendix B
      documents the not-adopted 1829 block and the non-monotone seeded
      table. Provenance: appendix_exact_by_k.csv (procedure),
      appendix_dropcurve.csv (registered greedy),
      appendix_unrestricted_by_k.csv, combine_subset_decision.json.
- [ ] Held-out calibration/validation split + block bootstrap plan (post-GPU; answers circularity objection).
- [ ] Confirm Metzger 2026 thesis (WVU ETD 13326) = "the Canary paper"; else supply citation.
- [ ] Hwang et al. 2013 author initials + pages (institutional access).
- [ ] Shelf-SNR and threshold-rule definitions (§5.1 blue slots).
- [ ] §5.5 ceiling-at-median rationale: confirm my drafted defense matches the pre-registered intent.
- [ ] CHKL-1 17.7 km path: confirm terrain-shielded trans-horizon.
- [x] 41.94 ms confirmed; the "~10 s frame level" phrase is PAPER_PLAN.md
      line 16 and is stale — update the plan doc, not the paper.
- [ ] plot_style.py font root cause found: `setup_matplotlib()` falls back
      to DejaVu Serif when Computer Modern/CMU system fonts are absent, and
      usetex is gated on PILOT_PROXY_USE_TEX=1 + latex + dvipng. For the
      publication regeneration pass: set PILOT_PROXY_USE_TEX=1 on a host
      with TeX (patch supplied adds newtxtext/newtxmath to the preamble to
      match the journal font), or install the CMU font package.
- [x] Census provenance closed via data/census/PROVENANCE.md: FCC LMS +
      ISED; 490 = on-air emitter-channel rows after 4 channel-share merges
      (494→490); detectability = modeled field strength, 43 rows. Remaining
      blue slots: retrieval date DONE 2026-07-17 (2026-06-09, from Dylan;
      mirror into repo PROVENANCE.md), propagation model, CHKL-1 terrain note,
      ch24 rogue-emission identification (absent from licensing data).
- [ ] Author list, affiliations, ORCIDs. Acknowledgements DONE
      2026-07-17: NSF in the group's house form (Directorate for
      Mathematical and Physical Sciences, Division of Astronomical
      Sciences, Award No. 2307581, per the ae0d86 template Dylan sent;
      generic disclaimer dropped to match house style, award title kept
      in this checklist for reference: "New Interference Detection,
      Mitigation, and Fusion Methodologies for Radio Astronomy");
      CHIME boilerplate adapted verbatim from 2511.19620 (DRAO/NRC +
      syilx Okanagan land acknowledgement + CFI/provinces/storage);
      GBO + NRAO standard facility lines added. Remaining blue slot:
      CHIME publication-policy confirmation (member-paper requirements)
      + exact current CADC/CANFAR standard lines.
- [ ] **CHIME internal publication approval — start the clock NOW** (external review concurs).
- [x] **GPU Phase 1c parity PASSED 2026-07-17**: max|GPU−CPU| = 0 over 200 same-seed trials, both comparison paths, identical detection decisions; §5 red box converted to measured text; run archived (provenance/parity_gpu_20260717.zip + GPU_PHASE1 memo).

## 4. Figure regeneration queue (repo work; captions already carry the intent)

- [x] **GLOBAL — LaTeX fonts. COMPLETE 2026-07-17** (all in-tree figure
      PDFs; pdffonts audit clean: embedded Type 1 CM/AMS only).
      Regenerated from the dumps via plot_style PILOT_PROXY_USE_TEX=1;
      fig_spectra_all23_* closed by the results bundle
      (transmitter_census/extracted_lines.csv); the one remaining DejaVu
      file, fig4_before_after_rules.pdf, was unreferenced by the
      manuscript and removed from figs/. Fixes applied to the repo (in
      02abdf6): amssymb fallback in the usetex preamble (newtxmath
      supplies AMS symbols when present), and conditional \% escaping —
      a bare % in a usetex label is a LaTeX comment and SILENTLY
      TRUNCATES the string (several axis labels had been losing their
      units). Original guidance below for reference:

      ```python
      import matplotlib as mpl
      mpl.rcParams.update({
          "text.usetex": True,
          "font.family": "serif",
          # match the submission build (mnras/rasti + newtxtext/newtxmath = Times):
          "text.latex.preamble": r"\usepackage{newtxtext,newtxmath}",
      })
      # fallback if usetex is unavailable on CANFAR nodes:
      # mpl.rcParams.update({"font.family": "serif",
      #     "font.serif": ["STIXGeneral"], "mathtext.fontset": "stix"})
      ```

- [ ] Fig. 1: define detectability axis + markers + census provenance; km units in-figure.
- [ ] Fig. 2: split conceptual geometry from edge/DC diagnostics (2 figures).
- [ ] Fig. 3: no-injection point; fitted crossings + CIs in inset; axis definition post-T2.
- [x] Fig. 4: DONE 2026-07-17 (dumps received): "analytic" unified in-figure
      and across the CSV chain (mu0_analytic); no-null-core arrows for
      ch24/ch30; per-event block-bootstrap errors on the gaps.
- [x] Fig. 5: DONE 2026-07-17: sweep extended to k=-1.5; ordinate relabelled
      "kept pilot-channel bandwidth"; contamination fraction defined in the
      caption (excess over Gaussian-H0 within the keep region; lower bound
      where signal-heavy). aggressive_masking.csv adds k=-1 columns.
- [x] Fig. 6: DONE 2026-07-17: panel (a) core as log-density + contours
      (core rides the same diagonal - stated in caption); panel (b) 68%
      per-event block-bootstrap bands + hourly denominator strip.
- [x] Fig. 7: DONE 2026-07-17: lines break across unsampled quarters
      (<=200-frame floor; <=500 aggregate); 68% per-event intervals;
      exposure strip (log). Channel-label confirmation still with Dylan.
- [x] Fig. 8: DONE 2026-07-17: 68% per-event block-bootstrap intervals on
      p99.9 (weighted-percentile unit resampling); twinx split into stacked
      panels; six-channel selection stated in caption (quiet 15/20/26,
      episodic 31/32, refused 24). threearm_fulldepth.csv adds CI columns.
- [ ] Optional (v1): survey gallery, carrier-offset case study Figs 10/11.

## 5. Release engineering (unchanged from v1)

- [ ] Tag pilot-proxy + datatrawl; Zenodo DOIs; DS001/UG001; CITATION.cff.
- [ ] Archive CSVs + per-frame dumps + results bundle.
- [ ] Data statement vs CHIME policy (§ Data Availability, now unnumbered endmatter).

## 6. RASTI mechanics (updated)

- [x] Keywords: RASTI scheme (Instrumentation — Data Methods — Algorithms — RFI — 21 cm intensity mapping).
- [x] Abstract ≤250 (now 245).
- [x] Data Availability as unnumbered endmatter; software cited per Force11.
- [x] Conclusions section; appendices after references.
- [ ] RASTI class file swap; single-column figure sizing pass.
- [ ] ORCIDs; cover letter (offer stands); data-availability/software-citation policy boxes.
- [ ] Title decision: current vs "Pilot-keyed recovery of DTV-allocated observing time…" (comment in main.tex).
