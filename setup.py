#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup
from setuptools import find_packages



project_name='hxapi_g'

def get_version(*file_paths):
    """Retrieves the version from [your_package]/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version(project_name, "__init__.py")


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'google-auth',
    'google-auth-httplib2',
    'google-api-python-client',
]

test_requirements = [
    'pytest',
]

setup(
    name=project_name,
    version=version,
    description="hx package to integrate with google docs",
    long_description=readme,
    author="nmaekawa",
    author_email='nmaekawa@g.harvard.edu',
    url='https://github.com/nmaekawa/' + project_name,
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependencies,
    zip_safe=False,
    keywords='hx googlesheets ' + project_name,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
