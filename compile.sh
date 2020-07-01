#!/usr/bin/env bash

TARGET="${1}"
WHITELIST="
	article.tex
	"
scratch_dir=~/.scratch/mlebe_threed/
data_path=${scratch_dir}data/*
cp -r $data_path data/
cp -r "${scratch_dir}classifiers" data/
cp "${scratch_dir}config.json" data/

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

rm auto_fig_py*
cp article.pdf $scratch_dir