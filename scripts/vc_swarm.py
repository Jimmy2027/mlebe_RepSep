import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from os import path

# Style
palette = ['#80e050','#755575']

volume_path = path.abspath('data/volumes.csv')
df = pd.read_csv(volume_path)

df.loc[df['Processing']=='Unprocessed', 'Template'] = ''
ax = sns.swarmplot(
	x='Processing',
	y='Volume Change Factor',
	data=df.loc[df['Processing']!='Unprocessed'],
	hue="Template",
	size=mpl.rcParams['lines.markersize'],
	palette=palette,
	)
