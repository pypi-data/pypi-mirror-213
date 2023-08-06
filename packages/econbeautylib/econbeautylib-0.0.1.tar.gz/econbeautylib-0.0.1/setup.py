# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 18:07:05 2022
@author:
Зайцева Дарья
"""

from setuptools import setup, find_packages
long_description = '''Library for the 5 semester'''
setup(name='econbeautylib',
      version='0.0.1',
      url='https://github.com/dashkazaitseva',
      packages=['econbeautylib'],
      license='MIT',
      description='',
      zip_safe=False,
      package_data={'econbeautylib': ['*.txt', '*.docx']},
      include_package_data=True
      )