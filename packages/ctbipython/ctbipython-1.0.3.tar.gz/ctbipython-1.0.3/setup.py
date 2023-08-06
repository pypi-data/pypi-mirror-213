from setuptools import setup

setup(
    name='ctbipython',
    version='1.0.3',
    description='The goal of ctbi is to clean, decompose, impute and aggregate univariate time series.',
    author='Florian Guillet & François Ritter',
    packages=['ctbipython'],
    install_requires=['pandas','numpy','scipy','seaborn','matplotlib'],
)
