#!/usr/bin/env bash

TARGET="${2}"
SCRATCH_DIR="${1}"

WHITELIST="
	article_ieeetm.tex
	"
if [["$SCRATCH_DIR" == ""]]; then
  scratch_dir=~/.scratch/mlebe_threed
else
   scratch_dir=~/.scratch/${SCRATCH_DIR}
fi

# get all the necessary data from the preprocessing
#sh prepare/transfer.sh -s ${scratch_dir} -d data || exit

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
#	bibtex ${TARGET} &&\
	biber ${TARGET} &&\
	pdflatex -shell-escape ${TARGET}.tex &&\
	pdflatex -shell-escape ${TARGET}.tex
fi

rm auto_fig_py*
cp article.pdf $scratch_dir