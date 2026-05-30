MAIN     = main
BUILDDIR = build
PDFLATEX = pdflatex -interaction=nonstopmode

API_SRCS := $(wildcard api/*.tex)
API_PDFS := $(patsubst api/%.tex,$(BUILDDIR)/api/%.pdf,$(API_SRCS))

.PHONY: all clean

all: $(BUILDDIR)/$(MAIN).pdf $(API_PDFS)

$(BUILDDIR)/$(MAIN).pdf: $(MAIN).tex $(API_SRCS)
	@mkdir -p $(BUILDDIR)/api
	$(PDFLATEX) -output-directory=$(BUILDDIR) $(MAIN).tex
	$(PDFLATEX) -output-directory=$(BUILDDIR) $(MAIN).tex
	@cp $(BUILDDIR)/$(MAIN).pdf $(MAIN).pdf

$(BUILDDIR)/api/%.pdf: api/%.tex
	@mkdir -p $(BUILDDIR)/api
	cd api && $(PDFLATEX) -output-directory=../$(BUILDDIR)/api $(notdir $<)

clean:
	rm -rf $(BUILDDIR)
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc $(MAIN).pdf
