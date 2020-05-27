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

if [ ! -d ~/.scratch/mlebe/dargcc_bids ]; then
  if [ -d '/usr/share/dargcc_bidsdata' ]; then
    ln -s '/usr/share/dargcc_bidsdata' ~/.scratch/mlebe/dargcc_bids
  else
    echo "No DARGCC BIDS data distribution found, processing from scanner IRSABI data:"
    exit
  fi
fi

ln -s /home/hendrik/.scratch/mlebe_final/classifiers /home/hendrik/.scratch/mlebe/classifiers
mkdir -p ~/.scratch/mlebe/preprocessing/generic
ln -s ~/.scratch/irsabi/preprocessing/generic/* ~/.scratch/mlebe/preprocessing/generic/

if [ ! -f ~/.scratch/mlebe/uid.json ]; then
  python config.py || exit 1
fi

if [ ! -d ~/.scratch/mlebe/classifiers ]; then
  python classifier/move_classifier_data.py
  exit 1
fi

#cp config.py ~/.scratch/mlebe/
#echo " With irsabi as training data " >~/.scratch/mlebe/description.txt
#python preprocess.py || exit 1
#python collapse.py || exit 1
#python l1.py || exit 1
#python manual_overview.py || exit 1
#python classifier/classifier_tester.py || exit 1

#mkdir -p ~/.scratch/mlebe/data
#python volume_data.py || exit 1
#python variance_data.py || exit 1
#python smoothness_data.py || exit 1
#python functional_data.py || exit 1
#python l2.py || exit 1
sh transfer.sh || exit 1
