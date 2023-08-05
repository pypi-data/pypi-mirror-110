from setuptools import setup, find_packages
import pathlib

setup(
    name='hello-dave-donaghy',
    version='0.0.3',
    description='Hello, World! Python project',
    long_description='Hello, World! Python project',
    long_description_content_type='text/markdown',
    url='https://github.com/dave-donaghy/hello',
    author='Dave Donaghy',
    author_email='dave.donaghy@pm.me',
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4'
)
