# Reproducible dissertation figures

Every active visual in the dissertation has editable source in this bundle.
External figures are generated as vector PDFs by the Python modules in this
directory. The two architecture drawings that are most naturally edited as
LaTeX graphics live in `tikz/` and are included directly by the chapters.

## One-command regeneration

From the dissertation root:

```bash
python3 -m figure_src.generate_all
python3 -m figure_src.audit_figures
make pdf
```

`make all` runs the same sequence automatically. Figure generation deliberately
requires a working LaTeX installation. It fails rather than silently falling
back to a different font.

## Typography and visual grammar

`style.py` is the single Matplotlib style source. It renders every plot label
through LaTeX using T1-encoded Latin Modern, the same family loaded by
`dissertation.tex`. `tikz/figure_styles.tikz` carries the matching TikZ palette
and line conventions while inheriting the document font.

The semantic colors are fixed across the dissertation:

- blue: measured archive or instrument quantity;
- orange: model, assumption, calibration, or transfer;
- green: conditionally feasible or accepted;
- red: failure, rejection, or excision;
- gray: pending, unmeasured, or contextual.

Figure 3.2 additionally uses Basemap only for vector coastline and boundary context; its source coordinates remain the census range and bearing.

All Python figures use a 6.35-inch canvas and are included at 0.98 of the
6.5-inch dissertation text block. This keeps label sizes physically comparable
instead of resizing unrelated canvases to the same width after export.

## Frozen data interface

All tabular inputs live in `data/frozen_export/v1/`. The dissertation does not
import PilotProxy and does not depend on a mutable repository checkout at build
time. Instead, it freezes small, schema-checked exports and applies its own
plotting style.

`data/frozen_export/v1/frozen_data_manifest.json` records for every CSV:

- scientific owner and authority class;
- upstream source or repository commit;
- row count and SHA-256 hash;
- whether the table is authoritative for the present draft; and
- whether an authoritative replacement is still required.

The figure audit verifies every byte and row count against this manifest and
also checks that the manifest inventory exactly matches the CSV dependencies in
`figure_manifest.csv`.

### Importing a newer PilotProxy export

Generate a versioned export in the PilotProxy repository, then import it here:

```bash
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1 --dry-run

python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1
```

The importer verifies the upstream schema, hashes, and row counts; copies all
matching available tables atomically; preserves unavailable bridge tables; and
updates the frozen manifest with the producing repository commit. Add
`--require-complete` for a final archival import.

Five current tables are represented by the PilotProxy export boundary:

- `census_full_500mi.csv` and `census_inner_120mi.csv`;
- `epoch_operating_points.csv`;
- `channel_status.csv`; and
- `bao_policy_case.csv`.

Seven tables remain explicit legacy-artwork or external-model bridges. They are
fully editable and reproducible, but are marked `replacement_required` until
direct archive or forecast exports are supplied.

## Editing workflow

1. Find the figure in `figure_manifest.csv`.
2. Edit its Python function or TikZ file.
3. For scientific values, replace/import the corresponding frozen data export
   rather than embedding numbers in plotting code.
4. Run `python3 -m figure_src.generate_all`.
5. Run `python3 -m figure_src.audit_figures`.
6. Rebuild the dissertation with `make pdf`.

The audit rejects active raster figures, missing sources, missing dependencies,
manifest/hash drift, font substitution, Type 3 fonts, non-embedded fonts, and
palette drift between Matplotlib and TikZ.

## Artwork-recovery utility

`extract_draft_paths.py` repeats the vector-path recovery from the retained
reference PDFs in `legacy_reference/`. It writes the canonical bridge filenames
inside `data/frozen_export/v1/`. It is not part of the normal build and is not a
substitute for a direct analysis export:

```bash
python3 -m figure_src.extract_draft_paths
```
