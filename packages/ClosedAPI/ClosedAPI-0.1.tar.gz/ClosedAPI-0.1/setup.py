from setuptools import setup, find_packages
import os

setup(
    name='ClosedAPI',
    version='0.1',
    license='MIT',
    author="Syirezz, Kararasenok_gd",
    author_email='email@syirezz.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/kararasenok-gd/krrsnkapi',
    keywords='',
    install_requires=[
          'requests'
      ],
    long_description= "README.md"
)
