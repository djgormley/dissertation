# Results plan: from finished data to a finished dissertation

Drafted 2026-09-06 against the state of the four repositories and the two data
copies on that date. Companion to `STUBS.md`, which remains the checklist.

## 1. Scopes

One sentence each, then the rule that follows from it.

| scope | owns | rule |
|---|---|---|
| **pilot-proxy** | turning baseband samples into per-pilot products, and the QA of those products | Exports only: products, product diagnostics, compact dumps and tables read straight from product internals. No interpretation, no dissertation figures. |
| **RFIsher** | turning products and evaluations into results | Every result the dissertation states -- tables, curves, selections, forecasts -- is produced here, whatever the source: CANFAR (offline) products, GNU Radio estimator evaluations, LimeSDR captures, and later the online run. One results package, one style. |
| **dissertation** | the text, and the figures that depend on no data | Renders illustrative and schematic figures from `figure_src/`; vendors RFIsher's and pilot-proxy's PDFs with the producing commit in `figure_manifest.csv`; keeps only the small hash-checked tables it renders from (`figure_src/data/frozen_export/`). |
| **WVU OneDrive** | data | Mirrors the stage roots below under `Datasets/pilot-tone-pipeline/`. Never scripts. |

Storage is by pipeline stage, one producer each, on WSL and on the OneDrive:
`datasets/` (raw inputs, produced by nobody), `products/` (pilot-proxy outputs),
`results/` (RFIsher outputs). "Where does it go" is "what produced it".

Consequences worth stating plainly:

- pilot-proxy's `analysis/` (45 scripts, all last touched 22-26 Aug) is results
  code by this rule. It migrates into RFIsher where a v5 stub needs it and is
  retired otherwise. The product-reading exporters stay: `tools/make_dissertation_tables.py`,
  `tools/export_dissertation_data.py`, the `analysis/dump_*.py` readers,
  `src/pilot_proxy/archive_health.py` (product QA, appendix C plates).
- pilot-proxy's `testbench/` (drives the SDR, evaluates captures with the
  detector) stays: that is sample processing. Its `plot_results.py` does not:
  transfer curves are results.
- RFIsher gains a results area with readers for the two evaluation formats
  it does not yet have (`dtv_snr_eval.json/.csv`, the estimator-transfer
  `analysis.json`/`plot_points.csv`) beside its existing `pilotproxy.py`
  reader for products.
- `evidence/` is not a category. Each release is an output of a run in a
  repository: RFIsher's forecast-completion releases already live in RFIsher
  (`docs/releases.md`); the archive-health release is pilot-proxy product QA;
  the estimator-transfer and OTA releases are RFIsher results. Small
  release tables (KB-MB) live in git in the producing repo; large artifacts
  (the 56 MB archive-health atlas, `legacy_projects`, `reference_pdfs`) go
  to the OneDrive with their manifests, and the dissertation keeps only what
  it renders from. `scripts/verify_vendored_evidence.py` then checks
  manifest hashes against the producing repo's release manifest instead of a
  local `evidence/` tree.

## 2. Style: one module, identical bytes

`dissertation/figure_src/style.py` is the audited original. The three copies
already agree on every constant (the WVU semantic palette -- measured
`#0062A3`, model `#7F6310`, conditional `#6A724F`, failure `#8D4638`,
pending `#988E8B`, sunset `#F58672`, gold `#EEAA00` -- Latin Modern through
LaTeX, 6.35 in canvas, pinned PDF metadata). They differ only in helpers:
the dissertation's diagram-fitting helpers, RFIsher's PDF byte-stability
helpers. Reconcile by union into the dissertation's module, copy it verbatim
into both repos, and add a test in each that fails on any byte difference.
Then retire pilot-proxy's older `analysis/_style.py` (Computer Modern, the
RFIsher-paper palette) with the scripts that use it.

## 3. What fills each stub

Producer -> consumer for the 38 stubs in `STUBS.md`.

| campaign | stubs | producer | input |
|---|---|---|---|
| v5 archive rerun, product side | ch03 spectra figure; ch06 worked example; ch08 eras/anchors/nulls; ch05 blocked evaluation; appC 23 plates + counts | pilot-proxy exporters on the v5 products (`make_dissertation_tables`, calibration data, `archive_health`) -> RFIsher tables -> dissertation | `products/chime_pilots_rebuild_20260829/products` |
| v5 archive rerun, results side | ch07 accounting; ch06 cross-build + held-out; ch09 (10 stubs, 83 markers); ch11 matrix, table, paragraph; headline | RFIsher | the same products via `rfisher.pilotproxy`; scan scopes in `logs/` for the accounting |
| LimeSDR detection | ch06 mscaling, loss table, fine-gain, frontier | RFIsher, from evaluations pilot-proxy's testbench already produced | evaluations in `products/estimator_transfer_2026-08-25/` and `products/ota_transfer_2026-08-24_ch35/`; raw captures in `datasets/sdr/`; `studies_2026-08/fine_gain_streams_2026-08-24` |
| dtv-census export | ch03 census table | pilot-proxy `analyze-transmitter-census` export -> RFIsher table | `pilot-proxy/data/census/census.csv` |
| synthetic estimation rerun | ch05:221 | pilot-proxy `evaluate-snr` sweeps at the production protocol (local GPU) -> RFIsher reconciliation | synthetic |
| Pathfinder shadow run | 5 + part of the headline | a live run; decision pending | telescope time |
| before submission | funding text | the author | -- |

The `\rerun{}` markers are re-verified mechanically: `STUBS_rerun_inventory.csv`
(file, line, section, value) is matched against a `numbers.json` each RFIsher
export writes; `\reruncolor` flips to black chapter by chapter as they verify.
The count disagrees across sources -- the inventory CSV has 177 rows, this plan
and `STUBS.md` say 175 -- so reconcile them when the matcher is written; the CSV
is grep-derived and has no generator script yet.

## 4. Order

1. Style union + hash tests (small, unblocks everything visual).
2. Export-interface bump: `pilot-proxy-dissertation-export` v2 covering the
   calibration tables and the archive-health counts; run the exporters on v5.
3. RFIsher results area: product readers already exist; add the SDR and
   estimator-transfer readers; migrate the calibration-report and
   tolerance-selection code from pilot-proxy `analysis/`; produce ch05-ch09,
   ch11 and appendix C tables and figures.
4. Dissertation: import the v2 exports, regenerate, audit, vendor; retire the
   local `evidence/` tree in favour of release manifests.
5. In parallel from step 2: synthetic sweeps on the local GPU; census export.
6. Re-verify the 175 markers; flip `\reruncolor`.
7. Pathfinder: run or rewrite.
8. Headline and funding text.

## Export schema v2: the measured gap (2026-09-06)

Running the existing exporters against the v5 products: `census_psd.csv` and
`census_centre.csv` export cleanly; the worked-example table fails on
`fstat_raw` (v5 carries `coarse_power_ratio`), and `make_calibration_data`,
`make_policy_data` and `make_report_data` fail on `mu0` (plus `best`,
`sweep`, `source_path`, which came from a summary JSON rather than the
product). Nine keys across four scripts in total; everything else in the
old analysis chain indexes fields v5 still has. The calibration-report
family is therefore a field-mapping port, not a rewrite, and it is the
first thing to migrate into `rfisher.results`.

## Progress

- 2026-09-06 (settled): generated results leave the repositories. RFIsher no
  longer tracks `out/` (commit 887ab81); its 12 MB of tables, ledgers and both
  forecast-completion release roots are frozen at
  `~/rail/results/forecasts/rfisher_out_c1302f4/`, which the repository
  resolves through `rfisher_results.results_tree.out_dir()`: `$RFISHER_OUT`,
  else the `out_dir` key of `data/products.local.json`, else its own ignored
  `out/` scratch. Both release manifests stay in git under `docs/releases/`,
  and a test checks a configured tree against them. The WVU backup is
  reorganised to match the stage roots under
  `Datasets/pilot-tone-pipeline/{products,results,archive}`; every tree there
  carries its own `SHA256SUMS`. See `HANDOFF.md` for what is left.

- 2026-09-06: RFIsher branch `results-layer` -- `rfisher.results` with the
  reconciled style and the estimator-transfer figures (digital and OTA)
  rendered from the releases in the dissertation style; six tests; CLI
  `rfisher-results estimator-transfer`. To merge, then vendor the two PDFs
  and update `figure_manifest.csv` (producer: RFIsher, not pilot-proxy).

## Figure audit on main (2026-09-06)

`python3 -m figure_src.audit_figures` fails on `main` before any of this
work: inline TikZ remains in ch04, and the manifest's active PDF and TikZ
inventories no longer match the chapters' includes (the Overleaf-side stub
edits removed some includes). The two re-rendered transfer figures pass the
font and format contracts; those three pre-existing errors are the author's
to reconcile when the stubs are filled.

- 2026-09-07 (UTC): the two transfer figures are vendored from RFIsher
  (dissertation 77c92b3; Latin Modern only; manifest rows name RFIsher). The
  results layer is the package `rfisher_results` (outside the bank digest);
  `python -m rfisher_results.cli estimator-transfer ...`. pilot-proxy
  hardening items 13, 14, 17, 18 landed (6147d23) with tests; 12 and 16 remain.
  The v5 census PSD export exists (`products/.../analysis/exports_v5/tables/`);
  a 23-panel renderer for it is next in `rfisher_results`.

- 2026-09-07: `rfisher_results` merged into RFIsher `main`; `census-psd`
  subcommand renders the chapter-3 stub's single 23-panel figure from a
  `census_psd.csv` export. Rendered now from the v5 archive average
  (`results/figures_preview/fig_census_psd_all23.pdf`); the per-era version
  the stub asks for follows the calibration port. Vendoring it also needs
  the chapter's two half-band includes replaced by the one figure -- text.

## 5. Decisions needed from the author

- LimeSDR: the author recalls the SDR test may need repeating to simulate
  2048 feeds (uncertain; the SDR is not at hand). Until settled, the four
  LimeSDR stubs are rendered from the 2026-08-25 captures and marked as such.
- Pathfinder shadow run: schedule it, or rewrite those five stubs and the
  headline as planned deployment.
- Confirm the `evidence/` disposition in section 1 (large artifacts to the
  OneDrive, small tables into the producing repos).
- The vendored-evidence gate: `verify_vendored_evidence.py` asserts byte
  equality between the two vendored transfer figures and the 2026-08-25
  releases, and today's re-render in the dissertation style breaks that.
  Re-issue those releases with the new figures, or move the verifier to the
  producing repository's release manifest as section 1 plans.
