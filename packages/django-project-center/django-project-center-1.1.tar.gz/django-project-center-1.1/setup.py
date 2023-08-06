# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

REQUIREMENTS = [
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = []

setup(
    name='django-project-center',
    version='1.1',
    description='Project Management Module for Django',
    author='siteshell.net',
    author_email='pdbethke@siteshell.net',
    url='https://github.com/pdbethke/django-project-center',
    packages=find_packages(),
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