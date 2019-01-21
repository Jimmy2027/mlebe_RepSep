import pandas as pd
from os import path
from scipy.stats import ttest_rel
from lib.utils import float_to_tex

smoothness_path = path.abspath('data/smoothness_data.csv')
df = pd.read_csv(smoothness_path)

summary =  ttest_rel(
	df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Smoothness Change Factor'].tolist(),
	df.loc[(df['Processing']=='Generic') & (df['Template']=='Generic'), 'Smoothness Change Factor'].tolist(),
	)
print(float_to_tex(summary.pvalue, max_len=3, condensed=True, padding=True))
