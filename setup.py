#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = '1.0'

setup(name='supervision.website',
      version=version,
      description="supervision.website provides utils to supervise websites.",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='python web supervision',
      author='Sylvain Boureliou [sylvainb]',
      author_email='sylvain.boureliou@gmail.com',
      url='http://www.asilax.fr',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['supervision'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points={
      },
      setup_requires=["PasteScript"],
      paster_plugins=["templer.localcommands"],
      )
