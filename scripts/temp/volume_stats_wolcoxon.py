import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
from os import path
from scipy.stats import levene, iqr, wilcoxon
import numpy as np

def wilcoxon_(
    df_path='data/volume.csv',
    contrast = '',
    dependent_variable='Volume Conservation Factor',
    ):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)
    df = df.loc[df['Processing']!= 'Unprocessed']
    df = df.loc[df['Contrast'] == contrast]
    generic_masked_df = df.loc[df['Processing'] == 'Generic Masked']
    generic_df = df.loc[df['Processing'] == 'Generic']
    generic_masked_df = generic_masked_df.sort_values(by = ['Path'])
    generic_df = generic_df.sort_values(by=['Path'])
    generic_masked = generic_masked_df[dependent_variable].tolist()
    generic = generic_df[dependent_variable].tolist()
    statistic, p = wilcoxon(generic_masked, generic)
    return np.round(statistic, 3), np.round(p, 3)


print(wilcoxon_(contrast = 'BOLD'))
print(wilcoxon_(contrast = 'CBV'))