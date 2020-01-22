import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from os import path
from itertools import product
from lib.categorical import violinplot

# Style
palette = ['#ffb66d','#009093']

data_path = path.abspath('data/functional_t.csv')
df = pd.read_csv(data_path)

df = df.loc[df['Processing']!='Unprocessed']
df = df.loc[((df['Processing']=='Legacy') & (df['Template']=='Legacy')) | ((df['Processing']=='Generic') & (df['Template']=='Generic'))]

df.loc[df['Processing']=='Unprocessed', 'Template'] = ''
ax = violinplot(
x = "Processing",
y = 'Mean DR t',
data = df,
hue = "Contrast",
saturation = 1,
split = True,
inner = 'quartile',
palette = palette,
scale = 'area',
dodge = False,
inner_linewidth = 1.0,
linewidth = mpl.rcParams['grid.linewidth'],
linecolor = 'w',
)
