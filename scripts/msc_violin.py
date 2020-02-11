import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
from itertools import product
from lib.categorical import violinplot

data_path = path.abspath('data/functional_significance.csv')
df = pd.read_csv(data_path)
#df = df.loc[~df['Subject'].isin([4003,4006,4013])]
df = df.loc[df['Processing']!='Unprocessed']
df = df.loc[((df['Processing']=='Generic Masked')) | ((df['Processing']=='Generic') )]
df.loc[df['Processing']=='Unprocessed'] = ''
ax = violinplot(
	x="Contrast",
	y='Mean Significance',
	data=df,
	hue="Processing",
	saturation=1,
	split=True,
	inner='quartile',
	palette='muted',
	scale='area',
	dodge=False,
	inner_linewidth=1.0,
	linewidth=mpl.rcParams['grid.linewidth'],
	linecolor='w',
	#bw=0.2,
	)
