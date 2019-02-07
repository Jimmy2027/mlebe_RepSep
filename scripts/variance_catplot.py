import pandas as pd
from os import path
import seaborn as sns
import matplotlib as mpl

workflows = ['Generic', 'Legacy']
palette = ['#80e050','#755575']

df_path='data/variance_data.csv'
df = pd.read_csv(path.abspath(df_path))

df_cc = df.drop('GC', axis=1).drop('MI',axis=1)
df_cc['Similarity Metric'] = 'CC'
df_cc.rename(columns={'CC':'Similarity'}, inplace=True)
df_gc = df.drop('CC', axis=1).drop('MI',axis=1)
df_gc['Similarity Metric'] = 'GC'
df_gc.rename(columns={'GC':'Similarity'}, inplace=True)
df_mi = df.drop('GC', axis=1).drop('CC',axis=1)
df_mi['Similarity Metric'] = 'MI'
df_mi.rename(columns={'MI':'Similarity'}, inplace=True)

df = pd.concat([df_cc, df_gc, df_mi], sort=False)

df = df.loc[df['acquisition'].str.contains('bold')]
df = df[df['Processing']!='Unprocessed']
n_cols = len(df['Similarity Metric'].unique())

ax = sns.catplot(
	x='Subject',
	y='Similarity',
	hue='Processing',
	data=df,
	col='Similarity Metric',
	palette=palette,
	legend=True,
	legend_out=False,
	height=mpl.rcParams['figure.figsize'][1],
	aspect=(mpl.rcParams['figure.figsize'][0]/n_cols)/mpl.rcParams['figure.figsize'][1],
	s=2,
	)
ax.set(xticklabels=[])
