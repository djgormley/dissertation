# Full-depth H0 table + stack-subset verification — 2026-07-17

Inputs: fulldepth.tar.gz (h0_fulldepth.csv, event_presence_signatures.npz),
generated on CANFAR by scripts/fulldepth_and_subsets.py at the same
product snapshot as the dumps.

## Verified

- **h0_fulldepth.csv consistent with the dumps.** n_valid matches
  perframe.npz on all 23 channels (0 mismatches; same 339,196-frame
  snapshot). 13 of 23 channels have full-depth mean F within the
  |mu0-1|/3 tracking bound; the failures are the signal-dominated and
  signal-elevated channels (17, 21, 24, 30), the pilot channel (14), and
  channels whose bound is microscopically tight because mu0 ~ 1 (16, 22,
  25, 28, 31). This is the expected pattern: the full-depth MEAN includes
  the signal tails, which is why the paper's calibration uses the
  mode-anchored core (Fig. 4), not the mean.
- **Survey bookkeeping ties out exactly.** Signature counts give 8604
  distinct events and 77,423 channel-event pairs — the manuscript's
  "77,423 of 161,872 file-events" to the digit.

## Discrepancy found (now a blue slot in Appendix B)

Exact k=16 subset search recomputed from the signatures (all C(23,16)
subsets, superset containment = "common events"):

| k | max common events | argmax channels |
|---|---|---|
| 14 | 1910 | 15,17,18,19,20,21,22,23,25,27,28,33,34,36 |
| 15 | 1873 | + 16 |
| 16 | **1829** | + 29 (15,16,17,18,19,20,21,22,23,25,27,28,29,33,34,36) |
| 17 | 1789 | + 35 |
| 18 | 1587 | 14 in, 35 out |
| 20 | 824 | |
| 23 | 0 | ch24/ch26/ch30 never co-occur with the rest |

The recorded stack is 16 x 1548. Alternate readings do not reproduce it
(events contained within the 16-set: 6593; exact signature match: 1).
Since the pair count matches the Section 6 snapshot exactly, the +281
gap is NOT survey growth after the text's dataset numbers were pulled;
the recorded selection most plausibly filtered on >=1 VALID frame per
channel per event (the signatures use raw source_event_keys presence),
or was frozen on an earlier product state (recorded 2026-07-08, amended
2026-07-14). Dylan to reconcile; the archived appendix_dropcurve.csv /
appendix_exact_by_k.csv will settle it immediately.

Note for the reconciliation: the stack-based analyses in the paper used
the recorded 1548-event stack, which remains a valid recorded choice
either way; what changes is only the wording strength available in
Appendix B and any future re-freeze.

## Resolution (same day)

Dylan confirmed the initial 07-14 selection ran against an incompletely
staged _per_pilot set, and chose to RE-FREEZE under the unchanged
recorded rule on the complete snapshot: **16 channels x 1829 events**
(physical channels 15-23, 25, 27-29, 33, 34, 36). Tables regenerated
from the signatures via a superset-sum transform over all 2^23 masks
(independently confirms the C(23,16) enumeration: 1829) and archived
here as appendix_exact_by_k.csv + appendix_dropcurve.csv. Greedy
drop-curve strands at 60 events at k=16 - the exact search is doing
real work. Manuscript updated (§6.1 + Appendix B); the superseded 1548
freeze is documented in-text as a staging incompleteness, not a rule
change.

## Correction (2026-07-17, after full pipeline regeneration)

The staging hypothesis above is FALSIFIED: Dylan re-ran
generate_results.py --stack-mode max-events on the complete staging
(all 23 products, same 339,196 frames; integrity PASS) and the pipeline
reproduces 16 x 1548 exactly. Root cause of 1548 vs 1829 is the SEARCH
FAMILY, not the data: exact_subset_search() seeds candidates only from
OBSERVED presence signatures (AND-closed per block), so its by-k table
is exact per block but not over all subsets (visibly non-monotone in k:
830 at k=15 vs 1548 at k=16). The unrestricted 2^23 superset-sum finds
the true objective maximum 1829 at {15-23,25,27-29,33,34,36}; both
counts verified against the same signatures file (pipeline set -> 1548,
matching combine_subset_decision.json; unrestricted set -> 1829).
Event-keyed alignment of the pipeline stack retains 1329 events / 5638
frames.

**Decision (Dylan):** keep 1548, procedure-as-recorded. The earlier
"re-freeze at 1829 / staging incompleteness" resolution above is
retracted; manuscript §6.1 and Appendix B rewritten accordingly (1548 +
aligned counts; 1829 documented as a not-adopted unrestricted
alternative). Provenance files re-roled: appendix_exact_by_k.csv =
recorded procedure's by-k (from combine_subset_decision.json);
appendix_dropcurve.csv = registered greedy drop-curve;
appendix_unrestricted_by_k.csv = unrestricted table;
combine_subset_decision.json archived alongside.

## Bundle received (canonical)

results_bundle_chime-pilots_20260717T040435Z.tar.gz archived in
provenance/ (sha256 be7e3d5767bf96d8a24d1e0409a860728235d7ed2dd5ebe0ae3399a01f396496,
11.5 MB, 184 files). Verified identical to the earlier zip-packaged
results tree (only the mid-run log tail differs); the zip additionally
carried the four big combined NPZ stack products that the bundle leaves
on /arc - retained locally for stack-level verification.
