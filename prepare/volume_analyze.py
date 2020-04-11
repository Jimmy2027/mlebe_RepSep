import pandas as pd
from numpy.random import choice
from sklearn.metrics import mean_squared_error
from math import sqrt
import statsmodels.formula.api as smf

volume_df = pd.read_csv('../data/volume.csv')
generic_df = volume_df.loc[volume_df['Processing']=='Generic']
generic_CBV_df = generic_df.loc[generic_df['Contrast']=='CBV']
generic_BOLD_df = generic_df.loc[generic_df['Contrast']=='BOLD']
generic_masked_df = volume_df.loc[volume_df['Processing']=='Generic Masked']
generic_masked_CBV_df = generic_masked_df.loc[generic_masked_df['Contrast']=='CBV']
generic_masked_BOLD_df = generic_masked_df.loc[generic_masked_df['Contrast']=='BOLD']


bootstrapped_RMSEs = pd.DataFrame(columns=['Contrast', 'Processing', 'Uid', 'RMSE'])

N = 10000

for i in range(N):
    generic_CBV_df_temp = choice(generic_CBV_df['Volume Conservation Factor'].to_list(), len(generic_CBV_df['Volume Conservation Factor'].to_list()))
    generic_BOLD_df_temp = choice(generic_BOLD_df['Volume Conservation Factor'].to_list(), len(generic_BOLD_df['Volume Conservation Factor'].to_list()))
    generic_masked_CBV_df_temp = choice(generic_masked_CBV_df['Volume Conservation Factor'].to_list(), len(generic_masked_CBV_df['Volume Conservation Factor'].to_list()))
    generic_masked_BOLD_df_temp = choice(generic_masked_BOLD_df['Volume Conservation Factor'].to_list(), len(generic_masked_BOLD_df['Volume Conservation Factor'].to_list()))
    rmse_generic_masked_CBV = sqrt(mean_squared_error([1] * len(generic_masked_CBV_df_temp), generic_masked_CBV_df_temp))
    rmse_generic_masked_BOLD = sqrt(mean_squared_error([1] * len(generic_masked_BOLD_df_temp), generic_masked_BOLD_df_temp))
    rmse_generic_CBV = sqrt(mean_squared_error([1] * len(generic_CBV_df_temp), generic_CBV_df_temp))
    rmse_generic_BOLD = sqrt(mean_squared_error([1] * len(generic_BOLD_df_temp), generic_BOLD_df_temp))
    bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['CBV', 'Generic', '{}.1'.format(i), rmse_generic_CBV]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))
    bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['BOLD', 'Generic', '{}.2'.format(i), rmse_generic_BOLD]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))
    bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['CBV', 'Generic Masked', '{}.1'.format(i), rmse_generic_masked_CBV]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))
    bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['BOLD', 'Generic Masked', '{}.2'.format(i), rmse_generic_masked_BOLD]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))

bootstrapped_RMSEs.to_csv('../data/bootstrapped_volume.csv')

# dependent_variable = 'RMSE'
# expression = 'Processing*Contrast'
# formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
# model = smf.mixedlm(formula, bootstrapped_RMSEs, groups='Uid')
# fit = model.fit()
# summary = fit.summary()
# print(summary)
