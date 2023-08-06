# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  setup_requires='git-versiointi>=1.6rc3',
  name='python-takauma',
  description='Python-moduulien tiedostoversiointi',
  url='https://github.com/an7oine/python-takauma.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@pispalanit.fi',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  extras_require={
    'kehitys': ['git-versiointi>=1.4.4'],
  },
)
