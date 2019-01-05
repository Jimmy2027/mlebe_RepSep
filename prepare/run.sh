#!/usr/bin/env bash

if [ ! -d ~/data_scratch ]; then
	echo "You seem to be lacking a ~/data_scratch/ directory."
	echo "We need this directory in order to process the data, and it needs to be on a volume with 200GB+ space."
	echo "You can simply symlink to a location you would like this to happen (and then re-run this script):
		ln -s /where/you/want/it ~/data_scratch"
	exit 1
fi

if [ ! -d ~/data_scratch/irsabi/bids ]; then
	if [ -d "/usr/share/irsabi_bidsdata" ]; then
		[ -d ~/data_scratch/irsabi ] || mkdir ~/data_scratch/irsabi
		ln -s /usr/share/irsabi_bidsdata ~/data_scratch/irsabi/bids
	else
		echo "No IRSABI BIDS data distribution found, processing from scanner IRSABI data:"
		SAMRI bru2bids -o ~/data_scratch/irsabi/ -f '{"acquisition":["EPIlowcov"]}' -s '{"acquisition":["TurboRARElowcov"]}' /usr/share/irsabi_data/
	fi
fi

echo "i"
exit 1

python preprocess.py || exit 1
python collapse.py || exit 1
python volume_data.py || exit 1
python legacy_background_fix.py || exit 1
python glm.py || exit 1
python functional_data.py || exit 1
python l2_maps.py || exit 1
