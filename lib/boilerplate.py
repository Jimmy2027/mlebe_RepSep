from os import path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from mlebe.training.configs.utils import json_to_dict
from scipy.stats import iqr, wilcoxon

from lib.utils import float_to_tex, inline_anova, inline_factor


def fstatistic(factor,
               df_path='data/volume.csv',
               dependent_variable='Volume Conservation Factor',
               expression='Processing*Contrast',
               exclusion_criteria={},
               **kwargs
               ):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)
    df = df.loc[df['Processing'] != 'Unprocessed']

    for key in exclusion_criteria.keys():
        df = df.loc[~df[key].isin(exclusion_criteria[key])]

    formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
    ols = smf.ols(formula, df).fit()
    anova = sm.stats.anova_lm(ols, typ=3)
    tex = inline_anova(anova, factor, 'tex', **kwargs)
    return tex


def wilcoxon_(
        df_path='data/volume.csv',
        dependent_variable='Volume Conservation Factor',
):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)
    df = df.loc[df['Processing'] != 'Unprocessed']
    generic_masked_df = df.loc[df['Processing'] == 'Masked']
    generic_df = df.loc[df['Processing'] == 'Generic']
    generic_masked_df = generic_masked_df.sort_values(by=['Path'])
    generic_df = generic_df.sort_values(by=['Path'])
    generic_masked = generic_masked_df[dependent_variable].tolist()
    generic = generic_df[dependent_variable].tolist()
    statistic, p = wilcoxon(generic_masked, generic)
    return np.round(statistic, 3), np.round(p, 3)


def factorci(factor,
             df_path='data/volume.csv',
             dependent_variable='Volume Conservation Factor',
             expression='Processing*Contrast',
             exclusion_criteria={},
             **kwargs
             ):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)

    df = df.loc[df['Processing'] != 'Unprocessed']

    for key in exclusion_criteria.keys():
        df = df.loc[~df[key].isin(exclusion_criteria[key])]
    formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
    model = smf.mixedlm(formula, df, groups='Uid')
    fit = model.fit()
    summary = fit.summary()
    tex = inline_factor(summary, factor, 'tex', **kwargs)
    return tex


def corecomparison_factorci(factor,
                            df_path='data/volume.csv',
                            dependent_variable='Volume Conservation Factor',
                            expression='Processing*Contrast',
                            exclusion_criteria={},
                            **kwargs
                            ):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)

    df = df.loc[df['Processing'] != 'Unprocessed']
    df = df.loc[((df['Processing'] == 'Masked')) | ((df['Processing'] == 'Generic'))]

    for key in exclusion_criteria.keys():
        df = df.loc[~df[key].isin(exclusion_criteria[key])]

    formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
    model = smf.mixedlm(formula, df, groups='Uid')
    fit = model.fit()
    summary = fit.summary()
    tex = inline_factor(summary, factor, 'tex', **kwargs)
    return tex


def bootstrapped_corecomparison_factorci(
        factor,
        metric='volume',
        **kwargs
):
    if metric == 'volume':
        summary = pd.read_csv('data/bootstrapped/vbootstrapped_analy.csv', index_col=0)
    if metric == 'smoothness':
        summary = pd.read_csv('data/bootstrapped/sbootstrapped_analy.csv', index_col=0)
    tex = inline_factor(summary, factor, 'tex', **kwargs)
    return tex


def varianceratio(
        df_path='data/volume.csv',
        dependent_variable='Volume Conservation Factor',
        max_len=2,
        **kwargs
):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)

    df = df.loc[df['Processing'] != 'Unprocessed']

    generic_masked = np.var(df.loc[df['Processing'] == 'Masked', dependent_variable].tolist())
    generic = np.var(df.loc[df['Processing'] == 'Generic', dependent_variable].tolist())

    ratio = generic_masked / generic
    return float_to_tex(ratio, max_len, **kwargs)


def variance_test(
        factor,
        workflow,
        metric,
        df_path='data/variance.csv',
        template=False,
        max_len=2,
        **kwargs
):
    df = pd.read_csv(path.abspath(df_path))
    df = df.loc[df['Processing'] == workflow]
    # contrast
    df = df.loc[df['acquisition'].str.contains('cbv')]
    model = metric + '~ C(Subject) + C(Session)'
    ols = smf.ols(model, df).fit()
    anova = sm.stats.anova_lm(ols, typ=3, robust='hc3')
    tex = inline_anova(anova, factor, 'tex', **kwargs)
    return tex


def print_dice():
    reg_results_df = pd.read_csv('prepare/classifier/reg_results.csv')
    config = json_to_dict('data/config.json')
    uid = config['workflow_config']['uid']
    dice_score = reg_results_df.loc[reg_results_df['uid'] == uid, 'anat_model_dice'].item()
    return np.round(float(dice_score), 3)


def get_training_shape(type='tuple', idx=False):
    workflow_config = json_to_dict('data/config.json')
    anat_model_config = json_to_dict(workflow_config['masking_config']['masking_config_anat']['model_config_path'])
    scale_size = anat_model_config['augmentation']['mlebe']['scale_size']
    if idx:
        return scale_size[type]
    elif type == 'tuple':
        return '({}, {})'.format(scale_size[0], scale_size[1])
    elif type == 'triple':
        return '({}, {}, {})'.format(scale_size[0], scale_size[1], scale_size[2])
    else:
        return scale_size[0]


def get_epochs():  # todo is this needed?
    reg_results_df = pd.read_csv('prepare/classifier/reg_results.csv')
    config = json_to_dict('data/config.json')
    uid = config['workflow_config']['uid']
    dice_score = reg_results_df.loc[reg_results_df['uid'] == uid, 'anat_model_dice'].item()


def iqr_(
        df_path='data/volume.csv',
        dependent_variable='Volume Conservation Factor',
        processing='Generic',
):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)
    df = df.loc[df['Processing'] != 'Unprocessed']
    list = df.loc[(df['Processing'] == processing), dependent_variable].tolist()
    print(iqr(list))


def plt_factorci_summary(df_path='data/volume.csv',
                         dependent_variable='Volume Conservation Factor',
                         expression='Processing*Contrast',
                         exclusion_criteria={},
                         caption=None,
                         label='',
                         ):
    df_path = path.abspath(df_path)
    df = pd.read_csv(df_path)

    df = df.loc[df['Processing'] != 'Unprocessed']
    df = df.loc[((df['Processing'] == 'Masked')) | ((df['Processing'] == 'Generic'))]

    for key in exclusion_criteria.keys():
        df = df.loc[~df[key].isin(exclusion_criteria[key])]

    formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
    model = smf.mixedlm(formula, df, groups='Uid')
    fit = model.fit()
    summary = fit.summary()
    if caption:
        summary.title = caption
    return summary.as_latex(label=label).replace('\hline', '')


def get_nmbrScans_from_dataselection(data_set):
    data_selection = pd.read_csv('data/data_selection.csv')
    return data_selection.loc[data_selection['data_set'] == data_set].groupby('subject').count()['uid'].sum()


def get_nmbrSubject_from_dataselection(data_set):
    data_selection = pd.read_csv('data/data_selection.csv')
    return len(data_selection.loc[data_selection['data_set'] == data_set].groupby('subject')['subject'])


def get_max_numbrSession_from_dataselection(data_set):
    data_selection = pd.read_csv('data/data_selection.csv')
    return max(data_selection.loc[data_selection['data_set'] == data_set].groupby('subject').count()['uid'])


if __name__ == '__main__':
    print(get_training_shape())
