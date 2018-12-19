import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
import seaborn as sns
from itertools import product

# Style
palette = ['#80e050','#755575']

data_path = path.abspath('data/functional_significance.csv')
df = pd.read_csv(data_path)

df = df.loc[df['Session']=='ofM']
df = df.loc[df['Contrast']=='BOLD']

ax = sns.swarmplot(
	x="Processing",
	y='Mean Significance',
	data=df,
	hue="Template",
	#saturation=1,
	split=True,
	palette=palette,
	dodge=False,
	)

ax.set_title('BOLD only')
