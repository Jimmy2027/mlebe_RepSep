import pandas as pd
from os import path
from scipy.stats import ttest_rel
from lib.utils import float_to_tex

smoothness_path = path.abspath('data/smoothness_data.csv')
df = pd.read_csv(smoothness_path)

ones = [1.0] * len(df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Smoothness Change Factor'].tolist())


summary =  ttest_rel(
	df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Smoothness Change Factor'].tolist(),
	ones,
	)
print(float_to_tex(summary.pvalue, max_len=3, condensed=True, padding=True))