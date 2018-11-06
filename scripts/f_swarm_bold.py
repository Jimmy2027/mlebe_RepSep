import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
import seaborn as sns
from itertools import product

# Style
palette = ['#80e050','#755575']

data_path = path.abspath('data/functional.csv')
df = pd.read_csv(data_path)

df = df.loc[df['Session']=='ofM']

ax = sns.swarmplot(
	x="Processing",
	y='Mean Significance',
	data=df.loc[df['Contrast']=='BOLD'],
	hue="Template",
	#saturation=1,
	split=True,
	palette=palette,
	dodge=False,
	)

ax.set_title('BOLD only')
