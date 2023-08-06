from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyqt5-utils',
    version='1.0.3',
    description='Utilities for PyQt5',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hadi Hassan',
    author_email='hassanhadi17@hotmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
)
