# Dissertation v4 versus old notes: preservation and integration review

Date reviewed: 2026-08-13

## Bottom line

Do **not** delete the old-notes archive wholesale yet. Four documents contain material that is not fully preserved in the current dissertation:

1. **`A_pilot_informed_F_statistic_DTV_detector_for_CHIME.pdf`** — the strongest controlled ATSC injection and paired floating-point/int4 comparison.
2. **`Pilot_Proxy_Findings_Ledger.pdf`** — a compact record of survey findings, rejected hypotheses, blind spots, and provenance pointers that are otherwise easy to lose.
3. **`dissertation_chapter04_sensitivity_latex_project.pdf`** — a well-structured synthetic-sensitivity chapter and artifact plan.
4. **`A_calibrated_ATSC_pilot_tone_F_ratio_detector_and_fixed_point_GPU_prototype_for_DTV_flagging.pdf`** — useful historical implementation evidence, provided its older architecture and different loss metric are clearly labeled.

The first item is exactly the idea remembered in the request: use a known, standards-chain ATSC signal as the reference; pass the same trials through a full-precision control and the packed fixed-point implementation; then measure the horizontal shift of the detection curve at a fixed operating point. That is worth keeping. The old numerical result should not simply be pasted into v4, because v4 now describes a different two-stage detector geometry and decision rule.

## What is already in dissertation v4

The present draft is substantially more mature than most of the older material. It already contains:

- a known-tone matched-filter/noncentral-F sensitivity model;
- the corrected complex-Gaussian factor of two;
- quantized weight norms and the exact rational zero-point correction;
- an exact-integer/bit-reproducibility contract;
- injected-pilot implementation gates and a signed-offset acceptance burst;
- a real weak-frame example showing the fine statistic finding a pilot missed by the coarse statistic;
- a measured-null calibration philosophy and a cosmological tolerance calculation.

Relevant source locations in the v4 archive are:

- [signed-offset independent injector](C:/Users/dylan/tmp/dissertation_notes_review/dissertation_v4/chapters/ch04_parameterization.tex#L120)
- [noncentral-F sensitivity model](C:/Users/dylan/tmp/dissertation_notes_review/dissertation_v4/chapters/ch05_pipeline.tex#L141)
- [real weak-frame example](C:/Users/dylan/tmp/dissertation_notes_review/dissertation_v4/chapters/ch05_pipeline.tex#L241)
- [exact-arithmetic scope and limits](C:/Users/dylan/tmp/dissertation_notes_review/dissertation_v4/chapters/ch06_implementation.tex#L7)
- [calibration chapter's currently one-line sensitivity requirement](C:/Users/dylan/tmp/dissertation_notes_review/dissertation_v4/chapters/ch08_calibration.tex#L59)
- [deployment acceptance burst](C:/Users/dylan/tmp/dissertation_notes_review/dissertation_v4/chapters/ch10_deployment.tex#L89)

What is missing is the bridge from those ingredients to a measured, auditable sensitivity/implementation-loss result.

## Highest-value recovery: controlled ATSC injection and fixed-point loss

### Strongest old result

Section 5.1 of `A_pilot_informed_F_statistic_DTV_detector_for_CHIME.pdf` (especially physical pages 5–6) records a good experiment:

- A standards-chain 8-VSB waveform was made with the GNU Radio ATSC transmitter chain: randomization, Reed–Solomon coding, interleaving, trellis coding, field sync, and root-raised-cosine shaping.
- The waveform was mixed with complex AWGN, passed through the four-tap sinc-Hamming reference PFB, quantized to offset-binary int4 at a declared clipping convention, and evaluated by the bit-exact CPU detector.
- The sweep used 1,000 trials per point over shelf SNR from about −38 to −24 dB and pilot offsets of −1, 0, and +1 kHz.
- Every archived trial carried both the full-precision statistic and the packed-int4 statistic. The crossings were therefore paired, not compared across independently generated sweeps.
- The measured int4-minus-float crossing shifts were −0.05, −0.02, and −0.06 dB, with paired-bootstrap 95% intervals of approximately [−0.12,+0.02], [−0.10,+0.05], and [−0.24,+0.12] dB. This disfavors quantization as the dominant loss term at that geometry, although the widest interval still permits about 0.24 dB.
- The ideal-versus-measured crossing offset was about +0.27 to +0.32 dB end to end.

The most important lesson is not the small number; it is the decomposition. The paired float/int4 result isolates implementation loss, while the ideal/measured offset contains waveform-model and normalization effects too.

The PDF is still visibly a working manuscript: it contains blue TODO annotations and says that deployment-dimensional regeneration is pending. Treat the quoted values as valuable internal evidence, not as a submission-ready result, until the archived trial products are recovered and the current-geometry rerun closes those TODOs.

### The generator audit is dissertation-quality material

The same work found that the supposed golden waveform was not stationary at startup. Its first 5.6 ms block was 9.7 dB below the steady pilot, the second block was 0.4 dB low, and later blocks were steady. After cropping to the stationary span and retrimming the pilot amplitude by about 0.9845, two independent estimators agreed to 0.007 dB; the steady pilot was 0.136 dB above nominal before that retrim.

This is an excellent negative-control story: a known injected signal is not automatically ground truth. The injector must be audited independently, the stationary span must be fixed before the sweep, and injection-calibration error must be reported separately from implementation loss. That point would strengthen the dissertation's recurring argument that arithmetic exactness does not validate the physical model.

### Why the old headline cannot be imported unchanged

The recorded sweep used 512 detector rows per trial, not the current full deployment dimensionality, and the paper explicitly treated full-frame sensitivity as an analytical scaling pending regeneration. V4 now has a two-stage architecture (`K=128`, `L=128`, padded fine transform), a designated-set fine statistic, empirical null calibration, and a threshold multiplier tied to the science operating point. The old experiment used an earlier decision geometry.

Therefore:

- preserve the old result as prior evidence and method development;
- do not present its crossing SNR as the final v4 detector sensitivity;
- rerun the paired float/int4 experiment through the current v4 pipeline before making a current quantitative claim;
- define implementation loss as a **horizontal SNR shift at fixed `P_D` and `P_FA`**, not merely a vertical residual in the statistic.

### Earlier prototype result: keep, but label carefully

`A_calibrated_ATSC_pilot_tone_F_ratio_detector_and_fixed_point_GPU_prototype_for_DTV_flagging.pdf` reports a different quantity and older implementation: 216.23 blocks/s, 29.02 GB/s packed input, about 14.1× below the stated real-time block-rate requirement, and a companion shelf-equivalent mean loss of −0.309 dB with maximum absolute loss about 0.59 dB over the tested range.

Those numbers do not directly contradict the later −0.02 to −0.06 dB crossing shifts. A statistic residual converted to shelf-equivalent loss and a detection-curve crossing shift are different metrics, measured on different prototypes. The later paired crossing experiment is the better sensitivity result; the earlier values belong in a historical/prototype paragraph or appendix, if used at all.

## Recommended dissertation addition

Add a short subsection at the end of Chapter 6 or as a calibration subsection in Chapter 8, tentatively titled **“Controlled ATSC Injection and Measured Implementation Loss.”** A clean version would contain:

1. **Reference signal contract.** Standards-chain waveform, shelf-SNR convention, pilot-to-shelf convention, sampling/PFB path, int4 scaling and clipping, frequency offsets, stationary-span rule, and independent normalization audit.
2. **Paired paths.** The same random waveform/noise realization evaluated by an ideal analytical prediction, a full-precision implementation, and the production fixed-point implementation.
3. **Operating-point metric.** `P_D(SNR)` at a declared empirical `P_FA`; report required-SNR crossings and paired-bootstrap intervals.
4. **Loss decomposition.** Separate generator/calibration error, model-versus-full-precision error, fixed-point-versus-full-precision loss, and frequency-offset mismatch.
5. **Current-geometry rerun.** Use the exact v4 weight bank, coarse/fine transforms, designated set, rank estimator, and threshold rational.
6. **Artifact chain.** Archive the detector configuration, seeds or trial identities, trial arrays, crossing table, bootstrap output, generator audit, and code revision. Figures should be treated as views of those products, not the evidence record itself.

The old sensitivity chapter supplies a useful structure: signal model, SNR convention, injection grid, `P_D` surfaces, ROC slices, required-SNR inversion, finite-trial support, accumulation scaling, offset penalty, stress axes, and an explicit artifact chain. Its representative −21.699 dB/bin result belongs to the old geometry and should be replaced, not copied.

## Other ideas worth retaining

### From the findings ledger

The following ideas are not fully captured in v4 and are worth preserving, even if only as future-work or validation notes:

- **“Separable but unusable null” versus “unseparable.”** A transmitter-off minority can show that the statistic separates populations while still leaving the on-sky null too broad for deployment calibration. This is more precise than calling a channel simply clean or contaminated.
- **Width-crossing sensitivity and retention are the same scale.** Expressing signal shift in null widths, `k=C s/σ`, exposes the point at which a positive-excess rule retains roughly half the contaminated frames by construction.
- **Why a deeper left-tail cut is a poor bargain.** Moving the threshold two null widths below the mean keeps only about 2.3% of clean data instead of 50%—roughly 22× less exposure—while buying modest purity for sub-width signals. Also, very low `F` can mean reference-cell contamination, so purity need not improve monotonically down the left tail.
- **The off-nominal blind spot.** Channel 33 was described as having strong carriers in a skipped guard near −3.6 kHz with about −17 dB detector response. A strong off-nominal pilot can therefore look “clean” inside the statistic. This is a sharper failure mode than ordinary sensitivity loss and deserves either a measured guard sweep or an explicit limitation.
- **Instrument-tone identification.** Clock-fraction coincidences, channel localization, and mask invariance form a defensible three-part identification test. A fixed ±3-bin notch left measured skirts; an adaptive notch grown until the spectrum returned within 0.5 dB of local background performed better.
- **Physical-invariant joins.** Matching day ±1 plus integer frame count linked archive units to inventory events far more cleanly than a day-only join. This is a compact, reusable survey-forensics method.
- **Exact rational thresholds.** The ledger records denominators bounded by `2^16`, approximation error below `10^-9`, zero disagreements over 339,196 frames, and a worst cross product of 55 bits. These are valuable deployment-scale exactness numbers if their underlying products are recovered and reconciled with v4.
- **Redshift tiering costs depth, not reach.** Protecting selected allocations removes slices across the redshift interval rather than moving the maximum redshift boundary.

Several ledger results refer to 23 channels, 77,423 events, and 339,196 frames, while the present v4 evidence matrix says only 10 channels are measured and 13 remain unmeasured. Those results should not be inserted until the source arrays/manifests are restored and the schema and detector version are reconciled.

### From the data-trawl tutorial

Chapter 7 already absorbs most of the tutorial's architecture. Two details could still help:

- use one stable unit key across inventory, completed product, and quarantine records;
- state failure semantics explicitly: fetch failure stays pending/retryable; probe failure is quarantined; mid-read failure aborts without a committed product; analyzer exception aborts without reclassifying the archive object; only the durable product is a commit.

### From the BAO article

The useful conceptual distinction is **achromatic time loss versus chromatic masking**. Flagged fraction alone prices exposure loss, but a frequency-dependent mask also changes the spectral window and can mix power along `k_parallel`. V4 already has a transfer-function placeholder and residual-template bank, so this belongs as a validation requirement rather than as imported old numerical forecasts.

## File-by-file disposition

| File | Recommendation | Reason |
|---|---|---|
| `A_calibrated_ATSC_pilot_tone_F_ratio_detector_and_fixed_point_GPU_prototype_for_DTV_flagging.pdf` | **Keep for provenance** | Earlier fixed-point prototype, throughput, residual, and historical loss metric. Superseded architecture. |
| `A_Hybrid_Technique_to_Increase_Throughput_of_the_Streaming_Spectrum_Sensor.pdf` | Archive separately | Prior low-resource spectrum-sensing work; not a needed dissertation section. |
| `A_pilot_informed_F_statistic_DTV_detector_for_CHIME.pdf` | **Must keep and adapt** | Best controlled injection, paired float/int4 crossings, generator audit, and explicit limitations. |
| `atsc_table.pdf` | Delete after checking authoritative source | Earlier tolerance summary is less nuanced and potentially misleading for translators/relays. |
| `bao_article.pdf` | Keep one copy for concept/provenance | Retain chromatic-mask/spectral-window idea; old numerical forecasts are superseded. |
| `bao_derivation.pdf` | Delete after preserving source if desired | Simplified radiometer/brightness-temperature calculation; present Fisher treatment is stronger. |
| `bao_snr_estimation_apj.pdf` | Delete | Two-page incomplete draft. |
| `bao_snr_estimation_apj__Copy_.pdf` | Delete if a canonical source exists | Older BAO-emergence draft; risks conflating detector cadence with cosmological aggregation. |
| `bao_snr_estimation_apj_v1__Copy_.pdf` | Delete if a canonical source exists | Duplicate/superseded forecast draft. |
| `bao_snr_estimation_apj_v1__Copy__2.pdf` | Keep only as the canonical BAO-SNR draft, if needed | Most complete of this draft family, but not for importing headline numbers. |
| `board.pdf` | Remove from research archive | Unrelated condominium/board material; handle as personal/private record. |
| `ccaaw_2021_final.pdf` | Archive as a publication | Prior CubeSat sensor work, not dissertation working material. |
| `cfar_bd.pdf` | Delete after source backup | Early sketch; current derivation/calibration is stronger. |
| `cfar_jai.pdf` | Preserve publication lineage only | Useful historical paper, but do not import broad UMPI/optimality language without a fresh proof audit. |
| `chime_doppler.pdf` | Keep for rationale only | Monte Carlo rationale for offset/guard choices; current work should use measured offsets and current geometry. |
| `circ.pdf` | Delete | Superseded one-page derivation. |
| `cyclic_modulation_spectrum.pdf` | Delete or merge into one future-work note | Alternate cyclostationary direction, not validated against current detector. |
| `cyclic_modulation_spectrum__Copy_.pdf` | Keep only if it is the canonical version | More complete alternate-detector note; possible factor-of-two convention needs recheck. |
| `datatrawl_tutorial.pdf` | Conditionally keep | Useful operational doctrine if the source/repository documentation is not preserved elsewhere. |
| `dissertation.pdf` | Delete after checking unique figures/data | Older incomplete draft with placeholders and unsupported claims. |
| `dissertation__Copy_.pdf` | Delete | Scaffold/template copy. |
| `dissertation_book_format.pdf` | Delete | Generic textbook-style draft with illustrative/superseded values. |
| `dissertation_chapter01_context_latex_project.pdf` | Delete after source backup | Main context and evidence-boundary ideas are absorbed in v4. |
| `dissertation_chapter02_detector_design_latex_project.pdf` | Delete after source backup | Older detector architecture; v4 is more exact and better scoped. |
| `dissertation_chapter03_null_calibration_latex_project.pdf` | Keep until null-Monte-Carlo artifacts are accounted for | Finite-tail support and 300k-trial validation concept may still be useful; geometry is old. |
| `dissertation_chapter04_sensitivity_latex_project.pdf` | **Must keep and adapt** | Best synthetic-sensitivity chapter outline and reproducible artifact plan. |
| `dissertation_template.pdf` | Delete | Template/scaffold. |
| `exploring_fo_so.pdf` | Delete or merge into future-work note | Superseded exploratory detector sketch. |
| `math.pdf` | Delete after source backup | One-page superseded calculation. |
| `msee_thesis.pdf` | Archive as a scholarly record | Prior thesis, not disposable working notes; only tangential detector lineage here. |
| `Pilot_Proxy_Findings_Ledger.pdf` | **Must keep in full** | Unique findings, failures, blind spots, provenance pointers, and unintegrated deployment-scale results. |
| `sf_fam.pdf` | Keep only as future-work provenance | Alternate cyclostationary algorithm; not part of the current evidence chain. |
| `tone_estimation_spl.pdf` | Keep as short theory/publication lineage | Helpful equivalence of matched filtering, off-grid DFT/Goertzel, and first cyclic mean; practical content is mostly absorbed by v4. |

## Before deleting anything

The four restored project archives now preserve the manuscript/chapter sources, generators, supplied figures, compact CSV/JSON/NPZ products, waveform-audit records, survey summaries, a producing commit, and a repository patch. They do not include every large canonical product referenced by the pilot-informed project's provenance notes: two CANFAR results bundles, the archived 45k-trial CPU sweep, and `all_spectra.npz` were explicitly held out for size. The generated waveform and weight-bank binaries are represented by hashes but are also absent. Locate those external artifacts if full regeneration is required.

The updated consolidated bundle keeps the four must-keep PDFs and the complete supplied contents of all four restored source projects.

## Packaging note

`dissertation_v4.zip` says it contains a compiled dissertation PDF, but no top-level `dissertation.pdf` was present. I compiled a review copy from the LaTeX sources in a scratch directory. The local MiKTeX installation lacked `multirow`, `pdflscape`, and `enumitem`, so the review build used temporary compatibility edits; the original ZIP was not modified. The substantive chapters and figures rendered cleanly, but this scratch build should not replace the author's canonical compiled PDF.
