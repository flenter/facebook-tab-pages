#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


tests_require = [
        'django',
]

setup(
        name='facebook-tab-pages',
        version=".".join(map(str, __import__('fb_tabs').__version__)),
        author='Jacco flenter @ secretcodemachine',
        dependency_links=[
            'http://bitbucket.org/flenter/django-scm_core/get/default.tar.gz#egg=django-scm_core'
        ],
        description='Link a view to an app/tabb on facebook',
        url='http://github.com/flenter/facebook-tab-pages',
        install_requires=[
            'django >=1.3',
            'django-scm_core',
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
