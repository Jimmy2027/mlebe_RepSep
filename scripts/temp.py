"""

This file can be deleted!
"""

import numpy as np
import pickle
import gzip
from lib import boilerplate
# from samri.masking.predict_mask import predict_mask

# boilerplate.factorci('Processing[T.Generic]', df_path='data/smoothness.csv', dependent_variable='Smoothness Conservation Factor')

# boilerplate.levene_(dependent_variable='1 - Vcf')
# print(boilerplate.wilcoxon_(dependent_variable='1 - Vcf'))
print(boilerplate.bootstrapped_corecomparison_factorci('Processing[T.Masked]'))
# print(boilerplate.corecomparison_factorci('Processing[T.Masked]:Contrast[T.CBV]', df_path='data/bootstrapped_volume.csv', dependent_variable='RMSE'))
# print(boilerplate.corecomparison_factorci('Intercept', df_path='data/bootstrapped_volume.csv', dependent_variable='RMSE'))
#
# boilerplate.iqr_(dependent_variable='1 - Vcf')
# boilerplate.iqr_(dependent_variable='1 - Vcf', processing = 'Masked')
# predict_mask('/home/hendrik/.scratch/mlebe/bids/sub-4013/ses-ofM/anat/sub-4013_ses-ofM_acq-TurboRARElowcov_T2w.nii.gz')
