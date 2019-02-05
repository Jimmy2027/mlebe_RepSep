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
df_cc.rename(columns={'CC':'similarity'}, inplace=True)
df_gc = df.drop('CC', axis=1).drop('MI',axis=1)
df_gc['Similarity Metric'] = 'GC'
df_gc.rename(columns={'GC':'similarity'}, inplace=True)
df_mi = df.drop('GC', axis=1).drop('CC',axis=1)
df_mi['Similarity Metric'] = 'MI'
df_mi.rename(columns={'MI':'similarity'}, inplace=True)

df = pd.concat([df_cc, df_gc, df_mi], sort=False)

df = df.loc[df['acquisition'].str.contains('bold')]
df['workflow subject'] = df['Processing'].astype(str) + ' ' + df['subject'].astype(str)
df = df[df['Processing']!='Unprocessed']

ax = sns.catplot(
	   #x='session',
	   x='workflow subject',
	   y='similarity',
	   data=df,
	   row = 'Similarity Metric',
	   hue="Processing",
	   #hue="session",
	   size=mpl.rcParams['lines.markersize'],
	   palette=palette,
	   margin_titles=True,
	   aspect=4,
	   )
ax.set(xticklabels=[])
