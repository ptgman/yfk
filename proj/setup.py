from setuptools import setup, find_packages

setup(
    name='yfk',
    version='0.1.4', # do not adjust time zone.
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
