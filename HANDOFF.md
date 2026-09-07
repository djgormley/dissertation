# Handoff: what is done, what is left

Written 2026-09-06, after the CANFAR campaign closeout and the reorganisation
of the workstation, the repositories and the WVU backup. Companion to
`RESULTS_PLAN.md` (the plan for filling the stubs) and `STUBS.md` (the
checklist). This file is the to-do list.

## Where everything is

Storage is by pipeline stage, one producer each, the same on the workstation
and on the WVU RAIL OneDrive.

| stage | workstation | OneDrive (`RFI Mitigation/Datasets/pilot-tone-pipeline/`) |
|---|---|---|
| raw inputs | `~/rail/datasets/` (294 GB) | not backed up: re-pullable from CHIME/FRB, and the team's captures are in the sibling folders |
| pilot-proxy outputs | `~/rail/products/` | `products/` |
| RFIsher outputs | `~/rail/results/` | `results/` |
| retired repositories | `~/rail/repo-archives/` | `archive/` |

The September campaign (`products/chime_pilots_rebuild_20260829/`, 17 GB, 82
files in its `SHA256SUMS`) exists in three verified copies: the workstation,
the OneDrive, and CANFAR until it is wiped. Code lives only in the
repositories; generated products live only outside them.

## Yours: decisions or hands-on work

1. **Run the deletions.** `~/rail/delete_me/` and
   `Datasets/delete_me/` on the OneDrive hold everything discarded during the
   reorganisation. Two things in there are cited by code before you empty them:
   `dev_rehearsals_uncited/local_archive_rehearsal_844_f9ab7d7cfb13/_per_pilot/844.npz`
   is the fixture `RFIsher/tests/test_residual_scores.py` pins by hash, and
   `campaign_superseded/duplicates_shard3_b59b5c0/` is the independent
   reproduction the campaign ledger cites (its products are byte-identical to
   the canonical ones, so the hashes in the ledger already record the result).
   Rescue or accept the loss, then delete.
2. **Wipe the CANFAR home.** Nothing there is unique any more. The qualified
   sm90 kernel, the `pp_switch` kit and the runtime freeze tar are preserved
   under the campaign's `kit/` on both copies.
3. **Pathfinder shadow run:** schedule it, or rewrite those five stubs and part
   of the headline as planned deployment.
4. **LimeSDR:** you thought the SDR test may need repeating to simulate 2048
   feeds. Until that is settled the four LimeSDR stubs render from the
   2026-08-25 captures and say so.
5. **Chapter 3 include swap:** the census figure is now one 23-panel plate
   (`rfisher_results census-psd`). The chapter still includes two half-band
   figures; replacing them is a text edit only you should make.
6. **`dissertation.pdf` is neither tracked nor ignored**, while `.gitignore`'s
   comment, `MANIFEST.sha256` and the CI freshness gate all assume it is
   committed. Decide: commit the built PDF, or ignore it and drop those
   assumptions.
7. **Two drawings of figures 5.2 and 6.2** exist: the tracked `tikz/` sources
   the chapters build from, and an untracked `figure_src/tikz/` left over from
   the superseded local line. Say which is canonical; the rest is mechanical.
8. **Vendored-evidence gate fails** on the two re-vendored transfer figures:
   `scripts/verify_vendored_evidence.py` asserts byte equality with the
   2026-08-25 releases, and the figures were re-rendered in the dissertation
   style. Either re-issue those releases with the new figures, or make the
   verifier check the producing repository's release manifest instead, as
   `RESULTS_PLAN.md` section 1 already plans.
9. **RFIsher: where do regenerated tables go.** The readers now resolve the
   frozen results tree; the writers still default to the repository's ignored
   `out/`. So "regenerate, then gate" no longer checks what was just written.
   Either point the writers at `out_dir()` and create a new dated tree per
   rerun, or have the rebuild scripts export `RFISHER_OUT=out` for their gate
   step.
10. **pilot-proxy deferred items 12 and 16** (the datatrawl rename including
    schema keys, and the staging guard in the retired CANFAR scripts), plus the
    live interrupt rehearsal that item 14 still leaves open.
11. **Send the CADC outage report** for the 2026-09-03 shard failures.
12. **Analysis flags** still unset: the H0 criterion and the census rho.
13. **Two hidden directories** outside the documented layout:
    `~/rail/.inventory-spectrum-sensor-20260903` (80 MB) and
    `~/rail/.review-ccaaw-2021` (144 MB). The second holds an audited version
    the visible `ccaaw-2021` lacks, so it may be the copy worth keeping.
14. **Four stray `fig_bao_*.pdf`** in the RFIsher repository root, from an
    August render; ignored by git and superseded by the vendored figures.
15. **`results-layer`** is fully merged into RFIsher `main`; the branch and its
    remote can go.

## Next session: the work itself

In the order `RESULTS_PLAN.md` sets out.

1. **Export schema v2.** The exporters and the whole of pilot-proxy's
   `analysis/` read the retired archived vocabulary, so they crash on the v5
   campaign products: `--worked-example` on `fstat_raw` (v5 has
   `coarse_power_ratio`), and the calibration, policy and report data on `mu0`
   (plus `best`, `sweep`, `source_path`, which came from a summary JSON).
   Nine keys across four scripts; a field-mapping port, not a rewrite.
2. **Port the calibration-report family** into `rfisher_results`, then produce
   the chapter 5 to 9, chapter 11 and appendix C tables.
3. **RFIsher readers** for the two evaluation formats it still lacks
   (`dtv_snr_eval.json/.csv` and the estimator-transfer
   `analysis.json`/`plot_points.csv`).
4. **LimeSDR figures** from `~/rail/products/estimator_transfer_2026-08-25/`
   and `~/rail/products/ota_transfer_2026-08-24_ch35/`.
5. **Census table** from the transmitter-census export.
6. **Synthetic sweeps** on the local GPU for the chapter 5 stub.
7. **Rerun markers:** match the inventory CSV against a `numbers.json` from
   each export and flip `\reruncolor` chapter by chapter. The counts disagree
   across sources (the CSV has 177 rows, this plan and `STUBS.md` say 175);
   reconcile them when the matcher is written.
8. **Retire** pilot-proxy's older `analysis/_style.py` plate scripts.

## Mechanical follow-ups

Small, safe, and none of them blocking. Found in a repository-wide audit on
2026-09-06; the first four were verified by a second pass, the rest were not.

- **RFIsher CI is red.** `scripts/check_paper_numbers.py` runs in a checkout
  that has no results tree, so it raises `FileNotFoundError` instead of the
  documented "tables missing" message. Guard the step or make the script exit
  cleanly.
- **pilot-proxy `docs/LOCAL_PROCESSING.md`**, the runnable local runbook, still
  writes to `~/rail/pilot_proxy_runs`, `pilot_proxy_staging` and
  `pilot_proxy_logs`, which the reorganisation removed. Following it would
  recreate the old layout on the next run.
- **pilot-proxy `analysis/_products.py`** defaults `PP_PER_PILOT` to
  `~/pilot_proxy_runs/...`, so every script in `analysis/` exits unless the
  variable is set. The right default depends on which product set the analysis
  uses.
- **pilot-proxy `scripts/canfar/`** and its README still tell a reader to look
  under `/arc/home/dgormley`. Add a line saying the home was cleared and where
  the kit now lives.
- **RFIsher `docs/reproducibility.md`** points `RFISHER_PRODUCT_DIRS` at a
  directory that no longer exists; the pinned products are in
  `~/rail/products/per_pilot_2026-08-20_complete23`.
- **RFIsher's paper** sets `\graphicspath{{../out/}}`, which is empty in a
  fresh clone. Note that `scripts/run_forecast.py` must run first.
- **647 dangling symlinks** in `~/rail/studies_2026-08/preflight_stage` and
  friends still point at the pre-move baseband path. The data is intact at the
  new path; the links are one substitution away.
- **Stale README numbers:** `~/rail/datasets/README.md` describes
  `canfar_pilots_10s` as 25 events x 23 channels; it holds 644 files over 115
  event ids. `~/rail/studies_2026-08/README.md` points the SDR captures at a
  path that never existed.
- **`~/rail/products/dev_rehearsals_2026-08/HANDOFF_20260831.md`** still reads
  as a live instruction to resume a scan that has since finished.
- **27 empty directories** left from scaffolding, mostly under
  `~/rail/inventory_rebuild/evidence/`.
- **`MANIFEST.sha256` and `.pdf-inputs-digest`** in this repository are from
  the superseded 1 September line and do not describe `main`.
