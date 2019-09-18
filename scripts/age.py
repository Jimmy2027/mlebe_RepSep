import pandas as pd
from os import path

data_path = path.abspath('data/participants.tsv')
df = pd.read_csv(data_path, sep='\t')

min_age = df['age [d]'].min()
max_age = df['age [d]'].max()

print('\SIrange{{{}}}{{{}}}{{days}}'.format(min_age,max_age))
