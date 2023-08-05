# completeness/setup.py
from setuptools import setup, find_packages

setup(
    name='completeness_ratio_check',
    version='0.1',
    author="JeeAnRyu",
    description="A python package to calculate and visualize the completeness ratio of data in CSV files.",
    license="MIT",
    keywords="data analysis, completeness ratio, csv",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib'
    ],
)
