PYTHON ?= python3
LATEX ?= pdflatex
LATEXFLAGS ?= -interaction=nonstopmode -halt-on-error
SOURCE_DATE_EPOCH ?= 1786492800
FORCE_SOURCE_DATE ?= 1
export SOURCE_DATE_EPOCH FORCE_SOURCE_DATE

.PHONY: all figures figure-audit evidence-audit pdf test manifest manifest-check verify clean distclean

all: pdf figure-audit evidence-audit

figures:
	MPLBACKEND=Agg $(PYTHON) -m figure_src.generate_all

figure-audit: figures
	$(PYTHON) -m figure_src.audit_figures

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

evidence-audit:
	$(PYTHON) -B scripts/verify_vendored_evidence.py

pdf: figures
	$(LATEX) $(LATEXFLAGS) dissertation.tex
	$(LATEX) $(LATEXFLAGS) dissertation.tex
	$(LATEX) $(LATEXFLAGS) dissertation.tex

manifest: all test
	$(PYTHON) scripts/release_manifest.py --write

manifest-check:
	$(PYTHON) scripts/release_manifest.py

verify: all test
	$(MAKE) manifest-check

clean:
	rm -f dissertation.aux dissertation.log dissertation.toc dissertation.lof \
	      dissertation.lot dissertation.out dissertation.fls dissertation.fdb_latexmk \
	      dissertation.synctex.gz chapters/*.aux
	rm -rf figure_src/__pycache__ scripts/__pycache__ tests/__pycache__

distclean: clean
	rm -f dissertation.pdf
