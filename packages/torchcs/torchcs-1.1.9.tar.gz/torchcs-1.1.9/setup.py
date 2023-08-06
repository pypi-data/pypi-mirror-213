#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2030, Zhi Liu.  All rights reserved.

from os import path as os_path
from setuptools import setup
from setuptools import find_packages
from Cython.Build import cythonize
from Cython.Distutils import Extension

__version__ = '1.1.9'

opensource = False

this_dir = os_path.abspath(os_path.dirname(__file__))

def read_file(filename):
    with open(os_path.join(filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

long_description = read_file('README.md'),
long_description_content_type = "text/markdown",


if opensource:
    extensions = [
                Extension("torchcs.signal.pulses", ['torchcs/signal/pulses.py']), 
                Extension("torchcs.sharing.normalization", ['torchcs/sharing/normalization.py']), 
                Extension("torchcs.sharing.nonlinearfn", ['torchcs/sharing/nonlinearfn.py']), 
                Extension("torchcs.dictionary.dcts", ['torchcs/dictionary/dcts.py']), 
                Extension("torchcs.dictionary.dfts", ['torchcs/dictionary/dfts.py']), 
                Extension("torchcs.sensing.bernoullis", ['torchcs/sensing/bernoullis.py']), 
                Extension("torchcs.sensing.gaussians", ['torchcs/sensing/gaussians.py']), 
                Extension("torchcs.sensing.binary", ['torchcs/sensing/binary.py']), 
                Extension("torchcs.recovery.ista_fista", ['torchcs/recovery/ista_fista.py']), 
                Extension("torchcs.recovery.matching_pursuit", ['torchcs/recovery/matching_pursuit.py']), 
                Extension("torchcs.recovery.dlmlcs", ['torchcs/recovery/dlmlcs.py']), 
    ]

    setup(name='torchcs',
      version=__version__,
      description="Compressed Sensing in PyTorch.",
      author='Zhi Liu',
      author_email='zhiliu.mind@gmail.com',
      url='https://iridescent.ink/torchcs/',
      download_url='https://github.com/antsfamily/torchcs/',
      license='MIT',
      packages=find_packages(),
      install_requires=read_requirements('requirements.txt'),
      include_package_data=True,
      keywords=['PyTorch', 'Machine Learning', 'Signal Processing', 'Compressed Sensing'],
      ext_modules=cythonize(extensions)
    )
    
else:
    extensions = [
                Extension("torchcs.signal.pulses", ['torchcs/signal/pulses.c']), 
                Extension("torchcs.sharing.normalization", ['torchcs/sharing/normalization.c']), 
                Extension("torchcs.sharing.nonlinearfn", ['torchcs/sharing/nonlinearfn.c']), 
                Extension("torchcs.dictionary.dcts", ['torchcs/dictionary/dcts.c']), 
                Extension("torchcs.dictionary.dfts", ['torchcs/dictionary/dfts.c']), 
                Extension("torchcs.sensing.bernoullis", ['torchcs/sensing/bernoullis.c']), 
                Extension("torchcs.sensing.gaussians", ['torchcs/sensing/gaussians.c']), 
                Extension("torchcs.sensing.binary", ['torchcs/sensing/binary.c']), 
                Extension("torchcs.recovery.ista_fista", ['torchcs/recovery/ista_fista.c']), 
                Extension("torchcs.recovery.matching_pursuit", ['torchcs/recovery/matching_pursuit.c']), 
                Extension("torchcs.recovery.dlmlcs", ['torchcs/recovery/dlmlcs.c']), 
    ]

    setup(name='torchcs',
        version=__version__,
        description="Compressed Sensing in PyTorch.",
        author='Zhi Liu',
        author_email='zhiliu.mind@gmail.com',
        url='https://ai.iridescent.ink/torchcs/',
        download_url='https://github.com/metai/torchcs/',
        license='MIT',
        packages=find_packages(),
        install_requires=read_requirements('requirements.txt'),
        include_package_data=False,
        keywords=['PyTorch', 'Machine Learning', 'Signal Processing', 'Compressed Sensing'],
        ext_modules=cythonize(extensions)
    )


