import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from os import path

volume_path = path.abspath('data/volumes.csv')
df = pd.read_csv(volume_path)
df.loc[df['Processing']=='Unprocessed', 'Template'] = ''
ax = sns.swarmplot(
	x="Processing",
	y='Thresholded Volume',
	data=df,
	hue="Template",
	size=mpl.rcParams['lines.markersize'],
	#data=df.loc[df['Processing']=='Unprocessed'],
	)
