from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='graphce',
    version='0.0.2',
    description='Working with databases related to IP, phone, and email information.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='authsafe',
    packages=find_packages(),
    install_requires=['sqlitedict', 'phonenumbers']
)