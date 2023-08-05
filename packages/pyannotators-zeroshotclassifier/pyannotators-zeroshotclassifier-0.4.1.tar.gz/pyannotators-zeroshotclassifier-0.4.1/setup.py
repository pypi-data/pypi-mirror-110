#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pyannotators_zeroshotclassifier']

package_data = \
{'': ['*']}

package_dir = \
{'': 'src'}

install_requires = \
['pymultirole-plugins>=0.4.0,<0.5.0',
 'torch==1.7.1',
 'protobuf',
 'sentencepiece',
 'transformers',
 'PyICU']

extras_require = \
{'dev': ['flit', 'pre-commit', 'bump2version'],
 'docs': ['sphinx',
          'sphinx-rtd-theme',
          'm2r2',
          'sphinxcontrib.apidoc',
          'jupyter_sphinx'],
 'test': ['pytest',
          'pytest-cov',
          'pytest-flake8',
          'pytest-black',
          'hypothesis',
          'tox']}

entry_points = \
{'pyannotators.plugins': ['zeroshotclassifier = '
                          'pyannotators_zeroshotclassifier.zeroshotclassifier:ZeroShotClassifierAnnotator']}

setup(name='pyannotators-zeroshotclassifier',
      version='0.4.1',
      description='Annotator based on Huggingface transformer',
      author='Olivier Terrier',
      author_email='olivier.terrier@kairntech.com',
      url='https://github.com/oterrier/pyannotators_zeroshotclassifier/',
      packages=packages,
      package_data=package_data,
      package_dir=package_dir,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.8',
     )
