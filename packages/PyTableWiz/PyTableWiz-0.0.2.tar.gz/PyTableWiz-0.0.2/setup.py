from setuptools import setup, find_packages
 
classifiers = [
  'Operating System :: Microsoft :: Windows',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open("README.md", "r") as f:
  long_description = f.read()
 
setup(
  name='PyTableWiz',
  version='0.0.2',
  description='Creating tables for CSV data file',
  long_description=long_description,
  long_description_content_type = "text/markdown",
  url='https://github.com/PramudithRangana/Table-Wizard.git',
  author='Pramudith Rangana',
  author_email='pramudithrangana@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='CSV, table', 
  packages=find_packages(),
  install_requires=[''] 
)

