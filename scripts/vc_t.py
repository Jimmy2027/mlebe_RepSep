import pandas as pd
from os import path
from scipy.stats import ttest_rel
from lib.utils import float_to_tex


volume_path = path.abspath('data/volume.csv')
df = pd.read_csv(volume_path)
summary =  ttest_rel(
	df.loc[(df['Processing']=='Generic Masked'), 'Volume Conservation Factor'].tolist(),
	df.loc[(df['Processing']=='Generic'), 'Volume Conservation Factor'].tolist(),
	)
print(df.loc[(df['Processing']=='Generic Masked'), df['Volume Conservation Factor'] - 1 > 0.1].tolist())
print(float_to_tex(summary.pvalue, max_len=3, condensed=True, padding=True))
