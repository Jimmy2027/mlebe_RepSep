import pandas as pd
from os import path
from scipy.stats import ttest_rel
from lib.utils import float_to_tex

volume_path = path.abspath('data/volumes.csv')
df = pd.read_csv(volume_path)

summary =  ttest_rel(
	df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Volume Change Factor'].tolist(),
	df.loc[(df['Processing']=='Generic') & (df['Template']=='Generic'), 'Volume Change Factor'].tolist(),
	)
print(float_to_tex(summary.pvalue, max_len=3, condensed=True, padding=True))
