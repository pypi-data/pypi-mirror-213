#!/usr/bin/env python3

# Copyright (C) 2016-2021
# Please see the accompanying LICENSE file for further information.

import re
import sys
from setuptools import setup, find_packages

python_min_version = (3, 6)
python_requires = '>=' + '.'.join(str(num) for num in python_min_version)

if sys.version_info < python_min_version:
    raise SystemExit('Python 3.6 or later is required!')

with open('README.rst') as fd:
    long_description = fd.read()

# Get the current version number:
with open('cogef/__init__.py') as fd:
    version = re.search("__version__ = '(.*)'", fd.read()).group(1)


package_data = {'cogef': ['test/*.dat']}

setup(name='ase-cogef',
      version=version,
      description='COnstrained Geometries simulate External Force',
      url='https://gitedit.gitlab.io/cogef',
      maintainer='Michael Walter',
      maintainer_email='mcoywalter@gmail.com',
      license='LGPLv2.1+',
      platforms=['unix'],
      packages=find_packages(),
      install_requires=['numpy', 'ase'],
      extras_require={'docs': ['sphinx', 'sphinx_rtd_theme', 'matplotlib']},
      package_data=package_data,
      entry_points={'console_scripts': ['cogef=cogef.cli.main:main']},
      long_description_content_type='text/x-rst',
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: '
          'GNU Lesser General Public License v2 or later (LGPLv2+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Physics'])
