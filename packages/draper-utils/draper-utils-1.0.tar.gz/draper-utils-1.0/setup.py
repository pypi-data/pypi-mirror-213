# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

REQUIREMENTS = [
    'django',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = []

setup(
    name='draper-utils',
    version='1.0',
    description='Project Management Module for Django - Utils',
    author='siteshell.net',
    author_email='pdbethke@siteshell.net',
    url='https://github.com/pdbethke/draper-utils',
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'draper_utils': 'draper_utils'},
    package_data={'draper_utils': ['sql/*', 'management/*', 'migrations/*']},
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    # test_suite="test_settings.run",
)
