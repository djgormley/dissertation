# Build instructions

## Included output

`dissertation.pdf` is the compiled dissertation. Bundle-scope figure PDFs
are regenerated and audited from source by the normal build. Repository-owned
result figures and all-channel diagnostic atlases (see `FIGURE_SOURCES.md`)
are vendored as finished PDFs and audited for provenance, fonts, page count,
format, and any explicitly declared raster content, but are not regenerated
here.

## Requirements

### LaTeX

- a current TeX Live installation with `pdflatex`, `latex`, and `dvipng`;
- packages used by `dissertation.tex`, including `amsmath`, `amssymb`,
  `booktabs`, `graphicx`, `tikz`, `lmodern`, `microtype`, `xcolor`, `array`,
  `tabularx`, `longtable`, `multirow`, `pdflscape`, `enumitem`, `url`, and
  `hyperref`.

The figure generator intentionally requires LaTeX so Matplotlib labels use the
same T1-encoded Latin Modern fonts as the dissertation.

### Python

Install the packages in `requirements-figures.txt`. Basemap and its boundary dataset are required for the vector geographic context in Figure 3.2. PyMuPDF is required only to
repeat the documented artwork-recovery step; it is not needed for ordinary
figure regeneration.

### Audit utilities

The audit uses the Poppler commands `pdffonts`, `pdfimages`, and `pdfinfo`.

## Recommended build

```bash
make all
```

Equivalent explicit commands are:

```bash
export SOURCE_DATE_EPOCH=1786492800
export FORCE_SOURCE_DATE=1
MPLBACKEND=Agg python3 -m figure_src.generate_all
pdflatex -interaction=nonstopmode -halt-on-error dissertation.tex
pdflatex -interaction=nonstopmode -halt-on-error dissertation.tex
pdflatex -interaction=nonstopmode -halt-on-error dissertation.tex
python3 -m figure_src.audit_figures
python3 -B scripts/verify_vendored_evidence.py
```

The bibliography is maintained as a LaTeX `thebibliography` environment, so no
BibTeX or Biber pass is required. The fixed `SOURCE_DATE_EPOCH` and figure PDF
metadata make repeated builds byte-for-byte reproducible when the toolchain and
inputs are unchanged.

## Figure-only editing cycle

```bash
python3 -m figure_src.generate_all
python3 -m figure_src.audit_figures
```

See `figure_src/README.md` and `figure_src/figure_manifest.csv` to locate the
source and frozen data dependency for any visual.

## Updating scientific data from PilotProxy

The normal build never reads a live repository checkout. First create a
versioned PilotProxy export, then import it into this bundle:

```bash
# In pilot-proxy
PYTHONPATH=src python -m pilot_proxy.dissertation_exports \
  --output-dir exports/dissertation/v1

# In this dissertation bundle
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1 --dry-run
python3 -m figure_src.import_dissertation_export \
  /path/to/pilot-proxy/exports/dissertation/v1
make all
```

The importer verifies the upstream manifest and updates
`figure_src/data/frozen_export/v1/frozen_data_manifest.json` atomically. Use
`--require-complete` for a final archival import.

## Repeating the artwork-recovery bridge

This is not part of the normal build:

```bash
python3 -m figure_src.extract_draft_paths
```

It reconstructs the temporary bridge CSVs from retained vector reference PDFs.
Direct analysis exports should supersede those tables before final archival
publication.

## Cleanup

```bash
make clean
```

This removes LaTeX auxiliary files and Python bytecode caches but preserves the
compiled dissertation, generated figures, and frozen data. Use `make distclean`
to remove the compiled PDF as well.
