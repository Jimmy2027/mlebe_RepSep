import pandas as pd
from os import path
import numpy as np
from lib.categorical import violinplot
import matplotlib as mpl

df_path='data/smoothness.csv'
df = pd.read_csv(path.abspath(df_path))

df = df.loc[((df['Processing']=='Generic Masked')) | ((df['Processing']=='Generic'))]

#df.loc[df['Processing']=='Legacy','Smoothness Conservation Factor'] = df.loc[df['Processing']=='Legacy','Smoothness Conservation Factor']/10
#df[r'$\mathsf{log_{10}(Smoothness\,Change\,Factor)}$'] = np.log10(df['Smoothness Conservation Factor'])
ax = violinplot(
        x='Contrast',
        #y=r'$\mathsf{log_{10}(Smoothness\,Change\,Factor)}$',
        y='Smoothness Conservation Factor',
        #y='Smoothness Conservation Factor',
        #y='Smoothness',
        data=df,
        hue="Processing",
        saturation=1,
        split=True,
        inner='quartile',
        palette='muted',
        scale='area',
        dodge=False,
        inner_linewidth=1.0,
        linewidth=mpl.rcParams['grid.linewidth'],
        linecolor='w',
        )
ax.legend()