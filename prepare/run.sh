#!/usr/bin/env bash

if [ ! -d ~/.scratch ]; then
	echo "You seem to be lacking a ~/.scratch/ directory."
	echo "We need this directory in order to process the data, and it needs to be on a volume with 200GB+ space."
	echo "You can simply symlink to a location you would like this to happen (and then re-run this script):
		ln -s /where/you/want/it ~/.scratch"
	exit 1
fi

if [ ! -d ~/.scratch/mlebe/bids ]; then
	if [ -d '/usr/share/irsabi_bidsdata' ]; then
		[ -d ~/.scratch/mlebe ] || mkdir ~/.scratch/mlebe
		ln -s '/usr/share/irsabi_bidsdata' ~/.scratch/mlebe/bids
	else
		echo "No IRSABI BIDS data distribution found, processing from scanner IRSABI data:"
		python make_bids.py
	fi
fi

python preprocess.py || exit 1
python collapse.py || exit 1
python volume_data.py || exit 1
python variance_data.py || exit 1
python smoothness_data.py || exit 1
#python legacy_background_fix.py || exit 1
python l1.py || exit 1
python functional_data.py || exit 1
python l2.py || exit 1
python manual_overview.py || exit 1
mkdir -p ../data/manual_overview/generic
cp ~/.scratch/mlebe/manual_overview/generic/coherence_4008_cbv.pdf ../data/manual_overview/generic/ || exit 1
cp ~/.scratch/mlebe/manual_overview/generic/4008_ofMcF1_T2w.pdf ../data/manual_overview/generic/ || exit 1
cp ~/.scratch/mlebe/manual_overview/generic/4008_ofMcF1_cbv.pdf ../data/manual_overview/generic/ || exit 1

mkdir -p ../data/manual_overview/generic_mask
cp ~/.scratch/mlebe/manual_overview/generic_mask/coherence_4008_cbv.pdf ../data/manual_overview/generic/ || exit 1
cp ~/.scratch/mlebe/manual_overview/generic_mask/4008_ofMcF1_T2w.pdf ../data/manual_overview/generic_mask/ || exit 1
cp ~/.scratch/mlebe/manual_overview/generic_mask/4008_ofMcF1_cbv.pdf ../data/manual_overview/generic_mask/ || exit 1
