import pandas as pd
from utils.bootstrapping import bootstrap

df = pd.read_csv('../data/smoothness.csv')
bootstrap(df, 'Smoothness Conservation Factor')
df = pd.read_csv('../data/volume.csv')
bootstrap(df, 'Volume Conservation Factor')
