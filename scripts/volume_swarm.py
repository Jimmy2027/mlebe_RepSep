import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import path

volume_path = path.abspath('../data/volumes.csv')
df = pd.read_csv(volume_path)
print(df.columns)
a = sns.catplot(
	x="Processing",
	y="thresholded volume",
	hue="Template",
	data=df,
	split=True,
	)
#df_ = df.loc[df['Processing'] == 'Unprocessed']
#df__ = df_.sort_values(by='thresholded volume', ascending=False)
#plt.savefig('foo.pdf')
plt.show()
