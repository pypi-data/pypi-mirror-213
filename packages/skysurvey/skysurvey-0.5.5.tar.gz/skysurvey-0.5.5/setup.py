#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
from distutils.core import setup
from setuptools import setup, find_packages


packages = find_packages()

VERSION = '0.5.5'
        
setup(name='skysurvey',
      version=VERSION,
      description='Simulating Transient in the sky and how to observe them',
      author='Mickael Rigault',
      author_email='m.rigault@ipnl.in2p3.fr',
      url='https://github.com/MickaelRigault/skysurvey',
      packages=packages,

     )
# End of setupy.py ========================================================


