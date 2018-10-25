#!/usr/bin/env bash

python make_bids.py || exit 1
python preprocess.py || exit 1
python collapse.py || exit 1
python volume_data.py || exit 1
