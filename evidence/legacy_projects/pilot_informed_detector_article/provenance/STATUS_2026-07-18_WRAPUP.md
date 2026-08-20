# Session wrap-up status — 2026-07-18

## Sync state (verified at goodbye)

origin/master = 7fa0476 ("changed default gpu settings"; before it
81c5256 = delta20 applied). Outstanding from our side = delta21
(pilot-proxy-delta21-ch30-notch-on-7fa0476.patch, verified on pristine
7fa0476): analysis/ch30_offair_minority.py + its provenance CSV +
build_spectra_all23.py adaptive notch. After delta21 is applied and
pushed, the repo fully reflects every number and figure in rev17.
Still owed as local drop-ins: audit_v3.json, audit_v4.json,
regenerated trim_report.json, trim_report_stationary.json into
data/provenance/t2_convention_20260718/ (if Block 1's script didn't
already put them there).

## Authoritative documents

- draft_article_rev17.pdf — 33 pp, 0 overfull, no Type 3, no undefined
  refs. New since rev16: Sec 5.2 ch30 mixture-route test + refusals
  cross-ref, Sec 8 kernel-integration status (measured pairs never
  loaded; floor-sense compare missing) + slow-loop recorded note,
  Sec 6.3/8.1 completeness-scan corrections and redshift translation
  (rev15/16 content).
- dissertation_supplement.pdf v5 — 15 pp findings ledger, 10 figures,
  incl. tone gallery, threshold exchange-rate argument, ch24-vs-time,
  ch30 dissection, ch33 drift hypothesis + prepared job.
- supplemental_plots_rev16a.zip — full diagnostic plot set (adaptive
  notches).

## In flight (Dylan's machines)

- Survey extension scan (tmux "scan", cupy-gpu): 84,449 units across
  15 capped channels, resumable, ~as large as the original scan.
  Interruptible filler: Ctrl-C when a GPU queue block is ready.
- GPU queue after Block 2 (stationary sweeps): 2b half-bin (+/-1526
  Hz), 2c wide extensions (-60..-39, -23..-20), Block 3 G2 controls
  (fids 637/714/760/484 + bounded scan), G4 injection ladder;
  PLUS (proposed, ratify when ready): parity rerun with ch14's
  MEASURED (P,Q) from empirical_thresholds.csv — one constant in the
  existing harness — to upgrade Sec 8's "loads unchanged" to
  "demonstrated".

## Analysis waiting on artifacts

- Stationary sweeps -> T2 closure test (crossings vs ncF benchmark;
  Fig 3 panel (a) points should land on the lines) + final Fig 3.
- G2 -> control floor number into Sec 8.1 gpuval slots.
- G4 -> retention curve (the acceptance interface) + comparator.
- Scan finish -> refresh decision (paper stays frozen on the 77,423-
  pair snapshot unless refresh is chosen; full re-verification
  required if so). ch27 interior + ch17 midspan fill in either way;
  ch33 drift-track kit (36 events, scripts delivered) deferred until
  after the scan per Dylan.

## Dylan desk items (unchanged + new)

Start CHIME internal review (critical path); ISED/FCC lookups now
including: ch30's 2019 Apr 6-25 off-air window (CHKL-1) and the
CHKL-DT parent/relay family question, KDYS-LD 2023 history, ch33/CBUT
interim facility; ops spur-confirmation email; CHKL-1 terrain
(DRAO staff); RASTI author-kit template; Zenodo linking.

## Open blue notes in rev17

11 body + 3 appendix \needsdylan slots (supplementary-material
decision, transition corroborations, recorded-choice timestamps, spur
provenance, ch30 off-air corroboration, epoch-split ch33, etc.).
