#!/usr/bin/env python
#
# test_performance.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import pytest

from fsleyes.tests import run_cli_tests, discretise


cli_tests = """
3d.nii.gz
3d.nii.gz -ot mask -t 4000 10000
3d.nii.gz -ot mip
{{discretise('3d.nii.gz', 500)}} -ot label
dti
dti/dti_V1 -ot rgbvector
dti/dti_V1 -ot linevector
sh -ot sh
mesh_l_thal.vtk -mc 1 0 0
"""


extras = {'discretise' : discretise}


def add_prefix(prefix):
    tests = list(cli_tests.strip().split('\n'))
    tests = [prefix + t for t in tests]
    return '\n'.join(tests)


@pytest.mark.parametrize('performance', [1, 2, 3])
@pytest.mark.parametrize('scene', ['ortho', 'lightbox'])
@pytest.mark.parametrize('neuro', [False, True])
def test_performance(performance, neuro, scene):
    prefix = f'-p {performance} -s {scene} '
    if scene == 'lightbox': prefix += '-zr 0 1 '
    if neuro:               prefix += '-no '
    tests = add_prefix(prefix)
    run_cli_tests('test_performance', tests, extras=extras)
