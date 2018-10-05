import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import path

volume_path = path.abspath('../data/volumes.csv')
df = pd.read_csv(volume_path)
print(df)
a = sns.violinplot(
	x="Processing",
	y="thresholded volume",
	hue="Template",
	data=df,
	)
plt.show()
