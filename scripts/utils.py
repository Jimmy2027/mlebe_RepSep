# -*- coding: utf-8 -*-
from pathlib import Path


def get_template_path() -> Path:
    paths = [Path('/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'),
             Path('/usr/local/share/mouse-brain-atlases/dsurqec_200micron_mask.nii')]
    for path in paths:
        if path.exists():
            return path

    raise RuntimeError(f'Template path not found under paths.')
