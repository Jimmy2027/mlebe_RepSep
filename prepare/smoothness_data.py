from itertools import product
from os import path
from samri.report.snr import df_threshold_volume ,iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator
import nipype.interfaces.io as nio

def bids_autofind(bids_dir,
        modality='',
        path_template="{bids_dir}/sub-{{subject}}/ses-{{session}}/{modality}/sub-{{subject}}_ses-{{session}}_task-{{task}}_acq-{{acquisition}}.nii.gz",
        match_regex='',
        ):
        """Automatically generate a BIDS path template and a substitution iterator (list of dicts, as produced by `samri.utilities.bids_substitution_iterator`, and used as a standard input SAMRI function input) from a BIDS-respecting directory.

        Parameters
        ----------
        bids_dir : str
                Path to BIDS-formatted directory
        modality : {"func", "anat"}
                Which modality to source data for (currently only supports "func", and "anat" - ideally we could extend this to include "dwi").

        Returns
        -------
        path_template : str
                String which can be formatted with any of the dictionaries in `substitutions`
        substitutions : list of dicti
                A substitution iterator usable as a standard SAMRI function input, which (together with `path_template`) unambiguoulsy identifies input files for analysis.
        """

        bids_dir = path.abspath(path.expanduser(bids_dir))

        if match_regex:
                pass
        elif modality in ("func","dwi"):
               match_regex = '.+/sub-(?P<sub>.+)/ses-(?P<ses>.+)/'+modality+'/.*?_task-(?P<task>.+).*?_acq-(?P<acquisition>.+)\.nii.gz'
        elif modality == "":
               match_regex = '.+/sub-(?P<sub>.+)/ses-(?P<ses>.+)/.*?_task-(?P<task>.+).*?_acq-(?P<acquisition>.+).*?\.nii.gz'
        elif modality == "anat":
               match_regex = '.+/sub-(?P<sub>.+)/ses-(?P<ses>.+)/anat/.*?_(?P<task>.+).*?_acq-(?P<acquisition>.+)\.nii.gz'

        path_template = path_template.format(bids_dir=bids_dir, modality=modality)

        datafind = nio.DataFinder()
        datafind.inputs.root_paths = bids_dir
        datafind.inputs.match_regex = match_regex
        datafind_res = datafind.run()

        substitutions = []
        for ix, i in enumerate(datafind_res.outputs.out_paths):
                substitution = {}
                substitution["acquisition"] = datafind_res.outputs.acquisition[ix]
                substitution["subject"] = datafind_res.outputs.sub[ix]
                substitution["session"] = datafind_res.outputs.ses[ix]
                substitution["task"] = datafind_res.outputs.task[ix]
                if path_template.format(**substitution) != i:
                        print("Original DataFinder path: "+i)
                        print("Reconstructed path:       "+path_template.format(**substitution))
                        raise ValueError("The reconstructed file path based on the substitution dictionary and the path template, is not identical to the corresponding path, found by `nipype.interfaces.io.DataFinder`. See string values above.")
                substitutions.append(substitution)

        return path_template, substitutions


def reg_cc(
        path = "~/ni_data/ofM.dr/preprocessing/composite",
        template = "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
        radius=8,
        autofind=False,
        plot=False,
        save = "f_reg_quality",
        metrics = ['CC','GC','MI'],
        ):
        from samri.plotting.aggregate import registration_qc
        from samri.report.registration import iter_measure_sim
        from samri.typesetting import inline_anova
        from samri.utilities import bids_substitution_iterator

        if autofind:
                path_template, substitutions = bids_autofind(path,"func")
        else:
                path_template = "{data_dir}/preprocessing/{preprocessing_dir}/sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_acq-{acquisition}_task-{task}_cbv.nii.gz"
                substitutions = bids_substitution_iterator(
                        ["ofM", "ofMaF", "ofMcF1", "ofMcF2", "ofMpF"],
                        ["4001","4007","4008","4011","5692","5694","5699","5700","5704","6255","6262"],
                        ["CogB","JogB"],
                        "~/ni_data/ofM.dr/",
                        "composite",
                        acquisitions=['EPI','EPIlowcov'],
                        validate_for_template=path_template,
                        )
        df = iter_measure_sim(path_template, substitutions,
                template,
                metric=metrics[0],
                radius_or_number_of_bins=radius,
                sampling_strategy="Regular",
                sampling_percentage=0.95,
                #save_as= save + "_" + metric +  ".csv",
                save_as = False,
                )

        df = df.rename(columns={'similarity': metrics[0],})

        for metric in metrics[1:]:
                _df = iter_measure_sim(path_template, substitutions,
                        template,
                        metric=metric,
                        radius_or_number_of_bins=radius,
                        sampling_strategy="Regular",
                        sampling_percentage=0.95,
                        save_as=False,
                        )
                df[metric] = _df['similarity'].values

        return df

def avg_smoothness(inp_file):
        from nipype.interfaces import afni
        import numpy as np
        fwhm = afni.FWHMx()
        fwhm.inputs.in_file = inp_file
        fwhm.inputs.acf = True
        res = fwhm.run().outputs.fwhm
        mean_smoothness = np.asarray(res).mean()
        return mean_smoothness

def acqname(inp_entry):
        if('bold' in  inp_entry):
                return 'bold'
        else:
                return 'cbv'



scratch_dir = '~/data_scratch/irsabi'

template = '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii'
df_generic = reg_cc(path = scratch_dir + '/preprocessing/generic_collapsed/', save = '../data/' + "variance_data_generic", template=template, autofind=True)
df_generic['Processing'] = 'Generic'
df_generic['Template'] = 'Generic'

template = '/usr/share/mouse-brain-atlases/ambmc_200micron.nii'
df_generic_legacy = reg_cc(path = scratch_dir + '/preprocessing/generic_collapsed/', save = '../data/' + "variance_data_generic", template=template, autofind=True)
df_generic_legacy['Processing'] = 'Generic'
df_generic_legacy['Template'] = 'Legacy'

template = '/usr/share/mouse-brain-atlases/lambmc_200micron.nii'
df_legacy = reg_cc(path = scratch_dir + '/preprocessing/legacy_collapsed/', save = '../data/' + "variance_data_legacy", template=template, autofind=True)
df_legacy['Processing'] = 'Legacy'
df_legacy['Template'] = 'Legacy'

template = '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii'
df_legacy_generic = reg_cc(path = scratch_dir + '/preprocessing/legacy_collapsed/', save = '../data/' + "variance_data_legacy", template=template, autofind=True)
df_legacy_generic['Processing'] = 'Legacy'
df_legacy_generic['Template'] = 'Generic'

template = '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii'
df_bids = reg_cc(path = scratch_dir + '/bids_collapsed/', save = '../data/' + "variance_data_bids", template=template, autofind=True)
df_bids['Processing'] = 'Unprocessed'
df_bids['Template'] = 'Unprocessed'

df = pd.concat([df_generic, df_legacy, df_generic_legacy, df_legacy_generic, df_bids])

df['smoothness'] = df['path'].apply(avg_smoothness)
df['acq'] = df['acquisition'].apply(acqname)

bids_smoothness = df[df['Processing'] == 'Unprocessed']
mean_smoothness = bids_smoothness['smoothness'].mean()
df['Smoothness Change Factor'] = df['smoothness'] / mean_smoothness

df.to_csv('./data/smoothness_data.csv')
