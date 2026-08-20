# R8 triage (review of rev12f) — 2026-07-17

Reviewer's analytic verifications all reproduce (C, crossings, Pd(-38),
sinc^2 1.592 dB, 13.546 dB). Verify-first results on their claims:

- Backup-mode 1.31 dB spread: VERIFIED exactly ((tau/mu0-1) ratio ch20
  vs ch18 -> 10log10 = 1.31 dB). Fixed by per-channel analytic-mu0
  normalization sentence + "tested curve is channel 14's".
- int4-float "<=0.06 dB" bound: reviewer right that it lacked
  uncertainty. Paired bootstrap (500 reps, trials resampled jointly)
  from the archived 45k trials: thrP50 -0.047 [95%: -0.121,+0.022],
  thrP90 -0.022 [-0.100,+0.051], pexP90 -0.063 [-0.238,+0.121] dB.
  Text now quotes central +/- 95% CI; "consistent with zero, at 95%
  extreme under half the observed offsets".
- Audit "direct" field: reviewer right it is not estimator-independent
  (pilot power = +/-10 kHz window - median baseline; matches the 0.05-
  0.06 dB systematic seen in the in-session synthetic validation).
  Wording adopted ("under the stated periodogram, pilot-window, and
  allocation-boundary conventions"); coherent-projection cross-check
  noted (arrives with trim_report.json in G3). "audit v2" name dropped
  (schema still v1); "pilot placement exact to -0.4 Hz" corrected (the
  -0.44 Hz was the PSD grid offset; resolution 164 Hz; placement is by
  generator construction).
- Reviewer's -0.38 dB projection: matches our own overshoot computation
  (0.678 dB pilot/noise shift); now stated in-text with the compensating
  component explicitly unattributed pending the trimmed regeneration.
- PAPER_PLAN.md check: records ONLY the stack rule + census inclusion
  rule (registered 2026-07-08). No three-arm thresholds, no ch24/ch30
  policy, no acceptance pair. Escalated blue slot with the R8
  conditional (timestamped record or downgrade to "retrospectively
  motivated candidate" at 4 sites). DYLAN DECISION.
- Parity: claim scoped to tested configuration; zero rational-overflow
  reported; artifact-schema gaps stated in-text (no CPU-side integer
  columns, no commit/weight-hash fields); repo-commit of the artifact
  requested (blue slot).
- p.20 remaining-work parity mention removed; Fig 3 caption "Inset" ->
  "Annotated"; FloatBarrier before section 7; appendix figures [t];
  emergencystretch for overfull URLs.
- 77,423 -> "channel-event records" + unique event counts (8,759
  inventoried / 8,604 in products), consistent with the archive
  composition memo.
- Appendix B: search renamed signature-seeded heuristic in-text;
  1548->1329 alignment loss explained (219 events fail (event,
  frame-in-file) identity); robustness-on-both-stacks blue slot added
  (one --stack-freq-ids CPU run).
- Phase 1a: out-of-allocation control now REQUIRED in-text (freq_id 484
  already in the chime-controls inventory command).

Not actionable now: Phase 2 gates (G4 queued), quarterly/trigger-stratum
analyses (event-key dump in flight), RASTI-class preflight (with class
swap).
