compile:
	rm -rf *.aux *.bbl *.blg *.log *.toc
	pdflatex TMOS.tex
	bibtex TMOS
	pdflatex TMOS.tex
	pdflatex TMOS.tex
	pdflatex TMOS.tex

support:
	rm -rf *.aux *.bbl *.blg *.log *.toc
	pdflatex TMOS_support.tex
	bibtex TMOS_support
	pdflatex TMOS_support.tex
	pdflatex TMOS_support.tex
	pdflatex TMOS_support.tex


follow:
	latexmk -pvc -pdf -bibtex -pdflatex="pdflatex --shell-escape %O %S" TMOS.tex

wordcount:
	texcount -utf8 -total -sum TMOS.tex

clean:
	rm -f *.aux
	rm -f *.fdb_latexmk
	rm -f *.fls
	rm -f *.log
	rm -f *.bbl
	rm -f *.blg
	rm -f *.out
	rm -f *.brf
	rm -f *.acn
	rm -f *.glg
	rm -f *.glo
	rm -f *.gls
	rm -f *.ist
	rm -f *.lof
	rm -f *.lot
	rm -f *.toc
	rm -f *.bcf
	rm -f *.run.xml
