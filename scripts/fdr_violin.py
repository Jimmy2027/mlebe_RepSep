import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
from itertools import product
from lib.categorical import violinplot

# Style
palette = ['#80e050','#755575']

data_path = path.abspath('data/functional_significance.csv')
df = pd.read_csv(data_path)

#df = df.loc[~df['Subject'].isin(['4003','4009','4002','4004','4006'])]
#df = df.loc[df['Session']=='ofMcF1']
df.loc[df['Processing']=='Unprocessed', 'Template'] = ''
df['Score'] = ''
df['Score'] = df['Mean DR Significance'] - df['Mean Significance']
#df['Score'] = df['Median DR Significance'] / df['Median Significance']
ax = violinplot(
	x="Processing",
	#y='Median DR Significance',
	#y='Median Significance',
	y='Mean Significance',
	#y='Mean DR Significance',
	#y='Score',
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
	bw=0.3,
	)
