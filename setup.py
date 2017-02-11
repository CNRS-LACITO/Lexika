#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


__author__ = 'Benjamin Galliot'
__copyright__ = "Copyleft"
__license__ = "Spéciale"
__version__ = "0.1"
__email__ = "b.g01lyon@gmail.com"
__status__ = "Development Status :: 2 - Pre-Alpha"

setup(name='lexika',
      version=__version__,
      description='Interface graphique pour pylmflib',
      author='Benjamin Galliot',
      author_email='b.g01lyon@gmail.com',
      url='https://bitbucket.org/BenjaminGalliot/lexika',
      packages=find_packages(),
      install_requires=['cchardet', 'regex'],
      include_package_data=True,
      entry_points={'console_scripts': ['lexika=lexika:main'],},
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: End Users/Desktop",
                   "Intended Audience :: Other Audience",
                   "Natural Language :: French",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.6",
                   "Topic :: Software Development :: Build Tools",
                   "Topic :: Software Development :: Internationalization",
                   "Topic :: Software Development :: Localization",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Text Processing :: Linguistic",
                   "Topic :: Text Processing :: Markup :: XML",
                   "Topic :: Utilities"],
      keywords="linguistique dictionnairique lexicographie linguistics dictionaric lexicography",


)
