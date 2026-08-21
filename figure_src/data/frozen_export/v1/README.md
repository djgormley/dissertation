# Frozen dissertation data interface

This directory contains the exact small tables used by the dissertation's own
figure generators. It is intentionally independent of a live PilotProxy
checkout. `frozen_data_manifest.json` records ownership, authority, source
class, row counts, and SHA-256 hashes.

Since the August 2026 reorganization the repositories own every data-backed
figure and vendor finished PDFs into `figs/`; only four tables remain here:

- `census_full_500mi.csv` / `census_inner_120mi.csv` — the transmitter-census
  export behind Figure 3.2 (rendered here until its generator completes its
  move to `WVURAIL/dtv-station-census`). Both preserve the upstream
  `schema_version` and per-row `evidence_status`; the full table's 11
  `licensed_candidate` rows are an inclusive maximum-envelope scenario, not
  reported active emitters.
- `intro_wiggle_correlation.csv` / `intro_wiggle_power.csv` — the pedagogical
  wiggle curves, still legacy-artwork bridges pending the CAMB-or-accept
  decision.

Future authoritative PilotProxy exports can be imported with:

```bash
python3 -m figure_src.import_dissertation_export /path/to/exports/dissertation/v1
```

The importer verifies the upstream manifest, immutable source commit, and
hashes before replacing any matching table. `last_import.json` records a
portable repository/commit identity and export-manifest hash rather than the
importing machine's path.
The dissertation continues to own plotting code, typography,
and visual conventions for the figures in its scope.
