# Sweep verification (rewritten 2026-07-16c, supersedes earlier versions) + remaining runs

## What the 1000-trial sweep establishes

`provenance/dtv_snr_summary.csv` (45 rows: 15 SNR levels × 3 offsets; 1000 trials/row; `num_input_streams = 4` throughout ⇒ R = 512 rows/trial):

| Observable (0 Hz) | This sweep | Ideal independent-Gaussian benchmark (μ₀-corrected ncF) |
|---|---|---|
| Threshold rule P_d = 0.5 | ≈ −31.8 dB | −32.09 dB |
| Threshold rule P_d = 0.9 | ≈ −29.1 dB | −29.38 dB |
| Positive excess P_d = 0.9 | ≈ −32.7 dB | −33.04 dB |
| Positive excess at −38 dB | 0.662 | 0.6611 |
| Capture-loss shifts (±1 kHz, P50) | +1.71 / +1.70 dB | sinc² prediction +1.59 dB |

Crossing values are linear interpolations on a 1 dB grid (quote to one decimal; fitted uncertainties pending). The crossing residuals are near-uniform (+0.27, +0.30, +0.32 dB) and **unattributed**: candidates include waveform pilot calibration (see the T2 memo) and quantization; attribution requires the sweep's audit JSON and a matched full-precision control. Wilson intervals in the CSV exactly reproduce the standard formula. The bundled Fig. 3 was produced from this CSV via the public `fig3_publication.py` at commit `aa8368d` with `PILOT_PROXY_USE_TEX=1` (CM Type 1 fonts; extracted text identical to the bundled figure).

This validates the *synthetic per-trial* chain at R = 512. It does not establish deployment-scale performance, real-data behaviour, or physical SNR calibration — those are the open gates.

## Runs still wanted, in priority order

**1. Deployment-dimensionality sweep** (gate item):

```bash
pilot-proxy evaluate-snr --input-iq generated/atsc/atsc_8vsb_complex64.cfile \
  --physical-channel 14 --frame-size-samples 16384 --num-input-streams 2048 \
  --snr-start-db -52 --snr-stop-db -40 --snr-step-db 1 \
  --standard-frequency-offset-sweep --threshold-snr-shelf-db -32 \
  --noise-trials 300 --detector-backend cpu-reference \
  --output-dir results/pd_curves_deploy
```

Predicted positive-excess P₉₀ ≈ −46.8 dB (ideal benchmark). ~512× the per-trial compute of the 4-stream run; if painful, use option 2 with one 2048-stream spot check near −47 dB.

**2. Scaling ladder** (cheaper, arguably stronger): `--num-input-streams` ∈ {1, 16, 64, 256}, 0 Hz only, ~7-point grids centred on predicted P₉₀ of −30.2 / −36.2 / −39.2 / −42.3 dB respectively (each 4× in streams ⇒ −3.01 dB). A P₉₀-vs-R panel against the −5·log₁₀R line demonstrates the scaling law empirically and validates the full-frame extrapolation.

**3. PFA / no-injection point:** add `--requested-snr-shelf-db -60` to any run — positive-excess rate should sit at ≈0.5 (the null acceptance check); a true zero-injection mode is a ~5-line testbench addition if preferred.

**Also wanted for the provenance bundle** (not sweeps): raw per-trial CSV (45,000 rows), evaluation JSON, exact command/seed/backend, input-IQ + weight-bank hashes, producing commit, and the sweep's full-precision `atsc_waveform_audit.json`.

**Not sweeps, still open:** GPU Phase 1a/1c (control scan incl. one out-of-allocation channel; same-seed parity), Phase 2 (real-baseband injection ladder; common-cadence comparator emulation reporting retained clean exposure + residual contamination under identical injections), held-out split, Figs 4/5/7 regeneration (fonts inherit automatically via `plot_style` at `aa8368d`).
