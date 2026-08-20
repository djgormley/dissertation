# Dissertation Chapter 4: Synthetic Signal Model and Detection Sensitivity

Standalone LaTeX project for dissertation Chapter 4. The chapter expands the article-scale detection sensitivity result into a dissertation-scale discussion of the injection signal model, pilot-to-shelf normalization, Monte Carlo grid, detection probability, finite-trial support, and sensitivity scaling.

## Build

```bash
make
```

or manually:

```bash
python make_figures_and_tables.py
pdflatex main.tex
pdflatex main.tex
```

The compiled PDF is `chapter04_sensitivity.pdf`.
