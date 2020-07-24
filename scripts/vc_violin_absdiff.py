from os import path
import matplotlib as mpl
import pandas as pd
from lib.categorical import violinplot

volume_path = path.abspath('data/volume.csv')
df = pd.read_csv(volume_path)

df = df.loc[df['Processing'] != 'Unprocessed']
df = df.loc[((df['Processing'] == 'Masked') | (df['Processing'] == 'Generic'))]

df.loc[df['Processing'] == 'Unprocessed'] = ''

ax = violinplot(
    x='Contrast',
    y='Abs(1 - Vcf)',
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
