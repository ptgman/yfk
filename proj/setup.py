from setuptools import setup, find_packages

setup(
    name='yfk',
    version='0.1.6',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
