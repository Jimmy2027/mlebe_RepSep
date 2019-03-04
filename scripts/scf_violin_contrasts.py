import pandas as pd
from os import path
import numpy as np
from lib.categorical import violinplot
import matplotlib as mpl

# Style
palette = ['#ffb66d','#009093']

df_path='data/smoothness.csv'
df = pd.read_csv(path.abspath(df_path))

df = df.loc[((df['Processing']=='Legacy') & (df['Template']=='Legacy')) | ((df['Processing']=='Generic') & (df['Template']=='Generic'))]

df.loc[df['Processing']=='Legacy','Smoothness Change Factor'] = df.loc[df['Processing']=='Legacy','Smoothness Change Factor']/10
#df[r'$\mathsf{log_{10}(Smoothness\,Change\,Factor)}$'] = np.log10(df['Smoothness Change Factor'])
ax = violinplot(
        x="Processing",
        #y=r'$\mathsf{log_{10}(Smoothness\,Change\,Factor)}$',
        y='Smoothness Change Factor',
        data=df,
        hue="Contrast",
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
