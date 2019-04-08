import pandas as pd
from os import path
import numpy as np
from lib.categorical import violinplot
import matplotlib.pyplot as plt
import matplotlib as mpl

palette = ['#80e050','#755575']
v_path='data/volume.csv'
v = pd.read_csv(path.abspath(v_path))
df_path='data/smoothness.csv'
df = pd.read_csv(path.abspath(df_path))

df = df[df['Processing']!='Unprocessed']
df = df[df['Template']!='Unprocessed']

#df.loc[df['Processing']=='Legacy','Smoothness Conservation Factor'] = df.loc[df['Processing']=='Legacy','Smoothness Conservation Factor']/10
#df[r'$\mathsf{log_{10}(Smoothness\,Change\,Factor)}$'] = np.log10(df['Smoothness Conservation Factor'])

ax = violinplot(
        x="Processing",
        #y=r'$\mathsf{log_{10}(Smoothness\,Change\,Factor)}$',
        #y='Smoothness Conservation Factor',
        y='Smoothness Conservation Factor',
        #y='Smoothness',
        data=df,
        hue="Template",
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
