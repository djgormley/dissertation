PYTHON ?= python3
LATEX ?= pdflatex
LATEXFLAGS ?= -interaction=nonstopmode -halt-on-error
SOURCE_DATE_EPOCH ?= 1786492800
FORCE_SOURCE_DATE ?= 1
export SOURCE_DATE_EPOCH FORCE_SOURCE_DATE

.PHONY: all figures figure-audit pdf verify clean distclean

all: pdf figure-audit

figures:
	MPLBACKEND=Agg $(PYTHON) -m figure_src.generate_all

figure-audit: figures
	$(PYTHON) -m figure_src.audit_figures

pdf: figures
	$(LATEX) $(LATEXFLAGS) dissertation.tex
	$(LATEX) $(LATEXFLAGS) dissertation.tex
	$(LATEX) $(LATEXFLAGS) dissertation.tex

verify: all

clean:
	rm -f dissertation.aux dissertation.log dissertation.toc dissertation.lof \
	      dissertation.lot dissertation.out dissertation.fls dissertation.fdb_latexmk \
	      chapters/*.aux
	rm -rf figure_src/__pycache__

distclean: clean
	rm -f dissertation.pdf
