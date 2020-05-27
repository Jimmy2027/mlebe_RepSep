"""

This file can be deleted!
"""

import numpy as np
import pickle
import gzip
from lib import boilerplate
from prepare.utils import bootstrapping
import prepare.config as config

scratch_dir = config.scratch_dir
# from samri.masking.predict_mask import predict_mask
print('******* Volume *******')
boilerplate.corecomparison_factorci('Processing[T.Masked]:Contrast[T.T2w+CBV]', df_path='data/smoothness.csv', dependent_variable='Smoothness Conservation Factor')
# bootstrapping.bootstrap_analysis('volume', dependent_variable='VCF_RMSE', expression='Processing*Contrast',
#                                  scratch_dir=scratch_dir)
# boilerplate.bootstrapped_corecomparison_factorci('Processing[T.Masked]')
# boilerplate.bootstrapped_corecomparison_factorci('Processing[T.Masked]:Contrast[T.CBV]')
# boilerplate.fstatistic('Processing', df_path='data/bootstrapped/bootstrapped_volume.csv', dependent_variable='VCF_RMSE',
#                        condensed=True)
#
# print('******* Smoothing *******')
# boilerplate.bootstrapped_corecomparison_factorci('Processing[T.Masked]', metric='smoothness')
# boilerplate.bootstrapped_corecomparison_factorci('Processing[T.Masked]:Contrast[T.CBV]', metric='smoothness')
# boilerplate.fstatistic('Processing', df_path='data/bootstrapped/bootstrapped_smoothness.csv',
#                        dependent_variable='SCF_RMSE',
#                        condensed=True)

# boilerplate.levene_(dependent_variable='1 - Vcf')
# print(boilerplate.wilcoxon_(dependent_variable='1 - Vcf'))
# print(boilerplate.bootstrapped_corecomparison_factorci('Processing[T.Masked]'))
# print(boilerplate.corecomparison_factorci('Processing[T.Masked]:Contrast[T.CBV]', df_path='data/bootstrapped_volume.csv', dependent_variable='RMSE'))
# print(boilerplate.corecomparison_factorci('Intercept', df_path='data/bootstrapped_volume.csv', dependent_variable='RMSE'))
#
# boilerplate.iqr_(dependent_variable='1 - Vcf')
# boilerplate.iqr_(dependent_variable='1 - Vcf', processing = 'Masked')
# predict_mask('/home/hendrik/.scratch/mlebe/bids/sub-4013/ses-ofM/anat/sub-4013_ses-ofM_acq-TurboRARElowcov_T2w.nii.gz')
