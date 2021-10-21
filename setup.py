import unittest

from setuptools import setup, find_packages


def test_suite():
    return unittest.TestLoader().discover('src', pattern='*.py')


setup(
    name='dev_droga_courses',
    version='0.0.1dev',
    packages=find_packages('src', exclude=('tests', )),
    package_dir={'': 'src'},
    test_suite='setup.test_suite',
    classifiers=['Programming Language :: Python :: 3.8'],
    install_requires=[
        'returns==0.13',
        'injector==0.18.3',
        'SQLAlchemy==1.3.17',
        'SQLAlchemy_utils==0.36.5',
        'Babel==2.9.1',
    ],
    tests_require=[
        'factory_boy==2.12.0',
    ],
)
