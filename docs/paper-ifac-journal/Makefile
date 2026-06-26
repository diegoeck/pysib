TEX = TEXINPUTS=.:ifacconf_latex//: BSTINPUTS=.:ifacconf_latex//: BIBINPUTS=.:

all: main.pdf cover-letter.pdf title-page.pdf

main.pdf: main.tex references.bib
	$(TEX) pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true
	$(TEX) bibtex main 2>&1 | grep -E "Warning|Error" || true
	$(TEX) pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true
	$(TEX) pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true

cover-letter.pdf: cover-letter.tex
	pdflatex -interaction=nonstopmode cover-letter.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true

title-page.pdf: title-page.tex
	pdflatex -interaction=nonstopmode title-page.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.pdf
	rm -f cover-letter.aux cover-letter.log cover-letter.pdf
	rm -f title-page.aux title-page.log title-page.pdf
