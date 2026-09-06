# Stub checklist — what still has to land before the dissertation is finished

Every `\stub{}` / `\stubfig{}` / `\stubtab{}` in the LaTeX renders as a red box in the PDF; each one is listed here under the campaign that fills it, in document order.
Every `\rerun{...}` is a number (or a status) quoted from the superseded v3/v4 products that is expected to move when the v5 rerun lands, or a value to confirm before use; it renders in blue.
When a campaign is in: replace its stubs, re-verify its `\rerun{}` values, then set `\reruncolor` to `black` in `dissertation.tex` (or `grep -n '\\rerun{' chapters/*.tex` and strip the wrappers).

Totals: **38 stubs**, **175 rerun markers**.

## v5 archive rerun and Pathfinder shadow run (1 stub)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `dissertation.tex:172` | stub |  | Two or three sentences with the headline results: how many of the 23 channels admit a tolerance-selected operating point, how many are excision candidates, the band-level integration-time cost of the selected masks, and the outcome of the Pathfinder shadow run (hours run, frames dropped, exact-replay agreement). |

## before submission (1 stub)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `dissertation.tex:210` | stub |  | Name every funding source with its award identifier (the NSF award requires its exact acknowledgment text); the ETD office and the sponsors both expect the identifiers. |

## `dtv-census` export (1 stub)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `chapters/ch03_broadcast.tex:185` | stubtab | `tab:census` | One row per physical channel 14–36: envelope records, primary/secondary split, licence-matched count, nearest licence-matched facility and its range and bearing, and the licensed ERP of the strongest matched facility. Generated from the frozen `dtv-census` export that also feeds Figure [fig:census:map]; the export's digest is recorded in the release manifest. |

## v5 archive rerun (25 stubs)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `chapters/ch03_broadcast.tex:198` | stub |  | Regenerate as one 23-panel figure (channels 14–36 in physical-channel order) from the current-era averaged spectra; the panels shown here and in Figure [fig:census:psd:lower] are the superseded archive-average exports for channels 27–36 and 14–26. |
| 2 | `chapters/ch05_pipeline.tex:233` | stub |  | Replace the previous sentence with the current-era null centres and widths from Table [tab:calibration:nulls]: per channel, the measured $F/\mu_0$ centre against $\mu_0$, the coarse and fine width factors against the i.i.d. model, and the fraction of channels within $0.1$ dB of prediction. |
| 3 | `chapters/ch05_pipeline.tex:236` | stub |  | Blocked-evaluation table: per channel, calibration-block and evaluation-block null centre and width, drift between blocks, finite-estimate rate, and block-bootstrap intervals. |
| 4 | `chapters/ch06_implementation.tex:261` | stub |  | Cross-build comparison record: the two build manifests, the joined event/frame denominator and completeness, and the mismatch count (expected zero) over the compared integer fields. |
| 5 | `chapters/ch06_implementation.tex:344` | stub |  | Held-out summary table: per channel, calibration-block $(\rho^\star,\eta^\star)$, evaluation-block masked fraction and retained residual, $r_{\rm sys}/r_{\rm tol}$, empirical $P_{\rm fa}$ where an off state exists, and block-bootstrap intervals. |
| 6 | `chapters/ch06_implementation.tex:358` | stub |  | Regenerate from the v5 product for the same two frames, and replace the illustrative boundary with the channel's selected $\eta^\star T_{(\rho^\star)}$. |
| 7 | `chapters/ch07_survey.tex:53` | stub |  | Archive accounting paragraph with the v5 numbers: events enumerated, excluded (outrigger), targeted, and completed; quarantined units; unique inventory objects; product units; stored and valid detector frames; calendar span; per-channel event-count range; median frames per acquisition. Every number in it comes from the release ledger via the number gate, not from prose. |
| 8 | `chapters/ch08_calibration.tex:114` | stubtab | `tab:calibration:eras` | One row per channel 14–36: current-era start and end (UTC month) with boundary uncertainty; the transition evidence that defines the start (sign-on, sign-off, station change, instrument change, or archive start) and its agreement with any station or instrument record; a stale-latest flag where the era ends before the snapshot; earlier eras listed for provenance; current-era valid-frame count; and current-era calendar coverage (months with frames / months spanned). |
| 9 | `chapters/ch08_calibration.tex:170` | stubtab | `tab:calibration:anchors` | One row per channel: current-era anchor $\widehat f_a$ (fine bin and Hz from synthesis) with its estimator (on-minus-off or fallback median) and block-bootstrap uncertainty; the dominant lobe of the current-era averaged spectrum (Hz from synthesis, dB over median); the per-frame peak-offset distribution (median, 90th and 99th percentiles, from the retained fine spectra rather than the average); for $K = 64$, $128$, and $256$, the fraction of frames and of pilot-associated energy inside the span, the straddle loss at the measured anchor, the margin to the span edge, and any reference-region contamination (these come from the retained per-frame $23.8$ Hz power spectra, which cover all three spans; they are a spectral containment analysis, not a rerun of the detector at the other two tap lengths, which the products cannot supply); the disposition (supported, supported with sentinel, unsupported); and, for channels with more than one era, the anchor of the previous era. |
| 10 | `chapters/ch08_calibration.tex:268` | stubtab | `tab:calibration:nulls` | One row per channel: current-era frame count and null-bulk count; the null source (off era, quiet subset, reference surrogate, model-only, or refused) and, for a bulk-read null, the declared mixture assumption; coarse null centre ($F/\mu_0$) against $\mu_0$ and its left-side scale; coarse and fine width factors, raw and robust-core; tail fraction beyond three core widths; fine-axis exchangeability rate at the selected rank against the combinatorial prediction; kept-frame or off-era floor in dB with its population; and the histogram plate reference in Appendix [app:archive-diagnostics]. |
| 11 | `chapters/ch09_tolerance.tex:125` | stub |  | Regenerate without the historical annotations; mark the band-level masked fraction at the bootstrap rule and at the selected per-channel operating points. |
| 12 | `chapters/ch09_tolerance.tex:262` | stub |  | Extend to all 23 channels on their current eras, adding a fourth row for the pilot proxy at the selected $(\rho^\star,\eta^\star)$. |
| 13 | `chapters/ch09_tolerance.tex:486` | stub |  | Replace the channel-33 example numbers with the current-era values from Table [tab:tolerance:channels], and state the across-channel range of the pilot-proxy-over-best-alternative ratio. |
| 14 | `chapters/ch09_tolerance.tex:492` | stub |  | Regenerate for the same channel on its current era at the selected $(\rho^\star,\eta^\star)$, adding that point beside the bootstrap-rule point. |
| 15 | `chapters/ch09_tolerance.tex:571` | stubtab | `tab:tolerance:eta` | One row per channel 14–36: current era; $|\mathcal B|$; selected rank $\rho^\star$ (and normalized rank $q_\rho$) and multiplier $\eta^\star$ (display value and exact $\eta^\star_{q16}$); masked fraction $f$ at that point; kept-frame floor (dB) and its population; $r_{\rm proxy}$; the operable-tier tolerance $r_{\rm tol}$ of the channel's bin and the margin $r_{\rm tol}/r_{\rm sys}$; cost $\mathcal C$ of Eq. [eq:tolerance:teff]; plateau width; and the selector's status (feasible, occupancy-wall, no feasible point, refused with reason). Channels whose $\tau_c$ is refused carry bounds, marked as such. |
| 16 | `chapters/ch09_tolerance.tex:579` | stub |  | Regenerate on the fine axis from the current-era histogram families: one curve per channel at its selected $\rho^\star$, the selected $\eta^\star$ marked on each, and the bootstrap-rule point shown for reference. The figure shown is the coarse-rule version from the superseded products. |
| 17 | `chapters/ch09_tolerance.tex:602` | stub |  | Regenerate for all 23 channels at their selected $(\rho^\star,\eta^\star)$, one row per channel, four worlds per row, with the dilation margins in a companion table. |
| 18 | `chapters/ch09_tolerance.tex:619` | stubtab | `tab:tolerance:channels` | One column per channel 14–36 (as a sideways table, or two half-band tables of the same construction), rows: allocation (MHz); redshift span; monitored bin (MHz); current era; masked fraction at the bootstrap rule and at $(\rho^\star,\eta^\star)$; on-air shelf (dB); null frames; kept-frame floor (dB); intra-day share; ground filter (dB); $\tau_c$ outcome; $r_{\rm keep}$; $r_{\rm proxy}$ at the selected point; $r_{\rm proxy}/r_{\rm tol}$ on the dilation tier and on $f\sigma_8$; and the screening class (recovery candidate, measurement-bound, occupancy-wall excision candidate, or off-era). |
| 19 | `chapters/ch09_tolerance.tex:622` | stub |  | Two or three paragraphs walking the table: which channels admit a recovery candidate on the dilation tier at their selected point, which are measurement-bound and on what (floor or $\tau_c$), which are occupancy-wall excision candidates, and which are evaluated on an off era; name the best-constrained channel and the channel whose verdict hangs most completely on a pending measurement. |
| 20 | `chapters/ch09_tolerance.tex:635` | stub |  | The disposition itself: the list of excised allocations with their discarded `freq_id` ranges, the retained pilot taps, the kept/discarded channel counts (previously 273/81 on the superseded products), and the per-allocation cost of the inclusive keeps priced at the coherence cap. |
| 21 | `chapters/ch11_conclusions.tex:27` | stubfig | `fig:conclusions:status` | One cell per channel 14–36 with its current-era screening class from Table [tab:tolerance:channels] (recovery candidate, measurement-bound on floor, measurement-bound on $\tau_c$, occupancy-wall excision candidate, off-era) and the closing measurement that controls it; the superseded archive-average map was removed rather than shown under a current-evidence heading. |
| 22 | `chapters/ch11_conclusions.tex:74` | stubtab | `tab:conclusions:matrix` | One row per channel 14–36: current-era screening class from Table [tab:tolerance:channels]; selected $(\rho^\star,\eta^\star)$ and masked fraction from Table [tab:tolerance:eta]; the handover policy status (kept-and-masked, excised interior, monitoring tap); and the binding evidence or closing condition (measured floor and its population, $\tau_c$ outcome, era transition, or transfer gate). |
| 23 | `chapters/ch11_conclusions.tex:82` | stub |  | One paragraph stating the band-level result: the number of recovery candidates, measurement-bound channels, excision candidates, and off-era channels; the integration-time cost of the selected masks on the kept allocations; and the one or two channels whose verdicts are most sensitive to a pending measurement. |
| 24 | `chapters/appC_archive_diagnostics.tex:68` | stubtab | `tab:archive:atlas-counts` | Per channel: `freq_id`; valid frames in the archive; frames excluded by reason; current era and its valid-frame count; frames kept by the selected $(\rho^\star,\eta^\star)$; and the plate's file digest. |
| 25 | `chapters/appC_archive_diagnostics.tex:74` | stub |  | Regenerate all 23 plates from the v5 products with the layers described above. The plates that follow are the superseded health-filtered versions: their upper panels show archive-wide (not current-era) histograms without the null-bulk overlay, their middle panels show the bootstrap coarse mask rather than the selected fine pair, and their lower panels mark quarterly anchors rather than the era boundary. They are retained so the reader can see the construction and the calendar coverage of every channel. |

## synthetic estimation rerun (1 stub)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `chapters/ch05_pipeline.tex:221` | stub |  | Repeat both sweeps at the production protocol and add the $g$ reconciliation of Section [sec:estimator:translation]: the waveform's spectral density at the reference bins relative to its flat top, the clean-waveform target-to-reference ratio, and the fitted saturation level, with the nominal value $1/2$ and the recorded $\approx 1$ both shown; replace Figures [fig:estimator:digital-transfer] and[fig:estimator:ota-transfer] and the fit coefficients quoted in the text. |

## Pathfinder shadow run (5 stubs)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `chapters/ch05_pipeline.tex:244` | stub |  | Live estimation summary: run duration and frame count per channel; fraction of frames with finite estimates; time-block stability of $F/\mu_0$ and inferred shelf SNR; exact-replay agreement count on sampled frames; dropped and late frames; kernel and stage runtime quantiles. |
| 2 | `chapters/ch06_implementation.tex:370` | stub |  | Live detection results: hours run and frames per channel; mask fraction timeline; before/after frame-averaged spectra per monitored channel (Section [sec:deployment:results]); tripwire and validity counts; exact-replay agreement on sampled frames; latency percentiles under load. |
| 3 | `chapters/ch10_deployment.tex:239` | stub |  | Full-load numbers: per-frame stage latency percentiles (50/90/99/max) on the Pathfinder GPU, deadline misses, memory headroom, and the kernel-only time on that GPU for the $N=8192$ profile. |
| 4 | `chapters/ch10_deployment.tex:298` | stubfig | `fig:deployment:spectra` | Per monitored channel: the run's frame-averaged power spectrum of all frames and of kept frames around the pilot, on the same axes as the archive plates; a panel of mask fraction versus time over the run. |
| 5 | `chapters/ch10_deployment.tex:304` | stubtab | `tab:deployment:results` | Per channel: run duration, frames processed, dropped, late; validity counts by reason; tripwire firings; exact-replay frames compared and mismatches; latency percentiles; mask fraction and its range over time blocks; state changes observed and the stage's response. |

## LimeSDR detection campaign (4 stubs)

| # | Where | Kind | Label | What goes there |
|---|---|---|---|---|
| 1 | `chapters/ch06_implementation.tex:319` | stubfig | `fig:detection:mscaling` | Measured null width (raw and robust core) and deflection of the fine and coarse statistics versus $M$ from $1$ to $2048$, on log axes, against the $1/\sqrt{\beta M}$ and $\sqrt{M}$ predictions, with the fully correlated bracket drawn as the upper bound on width. |
| 2 | `chapters/ch06_implementation.tex:321` | stubtab | `tab:detection:loss` | Paired implementation loss at the production geometry: horizontal crossing shift (packed minus full-precision) at fixed-threshold $P_d = 0.5$ and $0.9$ and at the positive-excess $P_d = 0.9$ crossing, for each pilot offset, with paired-bootstrap 95% intervals; the transform-only figure of $-0.0026$ dB from Section [sec:impl:fxfft] as the lower bound; and the same-seed CPU/GPU equality count. |
| 3 | `chapters/ch06_implementation.tex:323` | stubfig | `fig:detection:finegain` | Fine versus coarse detection: $P_d$ at fixed null $P_{\rm fa}$ against shelf SNR for both statistics at $M = 2048$, with the measured gain of the fine axis compared with the $10\log_{10}\sqrt{L} \approx 10.5$ dB bound of Section [sec:pipeline:coherent]. |
| 4 | `chapters/ch06_implementation.tex:325` | stubfig | `fig:detection:frontier` | The mask-versus-residual frontier of Eq. [eq:detection:frontier] from synthetic truth: one unsmoothed curve per rank $\rho$ in the (surviving injected contamination, masked fraction) plane, with $\eta$ labelling points along each curve, at two or three duty cycles, with trial-bootstrap intervals; a second panel comparing the residual the histogram cumulative sums claim with the residual actually injected into the kept frames; the before-and-after averaged spectra at one loud and one sub-noise shelf as a third panel. |

## `\rerun{}` markers per file

| File | Count |
|---|---|
| `dissertation.tex` | 1 |
| `chapters/ch01_introduction.tex` | 11 |
| `chapters/ch03_broadcast.tex` | 9 |
| `chapters/ch04_parameterization.tex` | 2 |
| `chapters/ch05_pipeline.tex` | 5 |
| `chapters/ch06_implementation.tex` | 26 |
| `chapters/ch07_survey.tex` | 5 |
| `chapters/ch08_calibration.tex` | 12 |
| `chapters/ch09_tolerance.tex` | 83 |
| `chapters/ch10_deployment.tex` | 11 |
| `chapters/appA_evidence_matrix.tex` | 1 |
| `chapters/appB_legacy_evidence.tex` | 2 |
| `chapters/appD_software.tex` | 6 |
| `chapters/bibliography.tex` | 1 |

## Values to set before a campaign runs (blue in the PDF)

- Table 10.3 shadow-run acceptance criteria: duration, frames, replay sample size, loss limit, latency fraction, invalid-rate halt — proposed values are placeholders until you set them.
- §8.1 era procedure policy values: 30 frames / 5 acquisitions / 3 days per month; 1 dB / 0.5 dB on/off medians; 3-bin anchor step; 2-month persistence — recorded with sensitivity values, confirm before the rerun.
- Table 10.1 merge status of the kotekan stage.

## Open correctness question (settle with data, not argument)

**Where does the pilot sit on the transmitted RRC skirt, and what shelf density do the reference bins see?** Theory (A/53 Part 2 Fig. 5.11: 0.707 amplitude at the pilot; the generator's own RRC design puts the carrier at its −3 dB point; a numpy re-creation of the generator chain gives 0.48/0.54 × flat-top at ∓6.1 kHz) says g ≈ ½ and the transfer should saturate ~3 dB *above* the flat-shelf benchmark. The recorded 2026-08-25 digital sweep saturates 0.12 dB *below* it (fit coefficient b = 1.106; clean-waveform target/reference ratio 124 ≈ A). Candidates: the generated waveform's density near the pilot is not what its filter implies, or the target captures ~2.5 dB less pilot than nominal. §5.1.6 now states g as a measured parameter with both numbers; the rerun measures g two independent ways (waveform PSD at ±6.1 kHz vs flat top; clean-waveform target/reference ratio) and must reconcile them with the fitted saturation. Do not quote either value as settled until then.

## From the figures-and-tables review (applied)

- Conventions frozen: $R = r_{\rm sys}/r_{\rm tol}$, $\le 1$ passes, everywhere (Tables 9.4/9.5/9.6, Fig 9.7, Ch 11); primary criterion $R_{\rm dil}$ against $\min(r_\perp, r_\parallel)$, both components reported; $g$ = local shelf density over the 6-MHz average, nominal 0.56.
- Tripwire drawn correctly in Figs 5.2 and 6.1: the exact identity is $P_r$ accumulated two ways with no transform; Parseval holds only to the rounding bound.
- Removed contamination is $\bar P_{\rm all} - \bar P_{\rm keep,contrib}$ over the common denominator, in linear power (§6.4, App C); the plates show $\bar P_{\rm all}$ and $\bar P_{\rm keep\mid keep}$ and never subtract them.
- Fig 6.3 is a strict one-factor ladder (unquantized/full-weight float → quantized-input float → int4-weight float → integer CPU oracle → GPU).
- Fig 10.2 finalizes inside the kernel and publishes on both paths (valid, or invalid with reason); Fig 10.3 is the new frame-timing diagram; Table 10.3 requires 24 h / $2.06\times10^6$ frames for a diurnal claim, with 8 h as the engineering-stability minimum.
- Era states are proxy-high / proxy-low / ambiguous unless a station record confirms; §8.1's frozen procedure is the authoritative statistic.
- Table 8.2 is now a containment plot (`fig:calibration:containment`) plus a compact table; Table 8.3 is preselection null calibration only; Table 9.6 is one decision row per channel with the term-by-term chain in the App C ledger; Table 11.1 is counts by disposition.
- Fig 7.1 routes calibration through the frozen holdout before the forecast; Fig 8.1 takes the science tolerance and transfer model as explicit inputs.
- Fig 4.2 writes $\mathcal D$ as a bin set and labels the nominal target as never retuned; the measured anchor places the window or triggers the sentinel.

Not adopted, deliberately: removing Fig 1.6, Fig 5.1, or the worked frame (Fig 6.7); moving Fig 9.6 / Table 9.3 to an appendix; these are pedagogical or method-sensitivity content the author wants in the body.

## Code follow-ups (for when you are back at a computer)

The document now describes only the durable checks; the code has to be made to match it. In rough priority:

1. **pilot-proxy debug taps** (`RowSumsTap`, `PowerTerms`): either retire them or mark them development-only in the kernel header and README; the dissertation says production binds them to `NULL` and the release suite checks that binding them changes no output — make sure a test actually asserts that.
2. **Era procedure as configuration** (§8.1): the policy values (≥30 frames / ≥5 acquisitions / ≥3 days per month; proxy-high ≥ 1 dB, proxy-low ≤ 0.5 dB on the monthly median of 10·log10(F/μ0); ≥3-bin peak step; 2-month persistence) and their sensitivity alternates belong in a versioned config that RFIsher/pilot-proxy reads, with the PELT sensitivity check as a separate command.
3. **Per-channel evidence ledger** from RFIsher: one machine-readable file per rerun from which Tables 8.1–8.3, 9.4, 9.6, 11.1, Fig 11.1 and the App C plates are all generated; nothing hand-typed.
4. **g reconciliation** in the estimator-sweep tooling (`make evaluate`): measure the waveform's density at ±6.1 kHz vs flat top and the clean-waveform target/reference ratio, and report both against the fitted saturation.
5. **Removed-contamination product**: compute P̄_all − P̄_keep,contrib over the common denominator, in linear power, from the decoded `psd_frame_db_i16` — not the difference of the two plotted means.
6. **Shadow-run acceptance values** (Table 10.3) into the kotekan test/CI config once you set them; **frame-timing contract** (readiness event → launch → completion event → visibility waits in applied mode) matches Fig 10.3.
7. **datatrail fork**: fold the `djg/feat-*` branches into one documented release (recursive discovery, inventory manifest, manifest pull with integrity, verify-dataset, doctor) so Appendix D can pin one revision.
8. **Manifest pins**: every `to pin` cell in Table D.1, plus GNU Radio / LimeSuite / RadioFisher versions and the FCC LMS / ISED snapshot dates.
9. **Lessons learned worth a line in the repo docs**: the 0x00/0x88 constant-frame incident → reason-coded validity at processing time; the rate-table-with-mistuned-detector incident → every rate table carries its weight-bank digest; the sequential-capture pseudo-array as the synthetic feed axis.
10. **Fiducial cosmology refresh** (needs RadioFisher): the forecast bank, the frozen exports behind Figs 1.3/1.4 (`intro_wiggle_*.csv`), the Eisenstein-Hu no-wiggle parameters in `figure_src/intro_figures.py` (`_H0`, `_OM`, `_OBH2`, `_NS`), and the tolerances of Table 9.2 all sit on the Planck-2018 fiducial. Re-derive them from the latest published measurements, regenerate the exports, and re-pin; every `\cite{planck2018}` and "Planck-2018 fiducial" in the text then needs the new reference.

- **Survey flag, not a threshold**: the text now treats $F>\mu_0$ as a per-frame mechanism check (the coarse path ran, the marginal identity held) plus a crude occupancy indicator; no threshold is set during the survey, every masked fraction is at the post-hoc $(\rho^\star,\eta^\star)$, and the flag rate appears only as occupancy. Make the code's naming match (`survey_flag`, threshold mode `none`), and drop any table generator that reports a "masked fraction at the bootstrap rule".
- **$K^\star$ rule** (Eq. 4.x): $K^\star = \max\{K=2^j : E_K(c) \ge E_{\min}\ \forall c\}$ with $E_{\min}=0.9$ (sensitivity 0.8, 0.95); implement $E_K(c)$ in the containment analysis so Table 8.2 reports it and names the binding channel.

## Verification tiers (the rule the text now follows)

- Production invariants (every frame, forever): marginal tripwire, reason-coded validity, completion-counter contract.
- Release suite (every build/commit): `make test`, `make release-check`, `make freeze-check` in pilot-proxy and the equivalents elsewhere; passing it is the reproducibility claim. Appendix D ends with the rerun recipe.
- Development diagnostics are not described unless they explain a design decision (Appendix B). The debug taps are now one sentence in §6.2.6 and are no longer drawn.

## Figures now drawn in TikZ (editable sources in `figure_src/tikz/`)

- Packages in use now: `circuitikz` (antenna, ADC, adder symbols in Figs 2.1 and 6.3), `bytefield` (Fig 6.1a bit layouts: packed byte, DP4A lane word, MaskOut word), `tikz-timing` (Fig 10.3 frame timing). `dsp_shapes.tikz` is a small shape library (adders/multipliers, comparators, registers with bus widths, shared/global memory, ring buffer, thread and block grids, crossbar, correlator, butterfly, impulse response, quantizer staircase, ADC, antenna). Figs 2.1 (`placement.tikz`), 5.2 (`pipeline_chain.tikz`), 6.1 (`datapath.tikz`), 6.2 (`fused_kernel.tikz`), 6.3 (`paired_validation.tikz`) and 10.1 (`stage_pipeline.tikz`) are drawn with it; add new symbols there rather than inline.

- Fig 1.1 `evidence_chain.tikz`, Fig 3.1 `pilot_on_skirt.tikz` (new; three panels: allocation, references at the skirt, and the sub-noise regime with the noise floor; absorbs the old Fig 3.1 near-coincidence note), Fig 5.2 `pipeline_chain.tikz`, Fig 6.2 `fused_kernel.tikz`, Fig 7.1 `survey_evidence_flow.tikz`, Fig 7.2 `product_card.tikz` (new), Fig 8.1 `calibration_flow.tikz` (new), Fig 9.3 `residual_chain.tikz`, Fig 10.2 `stage_lifecycle.tikz`; plus the inline TikZ of Figs 2.1, 4.2, 6.1, 6.3, 10.1.
- Figs 1.3 and 1.4 were regenerated from `figure_src/intro_figures.py` (2×2 ruler: separation and wavenumber, each with the smooth part and with it removed, using the Eisenstein–Hu no-wiggle spectrum as the smooth part; dilation/growth in ξ and in the wiggle plus a smooth additive residual, one centred legend); the regenerated PDFs are in the patch (`git apply` needs the `--binary` diff it was made with).
- The vendored PDFs no longer referenced (`figs/fig_claim_chain.pdf`, `fig_survey_evidence_flow.pdf`, `fig_residual_chain_audit.pdf`, `fig_deployment_lifecycle.pdf`, `fig_vsb_standard_model.pdf`) remove them and their generators from `FIGURE_SOURCES.md` / the manifest when convenient.

## Figures to regenerate (existing artwork kept as placeholder)

- `fig:census:psd`, `fig:census:psd:lower` — one 23-panel current-era spectral face replaces both.
- Figs 5.3/5.4 `fig:estimator:digital-transfer`, `fig:estimator:ota-transfer` — from the repeated sweeps with the g reconciliation.
- Fig 6.7 `fig:example` — the same two frames from the v5 product, boundary drawn at the selected (ρ*, η*).
- Fig 9.2 `fig:tolerance:time` — drop the historical annotations; mark the band fractions at the bootstrap rule and at the selected points.
- Fig 9.5 `fig:tolerance:case` — same channel on its current era at the selected point.
- Fig 9.7 `fig:tolerance:twowalls` — fine-axis curves from the current-era histogram families (artwork still labels the coarse floor).
- App C plates (23) — every plate now carries a SUPERSEDED banner; v5 layers: current-era histograms with null-source label, bulk overlay, CCDF and η*; offset-containment panel (K = 64/128/256 from the per-frame 23.8 Hz PSD); η trade curves with the selected point and holdout points; retained-conditional-mean masked-vs-unmasked PSD; era boundary and stale-latest flag on the heatmap. Expect two pages per channel for legibility.

## Other loose ends

- Appendix D: pin the commit of each of the six code repositories in the release manifest and fill the `to pin` cells; pin GNU Radio, LimeSuite, RadioFisher versions and the FCC LMS / ISED snapshot dates.
- v5 schema: Ch 7 and App C now describe `psd_frame_db_i16` as the code defines it (feed-summed, N-point grid, int16 at 0.01 dB about `psd_db_reference`, decode before averaging). Confirm one completed v5 unit against that paragraph before the rerun goes far.
- Shelf definition frozen: allocation-average over 6 MHz everywhere; flat-top density (B_N = 5.381 MHz) appears only in the Ch 3 transmitter-side derivation, 0.47 dB higher.
- ISED: §3.4 does not cite the Canadian instrument; add it if a committee member asks.
- dtv-census: §3.4 describes the chain as it is (curated workbook → deterministic reduction → ISED overlay); update when the direct source pull replaces the workbook.
- PDF accessibility tagging: pdflatex output is untagged; check the WVU ETD requirement before submission.
- `make verify` will fail its PDF-freshness and manifest checks until `make manifest` is re-run after rebuilding.
- `README.md`, `REVISION_NOTES.md`, `FIGURE_SOURCES.md`, `archive_completion_checklist.md` still describe the v3/v4 record and still use 'trawl'; not edited. The body text no longer says 'trawl' anywhere (the label `sec:survey:trawl` is kept so cross-references don't break).
- Colours: every figure, TikZ and matplotlib, draws from the WVU palette in `figure_src/style.py` / `figure_styles.tikz` (safety blue = measured, old gold = model/transfer, hemlock = conditional, woodburn = failure/refusal, seneca gray = pending/context); the only non-palette colours are the neutral ink/muted greys for text and axes.
- Acknowledgements: personal thanks still scaffold text; funding line is now a stub.
- Propagation case study (ducting vs aircraft Doppler): not started; §3.4 has the mechanisms and Table 3.2 the Doppler envelope.
