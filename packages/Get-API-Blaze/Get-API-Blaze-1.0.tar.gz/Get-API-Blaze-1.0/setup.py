from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='Get-API-Blaze',
    version=1.0,
    description='This package facilitates the data collection process directly from the blaze API by generating a list or a dictionary to work more easily with the blaze double or crash data.',
    long_description=Path('README.md').read_text(),
    author='Ramon',
    author_email='ramonma31@gmail.com',
    keywords=['blaze', 'api', 'get api', 'double', 'crash'],
    packages=find_packages()
)