import pandas as pd
from os import path
import numpy as np
from lib.categorical import violinplot
import matplotlib as mpl

palette = ['#80e050','#755575']
df_path='data/smoothness_data.csv'
df = pd.read_csv(path.abspath(df_path))

df = df.loc[((df['Processing']=='Legacy') & (df['Template']=='Legacy')) | ((df['Processing']=='Generic') & (df['Template']=='Generic'))]

ax = violinplot(
        x="Processing",
        y='Smoothness Change Factor',
        data=df,
        hue="acq",
        saturation=1,
        split=True,
        inner='quartile',
        palette=palette,
        scale='area',
        dodge=False,
        inner_linewidth=1.0,
        linewidth=mpl.rcParams['grid.linewidth'],
        linecolor='w',
        )
