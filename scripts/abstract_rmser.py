import pandas as pd
from os import path
from lib.utils import float_to_tex
from sklearn.metrics import mean_squared_error
from math import sqrt

s_path = path.abspath('data/smoothness.csv')
s_df = pd.read_csv(s_path)

s_legacy = s_df.loc[(s_df['Processing']=='Generic Masked') & (s_df['Template']=='Generic Masked'), 'Smoothness Conservation Factor'].tolist()
s_generic = s_df.loc[(s_df['Processing']=='Generic') & (s_df['Template']=='Generic'), 'Smoothness Conservation Factor'].tolist()

s_rmse_legacy = sqrt(mean_squared_error([1]*len(s_legacy), s_legacy))
s_rmse_generic = sqrt(mean_squared_error([1]*len(s_generic), s_generic))

v_path = path.abspath('data/volume.csv')
v_df = pd.read_csv(v_path)

v_legacy = v_df.loc[(v_df['Processing']=='Generic Masked') & (v_df['Template']=='Generic Masked'), 'Volume Conservation Factor'].tolist()
v_generic = v_df.loc[(v_df['Processing']=='Generic') & (v_df['Template']=='Generic'), 'Volume Conservation Factor'].tolist()

v_rmse_legacy = sqrt(mean_squared_error([1]*len(v_legacy), v_legacy))
v_rmse_generic = sqrt(mean_squared_error([1]*len(v_generic), v_generic))

s = int(round(s_rmse_legacy/s_rmse_generic))
v = int(round(s_rmse_legacy/s_rmse_generic))

if s == v:
	print("{}-fold".format(s))
else:
	print("{}-fold and {}-fold, respectively".format(s,v))
