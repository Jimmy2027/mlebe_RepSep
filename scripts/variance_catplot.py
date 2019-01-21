import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

workflows = ['Generic', 'Legacy']
palette = ['#80e050','#755575']

df_path='data/variance_data_catplot.csv'
df = pd.read_csv(path.abspath(df_path))
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
