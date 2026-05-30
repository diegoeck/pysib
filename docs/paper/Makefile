MAIN = main

.PHONY: all article clean

all: article

article: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib
	pdflatex -interaction=nonstopmode $(MAIN).tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true
	bibtex $(MAIN) 2>&1 | grep -E "Warning|Error" || true
	pdflatex -interaction=nonstopmode $(MAIN).tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true
	pdflatex -interaction=nonstopmode $(MAIN).tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out $(MAIN).pdf
