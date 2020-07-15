#!/usr/bin/env bash

if [ ! -d ~/.scratch ]; then
	echo "You seem to be lacking a ~/.scratch/ directory."
	echo "We need this directory in order to process the data, and it needs to be on a volume with 200GB+ space."
	echo "You can simply symlink to a location you would like this to happen (and then re-run this script):
		ln -s /where/you/want/it ~/.scratch"
	exit 1
fi

if [ ! -d ~/.scratch/mlebe/bids ]; then
  mkdir -p ~/.scratch/mlebe/bids
  python test_on_blacklisted/get_bl_data.py || exit 1
fi

#if [ ! -d ~/.scratch/mlebe/classifiers ]; then
#  echo "no classifiers found, please link them to the scratch directory"
#  exit 1
#fi


#echo " Write your experiment description here " > ~/.scratch/mlebe/description.txt
echo "testing on blacklisted data" > ~/.scratch/mlebe/description.txt

python preprocess_bl.py || exit 1

mkdir ../data/blacklist_comparison
mv ~/.scratch/mlebe/preprocessing/* ../data/blacklist_comparison/
rm -r ~/.scratch/mlebe