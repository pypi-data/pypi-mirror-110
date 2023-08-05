from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='hello-dave-donaghy',
    version='0.0.5',
    description='Hello, World! Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dave-donaghy',
    author='Dave Donaghy',
    author_email='dave.donaghy@pm.me',
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4'
)
