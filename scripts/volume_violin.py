import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import path

volume_path = path.abspath('../data/volume.csv')
df = pd.read_csv(volume_path)
a = sns.violinplot(x="Processing",
	y="thresholded volume",
	#hue="thresholded volume",
	split=False,
	inner="quart",
	data=df,
	)
