"""

This file can be deleted!
"""

import numpy as np
import pickle
import gzip
from lib import boilerplate
# from samri.masking.predict_mask import predict_mask
from temp_ import predict_mask

boilerplate.factorci('Processing[T.Generic]', df_path='data/smoothness.csv', dependent_variable='Smoothness Conservation Factor')

# boilerplate.levene_(dependent_variable='1 - Vcf')
# boilerplate.wilcoxon_(dependent_variable='1 - Vcf')
#
# boilerplate.iqr_(dependent_variable='1 - Vcf')
# boilerplate.iqr_(dependent_variable='1 - Vcf', processing = 'Generic Masked')
# predict_mask('/home/hendrik/.scratch/mlebe/bids/sub-4013/ses-ofM/anat/sub-4013_ses-ofM_acq-TurboRARElowcov_T2w.nii.gz')
