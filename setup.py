from setuptools import setup, find_packages
from .version import VERSION

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3'
]

setup(
  name='robotframework-azure-results',
  version=VERSION,
  description='Library robot framework for publish results tests',
  author='Ismail Ktami',
  author_email='ktamiismail@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='robotframework azure devops testplans', 
  packages=find_packages(),
  install_requires=[
    'robotframework>=3.2.2',
    'requests',
    'json',
    'utils'
  ] 
)