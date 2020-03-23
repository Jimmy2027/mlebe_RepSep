#!/usr/bin/env bash

TARGET="${1}"
WHITELIST="
	article.tex
	"

if [[ $TARGET = "all" ]] || [[ "$TARGET" == "" ]]; then
	for ITER_TARGET in *.tex; do
		if [[ $WHITELIST =~ (^|[[:space:]])$ITER_TARGET($|[[:space:]]) ]];then
			ITER_TARGET=${ITER_TARGET%".tex"}
			./compile.sh ${ITER_TARGET}
		fi
	done
else
	pdflatex -shell-escape ${TARGET}.tex &&\
	pythontex.py ${TARGET}.tex &&\
	pdflatex -shell-escape ${TARGET}.tex &&\
	bibtex ${TARGET} &&\
	pdflatex -shell-escape ${TARGET}.tex &&\
	pdflatex -shell-escape ${TARGET}.tex
fi

mv auto_fig_py* Auto_fig_py/