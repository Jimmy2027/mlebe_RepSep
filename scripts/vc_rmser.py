import pandas as pd
from os import path
from lib.utils import float_to_tex
from sklearn.metrics import mean_squared_error
from math import sqrt

volume_path = path.abspath('data/volume.csv')
df = pd.read_csv(volume_path)

generic_masked = df.loc[(df['Processing']=='Generic Masked'), 'Volume Conservation Factor'].tolist()
# temp = df.loc[(df['Processing']=='Generic Masked')]
# temp.to_csv('scripts/meeeh.csv')
# temp = df.loc[(df['Processing']=='Generic Masked'), 'Volume Conservation Factor']
# print(df)
# print(temp.idxmax(), temp.max())
# print(temp.idxmin(), temp.min())
generic = df.loc[(df['Processing']=='Generic'), 'Volume Conservation Factor'].tolist()

rmse_generic_masked = sqrt(mean_squared_error([1]*len(generic_masked), generic_masked))
rmse_generic = sqrt(mean_squared_error([1]*len(generic), generic))

print(float_to_tex(rmse_generic_masked/rmse_generic, max_len=2, condensed=True))
