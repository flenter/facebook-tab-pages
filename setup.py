#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = [
        'django',
]

setup(
        name='facebook-tab-pages',
        version=".".join(map(str, __import__('fb_tabs').__version__)),
        author='Jacco flenter @ secretcodemachine',
        description='Link a view to an app/tabb on facebook',
        url='http://github.com/flenter/facebook-tab-pages',
        install_requires=[
            'django',
            ],
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            "Framework :: Django",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Software Development"
        ],
)
