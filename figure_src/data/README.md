# Dissertation figure data

The active figure generators read only from `frozen_export/v1/`. That directory is a frozen, hash-checked data interface: it contains small CSV exports, not analysis code or raw products.

- `frozen_export/v1/frozen_data_manifest.json` records ownership, authority, row counts, hashes, and replacement status.
- `frozen_export/v1/README.md` explains the import workflow.
- `frozen_export/v1/legacy_recovery_provenance.md` documents the temporary vector-artwork recovery bridge.

Do not add a second loose copy of a table in this directory. Import a versioned PilotProxy export with `python3 -m figure_src.import_dissertation_export ...` so the manifest is updated atomically.
