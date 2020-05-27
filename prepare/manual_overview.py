import itertools
import matplotlib.pyplot as plt
import os
from samri.plotting.maps import contour_slices
from samri.utilities import bids_substitution_iterator
from joblib import Parallel, delayed
import multiprocessing as mp
import matplotlib as mpl
from subjects_reader import find_subjects, find_sessions, find_tasks

num_cores = max(mp.cpu_count() - 1, 1)
mpl.rcParams['font.size'] = 14

templates = {
    'generic': '/usr/share/mouse-brain-atlases/dsurqec_40micron_masked.nii',
    'masked': '/usr/share/mouse-brain-atlases/dsurqec_40micron_masked.nii',
}

# todo: do these functions still work?
# subjects = find_subjects()
# sessions=find_sessions(os.path.expanduser('~/.scratch/mlebe/bids_collapsed'))
# if '6mo' in sessions:
# 	blacklisted_run = True		#boolean to indicate that this script is executed for the blacklisted volumes
# else: blacklisted_run = False
# tasks = find_tasks(os.path.expanduser('~/.scratch/mlebe/bids_collapsed'))
# if blacklisted_run:
# 	functional_acquisitions = ['EPI']
# 	structural_acquisitions = ['TurboRARE']
# else:
# 	functional_acquisitions = ['EPIlowcov', 'geEPI']
# 	structural_acquisitions = ['TurboRARElowcov', 'TurboRARE']

subjects = [
    '4001',
    '4002',
    '4004',
    '4005',
    '4006',
    '4007',
    '4008',
    '4009',
    '4011',
    '4012',
    '4013',
    'VZ02',
    'VZ01',
    'VZ03',
    'VZ04',
    'VZ05',
    'VZ06',
    'VZ07',
    'VZ08',
    'VZ09',
    'VZ10',
]

sessions = [
    'ofM',
    'ofMaF',
    'ofMcF1',
    'ofMcF2',
    'ofMpF',
    'baseline',
    'FUP1',
    'FUP2',
]

runs = {
    0: 'bold',
    1: 'cbv'
}

data_dir = '~/.scratch/mlebe'
cmap = plt.get_cmap('tab20').colors


def func_contour_slices(substitution, file_path, data_dir, key, i, spacing):
    contour_slices(file_path.format(**substitution),
                   alpha=[0.9],
                   colors=cmap[::2],
                   figure_title='Single-Session Fit and Distortion Control\n Subject {} | Session {} | Contrast {}'.format(
                       i[0], substitution['session'], runs[i[1]].upper()),
                   file_template=templates[key],
                   force_reverse_slice_order=True,
                   legend_template='Template',
                   levels_percentile=[79],
                   ratio=[5, 5],
                   slice_spacing=spacing,
                   save_as='{}/manual_overview/{}/{}_{}_{}.pdf'.format(data_dir, key, i[0], substitution['session'],
                                                                       runs[i[1]]),
                   )


def anat_contour_slices(substitution, file_path, data_dir, key, i, spacing, contrast):
    contour_slices(file_path.format(**substitution),
                   alpha=[0.9],
                   colors=cmap[::2],
                   figure_title='Single-Session Fit and Distortion Control\n Subject {} | Session {} | Contrast T2'.format(
                       i[0], substitution['session']),
                   file_template=templates[key],
                   force_reverse_slice_order=True,
                   legend_template='Template',
                   levels_percentile=[79],
                   ratio=[5, 5],
                   slice_spacing=spacing,
                   save_as='{}/manual_overview/{}/{}_{}_T2w.pdf'.format(data_dir, key, i[0], substitution['session']),
                   )


for key in templates:
    spacing = 0.65
    for i in list(itertools.product(subjects, runs)):
        if 'VZ' in i[0]:
            if i[1] != 0:
                continue
            anat_contrast = 'T1w'
            func_path = '{{data_dir}}/preprocessing/{}_collapsed/sub-{{subject}}/ses-{{session}}/func/sub-{{subject}}_ses-{{session}}_task-rest_acq-EPI_run-{}_{}.nii.gz'.format(
                key, i[1], runs[i[1]])
            anat_path = '{{data_dir}}/preprocessing/{}_collapsed/sub-{{subject}}/ses-{{session}}/anat/sub-{{subject}}_ses-{{session}}_acq-FLASH_T1w.nii.gz'.format(
                key)
        else:
            anat_contrast = 'T2w'
            func_path = '{{data_dir}}/preprocessing/{}_collapsed/sub-{{subject}}/ses-{{session}}/func/sub-{{subject}}_ses-{{session}}_task-JogB_acq-EPIlowcov_run-{}_{}.nii.gz'.format(
                key, i[1], runs[i[1]])
            anat_path = '{{data_dir}}/preprocessing/{}_collapsed/sub-{{subject}}/ses-{{session}}/anat/sub-{{subject}}_ses-{{session}}_acq-TurboRARElowcov_T2w.nii.gz'.format(
                key)

        func_substitutions = bids_substitution_iterator(
            sessions=sessions,
            subjects=[i[0]],
            data_dir=data_dir,
            validate_for_template=func_path,
        )
        anat_substitutions = bids_substitution_iterator(
            sessions=sessions,
            subjects=[i[0]],
            data_dir=data_dir,
            validate_for_template=anat_path,
        )

        Parallel(n_jobs=num_cores, verbose=0)(map(delayed(func_contour_slices),
                                                  func_substitutions,
                                                  [func_path] * len(func_substitutions),
                                                  [data_dir] * len(func_substitutions),
                                                  [key] * len(func_substitutions),
                                                  [i] * len(func_substitutions),
                                                  [spacing] * len(func_substitutions),
                                                  ))
        Parallel(n_jobs=num_cores, verbose=0)(map(delayed(anat_contour_slices),
                                                  anat_substitutions,
                                                  [anat_path] * len(anat_substitutions),
                                                  [data_dir] * len(anat_substitutions),
                                                  [key] * len(anat_substitutions),
                                                  [i] * len(anat_substitutions),
                                                  [spacing] * len(anat_substitutions),
                                                  [anat_contrast] * len(anat_substitutions),
                                                  ))

        contour_slices(templates[key],
                       alpha=[0.6],
                       colors=cmap[::2],
                       figure_title='Multi-Session Coherence Control\n Subject {} | Task {}'.format(i[0], runs[i[1]]),
                       file_template=func_path,
                       force_reverse_slice_order=True,
                       legend_template='{session} session',
                       levels_percentile=[77],
                       save_as='{}/manual_overview/{}/coherence_{}_{}.pdf'.format(data_dir, key, i[0], runs[i[1]]),
                       slice_spacing=spacing,
                       substitutions=func_substitutions,
                       )
