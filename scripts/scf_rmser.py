import pandas as pd
from os import path
from lib.utils import float_to_tex
from sklearn.metrics import mean_squared_error
from math import sqrt

volume_path = path.abspath('data/smoothness.csv')
df = pd.read_csv(volume_path)

#legacy = df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Smoothness Conservation Factor'].tolist()
#generic = df.loc[(df['Processing']=='Generic') & (df['Template']=='Generic'), 'Smoothness Conservation Factor'].tolist()
generic_masked = df.loc[(df['Processing']=='Generic Masked'), 'Smoothness Conservation Factor'].tolist()
generic = df.loc[(df['Processing']=='Generic'), 'Smoothness Conservation Factor'].tolist()

rmse_generic_masked = sqrt(mean_squared_error([1]*len(generic_masked), generic_masked))
rmse_generic = sqrt(mean_squared_error([1]*len(generic), generic))

print(float_to_tex(rmse_generic_masked/rmse_generic, max_len=2, condensed=True))
