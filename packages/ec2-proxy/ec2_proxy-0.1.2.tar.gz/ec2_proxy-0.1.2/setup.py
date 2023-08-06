#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Suraj Bhari",
    author_email='surajbhari159@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="This package provides ability to use amazon aws as proxy with everchanging IP.",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ec2_proxy',
    name='ec2_proxy',
    packages=find_packages(include=['ec2_proxy', 'ec2_proxy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AG4lyf/ec2_proxy',
    version='0.1.2',
    zip_safe=False,
)
