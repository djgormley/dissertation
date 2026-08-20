# Dissertation structure and evidence map — implemented 2026-08-12

> **Historical structure record.** The chapter split below remains current, but
> its original result-status descriptions have been superseded by the completed
> all-23 archive, `archive_completion_checklist.md`, and Appendix A's evidence
> matrix. Treat this file as a map of the implemented structure, not as a current
> scientific completion checklist.

The earlier proposal to split the monolithic article into chapters has now been
implemented. `dissertation.tex` is the only active build entry point.

1. **A Ruler, a Broadcast, & an Error Budget** — pedagogical cosmology,
   detectability versus tolerance, requirements, and claim boundaries.
2. **Scientific Context, Instrument, & the Detection Problem** — CHIME signal
   path, RFI context, and scope of the work.
3. **Digital Television RF Anatomy & Parametric Beacon Characteristics** — ATSC
   clock/pilot relations, nominal transmitter model, census, and propagation.
4. **System Parameterization & Weight Profile Synthesis** — architectural
   constraints, reference geometry, and exact weight generation.
5. **Multichannel Signal Processing & Detection Pipeline** — hypotheses,
   coherent/noncoherent accumulation, statistic, calibration boundary, and
   decision rule.
6. **Exact-Arithmetic Implementation & Verification** — packed datapath,
   transform, modular arithmetic, fused kernel, host contract, and verification.
7. **The Survey: Captures, Trawl, & Products** — triggered archive, selection
   function, bounded-storage processing, product schema, provenance, and holdout.
8. **Calibration: Anchors, Nulls, & Operating Points** — anchor localization,
   floor refusal, correlation-time states, epoch splits, and calibration bundles.
9. **Noise Tolerance: Pricing the Mask for BAO Cosmology** — proxy and visibility
   chain, stochastic/coherent terms, Fisher tolerance, policy cost, residual
   templates, all-23 conditional screening results, and closing measurements.
10. **Real-Time Integration Contract & Operations** — proposed `kotekan` stage,
    buffer and synchronization contracts, fail-closed behavior, runbook,
    monitoring, and performance acceptance.
11. **Conclusions & Future Work** — measured contributions, conditional
    all-channel synthesis, and the program required for a final scientific
    recovery verdict.
12. **Appendix A: Evidence, Assumptions, and Closing Tests** — claim-by-claim
    maturity and release requirements.
13. **Appendix B: Legacy Evidence and Reuse Boundary** — superseded detector
    geometries, retained validation patterns, and the measurements that must be
    repeated at the current geometry.

The file `legacy/chapters_I-V_draft.tex` is retained only as the pre-split source
snapshot. It is not included by `dissertation.tex` and should not be edited for
future revisions.
