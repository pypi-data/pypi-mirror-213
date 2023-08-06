from setuptools import setup, find_packages
from smash.version import author, version, homepage

with open("README.md", 'r') as f:
  long_description = f.read()

setup(
  author=author,
  author_email='dlek@p0nk.net',
  url=homepage,
  #project_urls={
  #  'Source': 'https://gitlab.com/dlek/smash-clients',
  #  'Tracker': 'https://gitlab.com/dlek/smash-clients/issues'
  #},
  python_requires='>=3.6',
  description='Smash clients',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  install_requires=['requests', 'emoji', 'mergeconf'],
  license="MIT license",
  include_package_data=True,
  name='smash-clients',
  packages=['smash'],
  version=version,
  entry_points = {
    'console_scripts': [
      'smash-xbar = smash.xbar:xbar',
      'smash = smash.cli:main',
    ],
  }
)
