from setuptools import setup, find_packages

setup(
    name='stepwiseadrian',
    version='1.0',
    author='Adrian Glazer',
    author_email='adrianbadjideh01@gmail.com',
    description='This package is make for selecting best attribute to build multiple linear regression using stepwise selection',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
    ],
)