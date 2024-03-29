#!/usr/bin/env bash
# data needed to run this script:
# - /usr/share/irsabi_bidsdata and /usr/share/dargcc_bidsdata for make_bids
# - /mnt/data/hendrik/mlebe_data/ for classifier_tester
# - mouse-brain-atlases installed
# need to have run python setup.py develop --user for MLEBE package

if [ ! -d ~/.scratch ]; then
  echo "You seem to be lacking a ~/.scratch/ directory."
  echo "We need this directory in order to process the data, and it needs to be on a volume with 200GB+ space."
  echo "You can simply symlink to a location you would like this to happen (and then re-run this script):
		ln -s /where/you/want/it ~/.scratch"
  exit 1
fi

# This workflow runs with a json configuration file, choose one in configs/ and define it in make_config.py
if [ ! -f ~/.scratch/mlebe/config.json ]; then
  python make_config.py || exit 1
fi

# Write your workflow description here
echo "" > ~/.scratch/mlebe/description.txt

python make_bids.py || exit 1
python preprocess.py || exit 1
python collapse.py || exit 1
python l1.py || exit 1
python manual_overview.py || exit 1
# temp
#python classifier/get_model_data.py || exit 1

mkdir -p ~/.scratch/mlebe/data
python volume_data.py || exit 1
python variance_data.py || exit 1
python smoothness_data.py || exit 1
# temp
#python functional_data.py || exit 1
python l2.py || exit 1
python classifier/build_graph.py || exit 1

mv ~/.scratch/mlebe/preprocessing/masked_work/graph.dot ~/.scratch/mlebe/data/masked_nipype.dot || exit 1
mv ~/.scratch/mlebe/preprocessing/generic_work/graph.dot ~/.scratch/mlebe/data/generic_nipype.dot || exit 1
sh transfer.sh -s ~/.scratch/mlebe -d ../data || exit 1

