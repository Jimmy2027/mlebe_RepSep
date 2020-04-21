import pandas as pd
from numpy.random import choice
from sklearn.metrics import mean_squared_error
from math import sqrt
import os
import statsmodels.formula.api as smf


def bootstrap(df, factor, scratch_dir):
    if factor == 'Volume Conservation Factor':
        metric = 'VCF'
    elif factor == 'Smoothness Conservation Factor':
        metric = 'SCF'
    scratch_dir = os.path.expanduser(scratch_dir)
    if not os.path.isdir(scratch_dir + '/data/bootstrapped'):
        os.mkdir(scratch_dir + '/data/bootstrapped')

    generic_df = df.loc[df['Processing'] == 'Generic']
    generic_CBV_df = generic_df.loc[generic_df['Contrast'] == 'CBV']
    generic_BOLD_df = generic_df.loc[generic_df['Contrast'] == 'BOLD']
    generic_masked_df = df.loc[df['Processing'] == 'Masked']
    generic_masked_CBV_df = generic_masked_df.loc[generic_masked_df['Contrast'] == 'CBV']
    generic_masked_BOLD_df = generic_masked_df.loc[generic_masked_df['Contrast'] == 'BOLD']


    bootstrapped_RMSEs = pd.DataFrame(columns=['Contrast', 'Processing', 'Uid', metric + '_RMSE'])

    N = 10000

    for i in range(N):
        generic_CBV_df_temp = choice(generic_CBV_df[factor].to_list(),
                                     len(generic_CBV_df[factor].to_list()))
        generic_BOLD_df_temp = choice(generic_BOLD_df[factor].to_list(),
                                      len(generic_BOLD_df[factor].to_list()))
        generic_masked_CBV_df_temp = choice(generic_masked_CBV_df[factor].to_list(),
                                            len(generic_masked_CBV_df[factor].to_list()))
        generic_masked_BOLD_df_temp = choice(generic_masked_BOLD_df[factor].to_list(),
                                             len(generic_masked_BOLD_df[factor].to_list()))
        rmse_generic_masked_CBV = sqrt(
            mean_squared_error([1] * len(generic_masked_CBV_df_temp), generic_masked_CBV_df_temp))
        rmse_generic_masked_BOLD = sqrt(
            mean_squared_error([1] * len(generic_masked_BOLD_df_temp), generic_masked_BOLD_df_temp))
        rmse_generic_CBV = sqrt(mean_squared_error([1] * len(generic_CBV_df_temp), generic_CBV_df_temp))
        rmse_generic_BOLD = sqrt(mean_squared_error([1] * len(generic_BOLD_df_temp), generic_BOLD_df_temp))
        bootstrapped_RMSEs = bootstrapped_RMSEs.append(
            pd.DataFrame([['CBV', 'Generic', '{}.1'.format(i), rmse_generic_CBV]],
                         columns=['Contrast', 'Processing', 'Uid', metric + '_RMSE']), sort = False)
        bootstrapped_RMSEs = bootstrapped_RMSEs.append(
            pd.DataFrame([['BOLD', 'Generic', '{}.2'.format(i), rmse_generic_BOLD]],
                         columns=['Contrast', 'Processing', 'Uid', metric + '_RMSE']), sort = False)
        bootstrapped_RMSEs = bootstrapped_RMSEs.append(
            pd.DataFrame([['CBV', 'Masked', '{}.1'.format(i), rmse_generic_masked_CBV]],
                         columns=['Contrast', 'Processing', 'Uid', metric + '_RMSE']), sort = False)
        bootstrapped_RMSEs = bootstrapped_RMSEs.append(pd.DataFrame([['BOLD', 'Masked', '{}.2'.format(i), rmse_generic_masked_BOLD]],
                                                                    columns=['Contrast', 'Processing', 'Uid', metric + '_RMSE']), sort = False)
    if factor == 'Volume Conservation Factor':
        bootstrapped_RMSEs.to_csv(scratch_dir + '/data/bootstrapped/bootstrapped_volume.csv', index= False)
    elif factor == 'Smoothness Conservation Factor':
        bootstrapped_RMSEs.to_csv(scratch_dir + '/data/bootstrapped/bootstrapped_smoothness.csv', index = False)

def bootstrap_analysis(
    factor,
    dependent_variable = 'RMSE',
    expression = 'Processing*Contrast',
    scratch_dir = '',
    ):
    scratch_dir = os.path.expanduser(scratch_dir)
    if factor == 'volume':
        df_path = scratch_dir + '/data/bootstrapped/bootstrapped_volume.csv'
        df_name = 'vbootstrapped_analy'
    if factor == 'smoothness':
        df_path = scratch_dir + '/data/bootstrapped/bootstrapped_smoothness.csv'
        df_name = 'sbootstrapped_analy'

    df = pd.read_csv(df_path)

    df = df.loc[df['Processing'] != 'Unprocessed']
    df = df.loc[((df['Processing'] == 'Masked')) | ((df['Processing'] == 'Generic'))]

    formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
    model = smf.mixedlm(formula, df, groups='Uid')
    fit = model.fit()
    summary = fit.summary().tables[1]
    summary.to_csv(scratch_dir + '/data/bootstrapped/{}.csv'.format(df_name))
    # temp = pd.read_csv(scratch_dir + '/data/bootstrapped/{}.csv'.format(df_name), index_col=0)
