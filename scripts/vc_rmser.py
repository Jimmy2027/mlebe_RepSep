import pandas as pd
from os import path
from lib.utils import float_to_tex
from sklearn.metrics import mean_squared_error
from math import sqrt

volume_path = path.abspath('data/volumes.csv')
df = pd.read_csv(volume_path)

legacy = df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Volume Change Factor'].tolist()
generic = df.loc[(df['Processing']=='Generic') & (df['Template']=='Generic'), 'Volume Change Factor'].tolist()

rmse_legacy = sqrt(mean_squared_error([1]*len(legacy), legacy))
rmse_generic = sqrt(mean_squared_error([1]*len(generic), generic))

print(float_to_tex(rmse_legacy/rmse_generic, max_len=2, condensed=True))
