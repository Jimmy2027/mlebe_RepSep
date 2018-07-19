pdflatex -shell-escape article.tex && pythontex.py article.tex && pdflatex -shell-escape article.tex && bibtex article && pdflatex -shell-escape article.tex && pdflatex -shell-escape article.tex

