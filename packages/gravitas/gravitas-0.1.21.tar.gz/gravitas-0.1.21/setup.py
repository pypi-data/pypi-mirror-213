from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

import os
import numpy as np

_SOURCES = [os.path.join('gravitas', x) for x in os.listdir('gravitas') if '.c' == x[-2:]]
_INCDIR = ['gravitas', np.get_include()]

class CustomBuildExt(build_ext):
    def build_extensions(self):
        super().build_extensions()

# _LIB_DIR
setup(
    name='gravitas',
    version='0.1.21',
    packages=find_packages(),
    license='GPL-2',
    long_description="""High-fidelity gravity fields for satellite propagation""",
    long_description_content_type='text/markdown',
    author="Liam Robinson",
    author_email="robin502@purdue.edu",
    install_requires=['numpy'],
    package_data={'gravitas': ['libgrav.h']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    ext_modules=[
        Extension(
            # the qualified name of the extension module to build
            'gravitas._grav',
            # the files to compile into our module relative to ``setup.py``
            sources=_SOURCES,
            include_dirs=_INCDIR
        ),
    ],
    cmdclass={
        'build_ext': CustomBuildExt,
    },
    zip_safe=False,  # Allow the package to be unzipped without modification
)