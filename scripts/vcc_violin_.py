import pandas as pd
import seaborn as sns
import matplotlib as mpl
from lib.categorical import violinplot
from os import path

volume_path = path.abspath('data/volume.csv')
df = pd.read_csv(volume_path)

df = df.loc[df['Processing']!='Unprocessed']
df = df.loc[((df['Processing']=='Masked') | (df['Processing']=='Generic'))]

df.loc[df['Processing']=='Unprocessed'] = ''

ax = violinplot(
	x='Contrast',
	y='1 - Vcf',
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
	)