# JATIS-style Paper 1 Draft

Working LaTeX draft for the detector/implementation paper.

## Files

- `main.tex` -- manuscript draft.
- `references.bib` -- bibliography database.
- `main.pdf` -- compiled preview PDF.
- `figures/` -- current `paper1_small` figure PDFs copied with stable names.

## Target journal

Primary target: Journal of Astronomical Telescopes, Instruments, and Systems (JATIS).

This draft uses a generic `article` preamble for portability. Before submission, replace the preamble with the official SPIE/JATIS journal template.

## Current scope

The draft is written around the current `paper1_small` scope:

- calibrated K=128, guard=4 pilot-tone F-statistic detector;
- null/CFAR validation;
- detection sensitivity;
- robustness diagnostics;
- fixed-point/CUDA prototype characterization;
- single-segment recorded-data demonstration.

The manuscript intentionally does **not** claim archive-scale validation.

## Main TODOs before final submission

1. Add HDF5-to-NPZ conversion manifest and explicitly document stream semantics.
2. Verify the final Fig. 7 runtime metadata/caption use the latest benchmark values.
3. Decide whether to rerun Fig. 4 sensitivity with more injection trials or keep the finite-trial caveat.
4. Add a matched finite-sample baseline comparison, or keep it deferred.
5. Add archive-scale validation when >=7200 s of data are available across multiple RFI regimes.
6. Add code/data availability, acknowledgments, and final author contributions.
7. Convert to the official SPIE/JATIS LaTeX template.

## Build

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```
