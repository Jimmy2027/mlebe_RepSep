import pandas as pd
from utils.bootstrapping import bootstrap, bootstrap_analysis

# df = pd.read_csv('../data/smoothness.csv')
# bootstrap(df, 'Smoothness Conservation Factor')
bootstrap_analysis('smoothness',dependent_variable = 'RMSE',expression = 'Processing*Contrast')
# df = pd.read_csv('../data/volume.csv')
# bootstrap(df, 'Volume Conservation Factor')
bootstrap_analysis('volume',dependent_variable = 'RMSE',expression = 'Processing*Contrast')

