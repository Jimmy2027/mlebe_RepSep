import pandas as pd
from os import path
from lib.utils import float_to_tex
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np

volume_path = path.abspath('data/volume.csv')
df = pd.read_csv(volume_path)

generic_masked = df.loc[(df['Processing']=='Masked'), 'Volume Conservation Factor'].tolist()
generic = df.loc[(df['Processing']=='Generic'), 'Volume Conservation Factor'].tolist()
d_generic_masked = np.add(-1, generic_masked)
d_generic = np.add(-1, generic)

rmse_generic_masked = sqrt(mean_squared_error([1]*len(generic_masked), generic_masked))
rmse_generic = sqrt(mean_squared_error([1]*len(generic), generic))

print(float_to_tex(rmse_generic_masked/rmse_generic, max_len=2, condensed=True))