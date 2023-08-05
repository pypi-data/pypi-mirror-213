# coding: utf-8
from pathlib import Path
from setuptools import setup
from versao import version_info

long_description = Path("README.rst").read_text()

setup(
    name='colibri-packaging',
    author='Colibri Agile',
    author_email='colibri.agile@gmail.com',
    platforms=['Windows'],
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html'
    version=version_info()['fileversion'],
    description='Colibri Master Packages generator',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=[
        'colibri_packaging'
    ],
    package_data={
        'colibri_packaging': ['7za.exe']
    },
    data_files=[('', ['versao.py', '__version__.py', '__buildnumber__.py'])],
    classifiers=[
        'Programming Language :: Python :: 3.11'
    ],
    python_requires='>=3.11'
)
