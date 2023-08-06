from setuptools import setup, find_packages

classifiers = [
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Education',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3'


]

setup(

name = 'archeSetup',
version='0.0.7',
description='This is the setup for the basic Application library for reading the files and extract the data from the txt/lof files. Also, we can convert the data to csv files',
long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
url='',
author='Arche',
author_email='rkdyava@gmail.com',
classifiers=classifiers,
keywords='Setup',
packages=find_packages(),
install_requires=['']





)