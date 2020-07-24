from os import path
import matplotlib as mpl
import pandas as pd
from lib.categorical import violinplot

df_path = 'data/smoothness.csv'
df = pd.read_csv(path.abspath(df_path))

df = df.loc[((df['Processing'] == 'Masked')) | ((df['Processing'] == 'Generic'))]

ax = violinplot(
    x='Contrast',
    y='Abs(1 - Scf)',
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
