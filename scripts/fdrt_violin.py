import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
from itertools import product
from lib.categorical import violinplot

# Style
palette = ['#80e050','#755575']

data_path = path.abspath('data/functional_t.csv')
df = pd.read_csv(data_path)

df.loc[df['Processing']=='Unprocessed', 'Template'] = ''
df = df.loc[df['Contrast']=='CBV']
ax = violinplot(
	x="Processing",
	y='Mean DR t',
	data=df,
	hue="Template",
	saturation=1,
	split=True,
	inner='quartile',
	palette=palette,
	scale='area',
	dodge=False,
	inner_linewidth=1.0,
	linewidth=mpl.rcParams['grid.linewidth'],
	linecolor='w',
	)
