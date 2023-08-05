from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding = "utf-8") as fh:
        long_description = fh.read()

setup(
    name='ClosedAPI',
    version='0.2',
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
    long_description = long_description,
    long_description_content_type = "text/markdown",
)
