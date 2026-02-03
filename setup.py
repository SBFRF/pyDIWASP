#!/usr/bin/env python
"""
Setup script for pyDIWASP package
"""

from setuptools import setup
import os

# Read the contents of README file
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Package version
__version__ = "1.4.0"

# Setup configuration
setup(
    name='pyDIWASP',
    version=__version__,
    description='DIrectional WAve SPectrum analysis for Python',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='SBFRF',
    author_email='',
    url='https://github.com/SBFRF/pyDIWASP',
    license='GPLv3',
    # Specify modules explicitly since the package structure is flat
    py_modules=['dirspec', 'infospec', 'interpspec', 'plotspec', 'writespec'],
    packages=['private'],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.15.0',
        'scipy>=1.1.0',
        'matplotlib>=3.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords='oceanography waves spectrum directional wave analysis diwasp',
    project_urls={
        'Source': 'https://github.com/SBFRF/pyDIWASP',
        'Original DIWASP': 'https://github.com/metocean/diwasp',
    },
    include_package_data=True,
    zip_safe=False,
)
