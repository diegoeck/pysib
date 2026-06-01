TEX = TEXINPUTS=.:./ifacconf_latex//: BSTINPUTS=.:./ifacconf_latex//: BIBINPUTS=.:../paper-toms//:

main.pdf: main.tex
	$(TEX) pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true
	$(TEX) bibtex main 2>&1 | grep -E "Warning|Error" || true
	$(TEX) pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true
	$(TEX) pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^!|Warning|Error|Overfull|Underfull" || true

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.pdf
