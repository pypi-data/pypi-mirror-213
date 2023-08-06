from setuptools import setup, find_packages
setup(
   name='vartex',
   version='0.0.1',
   author='Sahil Pattni',
   author_email='sahilpattni97+vartex@gmail.com',
   description='A tool to compile multiple LateX files from a single template.',
   packages=find_packages(),
   entry_points={
      'console_scripts': [
         'vartex = vartex.cli:main'
      ],
   },
)