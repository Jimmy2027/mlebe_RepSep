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
		mkdir -p ~/.scratch/mlebe/bids
		ln -s /usr/share/irsabi_bidsdata/* ~/.scratch/mlebe/bids/
	else
		echo "No IRSABI BIDS data distribution found, processing from scanner IRSABI data:"
		python make_bids.py
	fi
fi

ln -s /home/hendrik/.scratch/mlebe_final/classifiers /home/hendrik/.scratch/mlebe/classifiers
mkdir -p ~/.scratch/mlebe/preprocessing/generic
ln -s ~/.scratch/irsabi/preprocessing/generic/* ~/.scratch/mlebe/preprocessing/generic/

if [ ! -d ~/.scratch/mlebe/classifiers ]; then
  python classifier/move_classifier_data.py
  exit 1
fi

echo config.py > ~/.scratch/mlebe/description.txt
#echo " Write your experiment description here " > ~/.scratch/mlebe/description.txt
#python config.py || exit 1
#python preprocess.py || exit 1
#python collapse.py || exit 1
python l1.py || exit 1
python manual_overview.py || exit 1
python classifier/classifier_tester.py || exit 1

mkdir -p ~/.scratch/mlebe/data
python volume_data.py || exit 1
python variance_data.py || exit 1
python smoothness_data.py || exit 1
python functional_data.py || exit 1
python l2.py || exit 1
mkdir -p ../data/manual_overview/generic
cp -v ~/.scratch/mlebe/manual_overview/generic/coherence_4001_cbv.pdf ../data/manual_overview/generic/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/generic/4001_ofMcF2_T2w.pdf ../data/manual_overview/generic/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/generic/4001_ofMcF2_cbv.pdf ../data/manual_overview/generic/ || exit 1

mkdir -p ../data/manual_overview/masked
cp -v ~/.scratch/mlebe/manual_overview/masked/coherence_4001_cbv.pdf ../data/manual_overview/masked/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/masked/4001_ofMcF2_T2w.pdf ../data/manual_overview/masked/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/masked/4001_ofMcF2_cbv.pdf ../data/manual_overview/masked/ || exit 1

cp -v ~/.scratch/mlebe/classifiers/T2/y_test_pred.npy ../data/classifier/ || exit 1
cp -v ~/.scratch/mlebe/classifiers/T2/dice_score.txt ../data/classifier/dice_score.txt || exit 1
cp -v ~/.scratch/mlebe/preprocessing/masked_work/graph.dot ../data/masked_nipype.dot || exit 1
cp -v ~/.scratch/mlebe/preprocessing/generic_work/graph.dot ../data/generic_nipype.dot || Truem
rsync -avP --exclude='*_cope.nii*' --exclude='*_zstat.nii*' ~/.scratch/mlebe/*l2* ../data/ || exit 1
rsync -avP ~/.scratch/mlebe/data/ ../data || exit 1
