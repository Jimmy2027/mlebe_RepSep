import pandas as pd
from os import path

data_path = path.abspath('data/participants.tsv')
df = pd.read_csv(data_path, sep='\t')

m = len(df.loc[(df['sex']=='m')])
f = len(df.loc[(df['sex']=='f')])
print('\SI{{{}}}{{males}} and {} females'.format(m,f))
