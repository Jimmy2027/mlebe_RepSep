#!/usr/bin/env bash

if [ ! -d ~/.scratch ]; then
	echo "You seem to be lacking a ~/.scratch/ directory."
	echo "We need this directory in order to process the data, and it needs to be on a volume with 200GB+ space."
	echo "You can simply symlink to a location you would like this to happen (and then re-run this script):
		ln -s /where/you/want/it ~/.scratch"
	exit 1
fi

if [ ! -d ~/.scratch/irsabi/bids ]; then
	if [ -d '/usr/share/irsabi_bidsdata' ]; then
		[ -d ~/.scratch/irsabi ] || mkdir ~/.scratch/irsabi
		ln -s '/usr/share/irsabi_bidsdata' ~/.scratch/irsabi/bids
	else
		echo "No IRSABI BIDS data distribution found, processing from scanner IRSABI data:"
		SAMRI bru2bids -o ~/.scratch/irsabi/ -f '{"acquisition":["EPIlowcov"]}' -s '{"acquisition":["TurboRARElowcov"]}' '/usr/share/irsabi_data/'
	fi
fi

python preprocess.py || exit 1
python collapse.py || exit 1
python volume_data.py || exit 1
python variance_data.py || exit 1
python smoothness_data.py || exit 1
python legacy_background_fix.py || exit 1
python l1.py || exit 1
python functional_data.py || exit 1
python l2.py || exit 1
python manual_overview.py || exit 1
cp ~/.scratch/irsabi/manual_overview/generic/coherence_4009_cbv.pdf ../data/ || exit 1
cp ~/.scratch/irsabi/manual_overview/generic/4007_ofMcF2_cbv.pdf ../data/ || exit 1
