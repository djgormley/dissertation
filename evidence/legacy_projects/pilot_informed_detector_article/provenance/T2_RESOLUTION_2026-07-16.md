# T2 resolution — current state (rewritten 2026-07-16c, supersedes all earlier versions)

**Agreed status label:** dimensionality and arithmetic closed; ideal-benchmark calculations independently reproduced; aggregate 1000-trial crossings reproduced; physical waveform/SNR calibration open; exact run identity and provenance open; deployment-scale and real-data performance open.

## Closed components, with receipts

- **Shelf-SNR convention** — `src/pilot_proxy/dtv_units.py`: data-shelf PSD averaged over the full 6 MHz allocation relative to the noise-floor PSD in the same band ("not an SNR in the occupied ~5.38 MHz"). Spreading 32.936 dB; `PILOT_BELOW_DATA_DB = 11.3` (integrated pilot vs integrated data power); capture efficiency 1.0 ⇒ **C = 145.7475** against the allocation-averaged shelf density (against the interior-plateau density C would be 130.714).
- **Trial dimensionality** — `docs/PUBLICATION_VALIDATION.md` §2: `--frame-size-samples 16384 --num-input-streams 4` ⇒ **R = 512 rows/trial**; a full 2048-input frame is 10·log₁₀√(262144/512) = **13.546 dB** deeper in positive-excess sensitivity. The paper's earlier "single 41.94 ms frame" description of the curves was the identified error.
- **Threshold rule** — the deployed rational-threshold machinery evaluated at the −32 dB design benchmark (raw-F threshold via `snr_shelf_threshold_fields`).
- **Ideal benchmark** — exact noncentral-F (F ~ μ₀·ncF(1024, 2048, λ), λ = 1024·C·s), termed the *ideal independent-Gaussian benchmark* — a benchmark, not the exact distribution of the packed-int4 statistic. With the raw-F threshold measured against the channel-14 null centre μ₀ = 1.00206: predicted crossings −32.09, −29.38, −33.04 dB.
- **Regenerated sweep agreement** — the fresh 1000-trial summary (provenance/dtv_snr_summary.csv; 45 rows = 15 SNR × 3 offsets; num_input_streams = 4 in every row) reproduces the archived crossings at the reported precision (≈ −31.8, −29.1, −32.7 dB; one decimal — the hundredth-dB values are linear interpolations on a 1 dB grid, not measurements) and the −38 dB positive-excess rate exactly (0.662 vs 0.6611 predicted). Residuals vs the ideal benchmark: **+0.27, +0.30, +0.32 dB (near-uniform)**. No mechanism is assigned to these residuals; candidates include waveform pilot calibration (below) and quantization, and attribution requires a matched full-precision control.

## Components closed 2026-07-16d (provenance bundle received and verified)

- **Waveform/SNR calibration: MEASURED by direct integration (2026-07-17e).** The sweep capture's full-precision audit (`provenance/atsc_waveform_audit.json`): `measured_pilot_below_data_db = 11.918447`; pilot frequency error −0.44 Hz. Removing the 0.4728 dB flat-6-MHz convention offset (ideal raised-cosine shelf, ENBW 5.3811 MHz) implies an integrated pilot-to-data ratio of **11.446 dB — a genuine +0.146 dB pilot deficit** vs nominal 11.3. Propagated through the noise normalization this predicts a **+0.136 dB** crossing shift: correct sign, ≈half the observed +0.27/+0.30/+0.32 dB residuals; the remaining ≈+0.14–0.18 dB is unattributed (int4 quantization the leading candidate; matched full-precision control decides). R7 (2026-07-17) correctly notes the shelf estimator (interior median-Welch, extrapolated over 6 MHz) is not calibrated for bias: on a flat synthetic with known ratio it reads -0.39 dB low while the new direct-integration field is 0.001 dB accurate. audit_atsc_signal.py extended (delta4 patch); one rerun on the sweep capture yields measured_pilot_below_data_direct_db and settles the physical interpretation. Then: correct the generated pilot amplitude, or fold the calibrated ratio into the SNR-axis calibration.
- **Run identity/provenance: RECEIVED.** `provenance/run_pd_curves_cpu_1000.tar.gz` holds all 45 shards; 45,000 raw trial rows re-aggregated in-session and reproduce the merged summary **exactly (0 mismatches at 0 Hz)**; `num_input_streams = 4` and `detector-backend = cpu-reference` on every row. Hashes (capture + weights) and producing commit (7d5ae68) included. Gap: per-shard evaluation JSONs were not emitted by the shard wrapper — per-shard seeds/commands live in `shard.log`s.

## Still open

- **Deployment scale.** Deployment-dimensionality curves, or the {1, 16, 64, 256}-stream scaling ladder plus a full-frame spot check (predicted positive-excess P₉₀ ≈ −47 dB per frame under the ideal benchmark), plus the −60 dB PFA point.

## Public-repo reproduction status

Commit `aa8368d` carries the figure-pipeline fixes (kpsewhich-guarded newtx fallback, `\%` escape, "design benchmark" label, provisional watermark). Verified in-session: running `analysis/fig3_publication.py` at `aa8368d` with `PILOT_PROXY_USE_TEX=1` on `provenance/dtv_snr_summary.csv` regenerates the bundled Fig. 3 (identical extracted text; CM Type 1 fonts only). Host requirements: `latex`, `dvipng`, `ghostscript`, `cm-super`.

## 2026-07-17e — direct integration + full-precision control (both measured)

- **audit v2 (provenance/atsc_waveform_audit_v2.json):**
  measured_pilot_below_data_direct_db = 12.0239 — the sweep capture's
  pilot is a genuine 0.72 dB below nominal 11.3 by direct integration.
  Interior-shelf estimators bracket it (median 11.918, mean 12.375). The
  earlier ideal-RC inference (11.446 -> +0.146 -> +0.136 shift) is
  SUPERSEDED: the estimator's convention sensitivity (0.457 dB
  median-vs-mean; -0.39 dB median bias measured on a flat synthetic)
  exceeds the inferred effect.
- **Matched full-precision control — computed from the existing 45k-trial
  archive** (per-trial cpu_float_fstat_raw, same trials, same noise):
  float-weight crossings differ from int4 by -0.044 / -0.018 / -0.063 dB
  (threshold P50/P90, pos-excess P90). int4 quantization contributes
  <= 0.06 dB; the R4-era "int4 leading candidate" attribution is closed
  in the negative.
- **Budget:** naive propagation of the 0.72 dB deficit through the
  total-power normalization chain (composite correction -0.31 dB,
  6 MHz snr bandwidth) predicts +0.63-0.68 dB, overshooting the measured
  +0.27-0.32; pilot-window baseline (pilot sits on the RC rolloff) and
  band-edge conventions partially compensate. The paper now quotes the
  measured +0.27-0.32 dB as the end-to-end calibration envelope; the
  closure action is the generator pilot-amplitude correction (+0.72 dB)
  verified by audit v2's direct field, then deployment-scale
  regeneration.
- In-container chain probe (synthetic, direct ratio 11.34, 60 trials/pt,
  cpu-reference): threshold P50 lands ~0.5 dB left of the ideal
  benchmark with a shallower transition — consistent with
  convention-side effects independent of the GNU Radio waveform;
  indicative only (non-production waveform), archived for context.
