import pandas as pd
from os import path
from scipy.stats import ttest_rel
from lib.utils import float_to_tex

volume_path = path.abspath('data/functional_t.csv')
df = pd.read_csv(volume_path)

summary =  ttest_rel(
	df.loc[(df['Processing']=='Legacy') & (df['Template']=='Legacy'), 'Mean DR t'].tolist(),
	df.loc[(df['Processing']=='Generic') & (df['Template']=='Generic'), 'Mean DR t'].tolist(),
	)
print(float_to_tex(summary.pvalue, max_len=3, condensed=True, padding=True))
