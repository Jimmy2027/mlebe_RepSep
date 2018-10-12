#!/usr/bin/env bash

python make_bids.py || exit 1
python preprocess_base.py || exit 1
python volume_data.py || exit 1
