from setuptools import setup, find_packages

setup(
    name='yfk',
    version='0.2.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
