import pandas as pd
from utils.bootstrapping import bootstrap, bootstrap_analysis
import nibabel as nib
# df = pd.read_csv('../data/smoothness.csv')
# bootstrap(df, 'Smoothness Conservation Factor')
# bootstrap_analysis('smoothness',dependent_variable = 'RMSE',expression = 'Processing*Contrast')
# # df = pd.read_csv('../data/volume.csv')
# # bootstrap(df, 'Volume Conservation Factor')
# bootstrap_analysis('volume',dependent_variable = 'RMSE',expression = 'Processing*Contrast')
image = nib.load('/mnt/scratch/mlebe/preprocessing/masked_work/_ind_type_124/s_mask/masked_output.nii.gz').get_data()
print(image.shape)
mask = nib.load('/mnt/scratch/mlebe/preprocessing/masked_work/_ind_type_124/s_mask/resampled_mask.nii.gz').get_data()
print(mask.shape)

