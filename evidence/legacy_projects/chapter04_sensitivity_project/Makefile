all: figures pdf

figures:
	python make_figures_and_tables.py

pdf: figures
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex
	cp main.pdf chapter04_sensitivity.pdf

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk main.pdf chapter04_sensitivity.pdf
