# Recovered draft-figure data provenance

The supplied dissertation contained scientific curves whose authoritative
arrays and original plotting programs were not included.  The CSVs in this
directory were recovered from vector paths by `extract_draft_paths.py`.
They preserve the supplied draft artwork and make every figure editable;
they are not a replacement for direct exports from the analysis pipeline.

When direct result tables are archived, replace the corresponding CSV while
keeping the generator and styling layer unchanged.

## Reference PDFs

| file | SHA-256 |
|---|---|
| `fig_bao_convergence_original.pdf` | `36b22d1aea7ef815e34c9f0f4a1b288ab21f4296241aa4fa230cf03c956301fa` |
| `fig_bao_the_case_original.pdf` | `2bc0acb1f9d5241d509686793a5a5ae804a3fb23231d811af95325da6cede046` |
| `fig_bao_time_vs_masking_original.pdf` | `7f859e93c8d3135c90b622523e7d84f4b8663a3fa450bb63172d71f3f1645534` |
| `fig_bao_two_walls_original.pdf` | `3de6513ffc44ecf13c7aaa61284c9c7fda1317d66092cd277335d0d801a7bebc` |
| `fig_census_psd_original.pdf` | `754bf99638a6edbd75d129ef888408e785d46b57063602b9f7a7a7dd8dd7ee99` |
| `fig_intro_wiggle_original.pdf` | `c59bf1fc6af06c762ceb5d1c06e04806dbc742d7c06065b365fc4dc13dc6e535` |
| `fig_worked_example_original.pdf` | `1e4724519cc9f8e404e9446241ccdd540436453a0fcdd6db1637dc3108cccd81` |

## Recovered tables

- `intro_wiggle_*.csv`: CAMB-derived pedagogical curves.
- `worked_example_spectra.csv`: the two plotted fine spectra; the vertical
  transform is anchored to the medians and maxima printed in the draft.
- `census_psd.csv`: ten archive-averaged spectra in Chapter 3.
- `bao_time_vs_masking.csv`: the three mask-cost curves.
- `bao_convergence.csv`: clean-error and bias-significance curves.
- `bao_two_walls.csv`: ten threshold-sweep curves.
