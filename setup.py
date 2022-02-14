from setuptools import setup, find_packages
from PublisherAzureTestsResults.version import VERSION

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3'
]

setup(
  name='robotframework-publisher-results-azure',
  url='https://github.com/ismailktami/robotframework-publisher-results-azure',
  version=VERSION,
  description='Library to publish robot framework automation results on azure',
  author='Ismail Ktami',
  author_email='ktamiismail@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='robotframework azure devops testplans results outcomes', 
  packages=find_packages(),
  install_requires=[
    'robotframework>=3.2.2',
    'requests',
    'utils'
  ] 
)