## -*- encoding: utf-8 -*-
r"""
Setup script for installing the ``topological-recursion`` module.

This uses `setuptools`. See https://docs.python.org/3/distutils/setupscript.html
for details.
"""
import os
import sys
from setuptools import setup
from codecs import open

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding="utf-8") as f:
        return f.read()

setup(
    name="topological-recursion",
    version=readfile("VERSION").strip(), # get version from VERSION
    description="Topological recursion",
    long_description=readfile("README.rst"), # get the long description from the README.rst
    url="https://gitlab.com/toprec/toprec",
    author="Vincent Delecroix, Bertrand Eynard, Dimitrios Mitsios",
    author_email="bertrand.eynard@ipht.fr",
    license="GPLv2+",
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Science/Research",
      "Topic :: Scientific/Engineering :: Mathematics",
      "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
      "Programming Language :: Python :: 3"
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "topological-recursion surfaces geometry",
    packages = ["topological_recursion"],
)
