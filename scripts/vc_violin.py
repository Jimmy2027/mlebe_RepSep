import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
from itertools import product
from lib.categorical import violinplot

# Style
palette = ['#80e050','#755575']

volume_path = path.abspath('data/volumes.csv')
df = pd.read_csv(volume_path)

df['Volume Change Factor']=-1
uids = df['uID'].unique()
templates = [i for i in df['Template'].unique() if i != 'Unprocessed']
processings = [i for i in df['Processing'].unique() if i != 'Unprocessed']

for uid, template, processing in list(product(uids,templates,processings)):
	reference = df.loc[(df['uID']==uid) & (df['Processing']=='Unprocessed'), 'Thresholded Volume'].item()
	volume = df.loc[(df['uID']==uid) & (df['Processing']==processing) & (df['Template']==template), 'Thresholded Volume'].item()
	df.loc[(df['uID']==uid) & (df['Processing']==processing) & (df['Template']==template), 'Volume Change Factor'] = volume/reference

df.loc[df['Processing']=='Unprocessed', 'Template'] = ''
ax = violinplot(
	x="Processing",
	y='Volume Change Factor',
	data=df.loc[df['Processing']!='Unprocessed'],
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
