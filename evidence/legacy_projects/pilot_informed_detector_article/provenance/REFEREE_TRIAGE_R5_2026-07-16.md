# R5 triage — calibration question investigated, ncF adopted, claim pass applied (rev8)

## The 11.9 vs 11.3 dB question: investigated and mostly decomposed

The reviewer's find is real (`examples/expected_output_snippet.txt`: `measured_pilot_below_data_db=11.9`), and the audit source explains most of it. `audit_atsc_signal.py` line 287 computes the denominator as `shelf_psd_median × 6 MHz` — a flat-shelf extrapolation across the whole allocation. But the generated waveform's RRC (β = 0.1152 on R_p = 5.381 MHz) gives a raised-cosine power spectrum whose equivalent bandwidth is exactly R_p = **5.3811 MHz** (as a Nyquist pulse must), so the flat extrapolation overstates true integrated data power by 10·log₁₀(6/5.3811) = **0.473 dB**. A physically correct 11.3 dB waveform therefore audits at **11.77 dB** under this metric; the reported one-decimal 11.9 leaves **≲0.15 dB possibly genuine** — which is exactly the right size to contribute to the +0.17/+0.24/+0.32 dB crossing residuals. Both the decomposition and the open remainder are now stated in §5.1, with the provenance ask as a blue slot: the sweep's own `atsc_waveform_audit.json` at full precision, the input-IQ hash, raw per-trial CSV, eval JSON, command/seed/backend, and producing commit into `provenance/`. If the full-precision audit shows a genuine deficit beyond the convention artifact, recalibrate or regenerate — Dylan's call once the JSON is in hand.

## Noncentral-F: verified exactly, adopted

Recomputed independently (scipy, F ~ ncF(1024, 2048, λ = 1024·C·s), C = 145.7475): predictions −31.984, −29.318, −33.040 dB and 0.6611 at −38 dB — matching the reviewer's numbers to the third decimal. §5.1 now uses the exact noncentral-F description in place of the Gaussian approximation, quotes measured crossings to one decimal with the interpolation caveat ("hundredth-dB precision is not claimed"), and gives the residuals as +0.17/+0.24/+0.32 dB with the calibration candidate named and the full-precision-control caveat retained.

## Their six substantive items — all applied

1. Abstract now says "candidate three-arm mask, frozen in the analysis plan" (consistent with §5.5); the p12/p13 contradiction is resolved — §5.5 no longer asserts low-tail frames are "genuinely contaminated," it cites the measured kept-data contamination rise (Fig. 5) with origin explicitly deferred to §6.2.
2. §8.1: "chosen with exactly that objective — its achieved cleanliness remains to be established"; selection bias "mitigated by construction … and will be quantified alongside the Phase-2 measurements."
3. §3.4 now states that detection rates alone cannot supply the occupancy model once decorrelation is admitted — simultaneous wideband (allocation-spanning) power information and an explicit decorrelation prior are required.
4. "Proposed deployment default" unified across abstract, §7 (both places), §8.1, §8.2, Table 2, conclusions.
5. The reviewer's exact epoch phrasing adopted everywhere the two-year claim lived: "sampled (detection) rates changed substantially between epochs separated by order-year intervals" — abstract, §6.3 body, Fig. 7 caption, conclusions.
6. Conclusions comparator re-synced with §5.4: common cadence, retained clean exposure, residual contamination under identical injections.

## Provenance-document hygiene

Both memos in `provenance/` now open with a boxed R5 revision notice retracting, explicitly: the "all four crossings 0.4–0.5 dB" sentence, the int4 attribution, the categorical "neither has a bug," and the "0.3% agreement" precision — replaced by the agreed label: **"dimensionality and arithmetic closed; 512-row summary independently reproduced; physical SNR calibration and exact run provenance provisional."** The checklist gate carries the same label and the new provenance-manifest item.

## Presentation status (unchanged blockers, on your side)

The public repo's `fig3_publication.py` still lacks the delta (benchmark label, `\%` escape, watermark, newtx fallback) — **push `pilot-proxy-delta-on-de193cb.patch`** so the public script reproduces the bundled figure. Figs 4/5/7 await the npz dumps (or a CANFAR run with `PILOT_PROXY_USE_TEX=1` after the delta lands); the mixed fonts and the stray Type 3 font disappear in that same regeneration pass. Blue slots: 27 (one added for the audit JSON), four GPU boxes, two bib TODOs — all data- or Dylan-gated, none textual.

Build: 22 pp, clean, abstract 246 words.
