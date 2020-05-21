from setuptools import setup, find_packages

setup(
    name='dev_droga_courses',
    version='0.0.1dev',
    packages=find_packages('src', exclude=('tests', )),
    package_dir={'': 'src'},
    classifiers=['Programming Language :: Python :: 3.8'],
    install_requires=[
        'returns==0.13',
        'injector==0.18.3',
    ],
)
