# Dissertation evidence releases and integrated legacy evidence

This directory is the canonical home for both the current evidence releases and
the legacy work retained by the dissertation.  Appendices B and C explain which
findings are current, which numbers belong to superseded detector geometries,
and which closing measurements remain.

## Directory map

- `canfar_archive_health_v1/` - immutable all-23-channel archive-health release,
  exact exclusion ledger and spectrum repair, exposure accounting, status
  exports, and 92 channel diagnostics from PilotProxy commit `2cf4d8c`.
- `bao_forecast_completion/` - authenticated all-seven-bin, four-analytic-family
  forecast completion release from `bao-noise-tolerance` scientific commit
  `3b5fc5e` and deterministic dissertation-figure commit `db89d62`.
- `legacy_projects/pilot_informed_detector_article/` - article source, figures,
  compact sweep/survey products, waveform audits, decision records, provenance
  memos, producing commit, and repository patch.
- `legacy_projects/calibrated_detector_gpu_prototype/` - earlier detector/GPU
  manuscript, compiled preview, bibliography, and figures.
- `legacy_projects/chapter04_sensitivity_project/` - sensitivity chapter source,
  compiled PDF, generator, compact NPZ/CSV/JSON products, tables, and figures.
- `legacy_projects/pilot_proxy_findings_ledger/` - findings-ledger source,
  scripts, tone CSV, and figures.
- `reference_pdfs/` - the four reviewed reading copies.
- `legacy_review.md` - the original file-by-file preservation assessment.
- `../MANIFEST.sha256` - root-level release hashes for every tracked file in the
  dissertation bundle, including this directory; it is refreshed only after
  the bundle is otherwise frozen.

## Important legacy boundary

The following large artifacts are named by the retained provenance but were not
inside the supplied projects:

- `results_bundle_chime-pilots_20260717T040435Z.tar.gz`
  (`be7e3d5767bf96d8a24d1e0409a860728235d7ed2dd5ebe0ae3399a01f396496`)
- `results_bundle_chime-pilots_20260717T162658Z_stack1829.tar.gz`
  (`16fba766541e165661f86810dac1e5efb5d9e57afdeaddadb1becb835b0c571b`)
- `run_pd_curves_cpu_1000.tar.gz` (the archived 45k-trial CPU sweep)
- `all_spectra.npz`
- `generated/atsc/atsc_8vsb_complex64.cfile`
  (`004a05d5a462149c24d05b3478f860b4b7f68da5a7dc0a97a41789e16042b530`)
- `weights/chime_dtv_weights_k128.bin`
  (`b0dce17a8ef5b24da1fa9d7e41bab019531a06549bd8eb20ce54e9a9c77e173b`)
- `weights/chime_dtv_weights_k128.bin.manifest.json`
  (`3ab681e85eea44f74d3dd2aed6bcf58660f0452e592aa6a84ad7fac776805062`)

The compact products preserve the reported results and methods, but full
raw-trial regeneration still requires these external artifacts.
