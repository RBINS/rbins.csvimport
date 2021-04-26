#-*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='rbins.csvimport',
      version=version,
      description="",
      long_description=open("README.rst").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone',
      url='http://www.naturalsciences.be',
      license='GPL',
      namespace_packages=['rbins'],
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "plone.api",
      ] ,
      entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
        """,
      extras_require={},
     )
