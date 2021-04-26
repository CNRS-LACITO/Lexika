#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='lexika',
      version="1.0",
      description='Logiciel de création de dictionnaires multilingues.',
      author='Benjamin Galliot',
      author_email='b.g01lyon@gmail.com',
      url='https://gitlab.com/BenjaminGalliot/Lexika/',
      packages=find_packages(),
      install_requires=['cchardet', 'colorama', 'lxml', 'regex', 'pyyaml'],
      include_package_data=True,
      entry_points={'console_scripts': ['lexika=lexika.base:démarrer_lexika'],},
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: End Users/Desktop",
                   "Intended Audience :: Other Audience",
                   "Natural Language :: French",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.8",
                   "Topic :: Software Development :: Build Tools",
                   "Topic :: Software Development :: Internationalization",
                   "Topic :: Software Development :: Localization",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Text Processing :: Linguistic",
                   "Topic :: Text Processing :: Markup :: XML",
                   "Topic :: Utilities"],
      keywords="linguistique dictionnairique lexicographie linguistics dictionaric lexicography",
)
