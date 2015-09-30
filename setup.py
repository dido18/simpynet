#!/usr/bin/env python
import os
import sys
from distutils.sysconfig import get_python_lib
from distutils.core import setup
from setuptools import find_packages

setup(name='simpynet',
      version='1.0',
      description='A simulator Python framework used to run simulations on all TCP/IP levels in a network',
      author=['Davide Neri','Artem Piazzi'],
      author_email='davideneri18@gmail.com',
      url='https://github.com/dido18/spn',
      packages=find_packages(),
      include_package_data=True,
      #packages=['simpynet'],
     )
