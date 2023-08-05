from setuptools import setup, find_packages

setup(
name='sceleto',
license='LICENSE',
#url='NULL'
author='Jongeun Park',
author_email='jp24@kaist.ac.kr',
description='Tool to aid in single cell analysis (temporary description)',
#####Package#####
include_package_data=True,
python_requires='>=3.7',
packages=find_packages(include=['sceleto','sceleto.*','.']),
#####Needed dependencies#####
install_requires=[
   'pandas',
   'numpy',
   'scanpy>=1.6.1',
   'scipy',
   'seaborn',
   'networkx',
   'python-igraph==0.9.1',
   'bbknn==1.4.1',
   'scikit-learn==0.22',
   'scrublet',
   'joblib',
   'datetime',
   'harmonypy',
   'matplotlib',
   'geosketch==0.3',
   'scrublet',
   'adjustText',
   'numba==0.51.2'
],
#####Sharing#####
version='0.9.8',
#####Search#####
keywords=['sceleto', 'single cell', 'scRNA-seq'],
#####Read Me#####
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
zip_safe=False,
)
