#!/usr/bin/env bash

#jupyter nbconvert --to notebook --execute qualitative_reg_ev.ipynb && jupyter nbconvert --to html qualitative_reg_ev.nbconvert.ipynb

jupyter nbconvert --to notebook --execute qualitative_reg_ev_func.ipynb && jupyter nbconvert --to html qualitative_reg_ev_func.nbconvert.ipynb

#cp *.html ~/.scratch/mlebe

jupyter nbconvert --to notebook --execute homework_11_and_12.ipynb && jupyter nbconvert --to html homework_11_and_12.nbconvert.ipynb