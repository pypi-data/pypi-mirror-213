"""Setup file for pyhip building/installing"""
from glob import glob
import os
import sys
import platform
from distutils.sysconfig import parse_makefile
from setuptools import setup, find_packages#, Extension

NAME = "pyhip"
VERSION = "0.7.0"
DESCR = """A Python interface to Hip which is a package for manipulating
           unstructured computational grids and their associated datasets"""
URL = "http://www.cerfacs.fr/avbp7x/hip.php"

AUTHOR = "Jens-Dominik Mueller, CERFACS"
EMAIL = "j.mueller@qmul.ac.uk, gabriel.staffelbach@cerfacs.fr, erraiya@cerfacs.fr"

LICENSE = "CeCILL-B Free Software License Agreement (CECILL-B)"

SRC_DIR = "pyhip"
PACKAGES = [SRC_DIR]
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
# EXT = build_extension()

setup(name=NAME,
      version=VERSION,
      description=DESCR,
      long_description=README,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license=LICENSE,
      packages=find_packages("src"),
      package_dir={"": "src"},
      py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
      include_package_data=True,
      #data_files = [('bin', ['./src/pyhip/hip_Linux.exe','./src/pyhip/hip_Darwnin.exe'])],
      zip_safe=False,
      python_requires='>=3.6.0',
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Topic :: Scientific/Engineering :: Physics"
                   ],
      setup_requires=[#"Cython",
                      "sdist",
                      "wheel",
                      "numpy",
                      "nob",
                      'reportlab',
                      "PyYAML",
                      "matplotlib",
                      "scipy",
                      "arnica",
                      "opentea>=3.1.0"],
      install_requires=["numpy",
                        "nob",
                        "reportlab",
                        "PyYAML",
                        "matplotlib",
                        "scipy",
                        "arnica",
                        "opentea>=3.1.0"],
      entry_points={
        "console_scripts": [
            "ihm_hip = pyhip.gui.startup:main",
            "pyhip = pyhip.cli:main_cli",
            ]
      }
      )
