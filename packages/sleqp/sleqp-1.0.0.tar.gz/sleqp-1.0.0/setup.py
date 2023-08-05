from setuptools import setup, find_packages
from setuptools.extension import Extension

import os
import subprocess

import numpy

project_description = 'Active set-based NLP solver'
long_description = 'This package provides SLEQP, an open-source solver for large-scale nonlinear continuous optimization. SLEQP is available as a callable library with interfaces to C, Python, AMPL, and MATLAB / Octave. It uses an active set method based on a combination of successive linear programming and equality constrained quadratic programming.'
project_name = 'sleqp'
project_version = '1.0.0'
license_file = 'LICENSE.txt'
maintainer_name = 'Christoph Hansknecht'
maintainer_email = 'c.hansknecht@tu-braunschweig.de'

local_env = os.getenv('SLEQP_LOCAL_BUILD')
local_build = (local_env is not None)

ldflags = []
cflags = []
lib_dirs = []
include_dirs = []


def pkgconfig(name):

    def pkgconfig_get(flags):
        res = subprocess.run(['pkg-config', flags, name],
                             stdout=subprocess.PIPE,
                             check=True)

        return res.stdout.decode().strip().split()

    cflags = pkgconfig_get('--cflags-only-other')

    includes = pkgconfig_get('--cflags-only-I')

    libs = pkgconfig_get('--libs-only-l')

    libdirs = pkgconfig_get('--libs-only-L')

    return {'cflags': cflags,
            'includes': includes,
            'libs': libs,
            'libdirs': libdirs}


if not(local_build):
    pkgconfig_args = pkgconfig(project_name)

    ldflags += pkgconfig_args['libs']
    cflags += pkgconfig_args['cflags']
    lib_dirs += pkgconfig_args['libdirs']
    include_dirs += pkgconfig_args['includes']


extensions = [
    Extension("sleqp.sleqp",
              ['src/extension/sleqp.pyx'],
              include_dirs=[numpy.get_include()] + include_dirs,
              libraries=[project_name],
              extra_link_args=ldflags,
              library_dirs=lib_dirs,
              extra_compile_args=cflags
              )]

requirements = []

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name=project_name,
      author=maintainer_name,
      author_email=maintainer_email,
      description=(project_description),
      license_file=license_file,
      long_description=long_description,
      version=project_version,
      ext_modules=extensions,
      packages=find_packages(where="src", exclude=["tests"]),
      package_dir={"": "src"},
      install_requires=requirements,
      setup_requires=['wheel'],
      classifiers=[
        'Programming Language :: Cython',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics'
      ],
      test_suite='tests')
