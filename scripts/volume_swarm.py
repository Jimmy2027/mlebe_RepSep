import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import path

volume_path = path.abspath('../data/volume.csv')
df = pd.read_csv(volume_path)
a = sns.swarmplot(x="Processing",
	y="thresholded volume",
	data=df,
	)
df_ = df.loc[df['Processing'] == 'Unprocessed']
df__ = df_.sort_values(by='thresholded volume', ascending=False)
print(df__)
plt.savefig('foo.pdf')
