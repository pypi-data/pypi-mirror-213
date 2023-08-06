from setuptools import setup,find_packages

requirements=[r.strip() for r in open("requirements.txt").readlines()]

setup(
   name='transphone',
   version='1.5.3',
   description='a multilingual g2p/p2g model',
   author='Xinjian Li',
   author_email='xinjianl@cs.cmu.edu',
   url="https://github.com/xinjli/transphone",
   packages=find_packages(),
   package_data={'': ['*.csv', '*.tsv', '*.yml']},
   install_requires=requirements,
)
