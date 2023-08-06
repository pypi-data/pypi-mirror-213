from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'A comprehensive toolkit for climate impact analysis.'
LONG_DESCRIPTION = 'A package that allows researchers, analysts, and climate enthusiasts to dissect complex climate data.'

# Setting up
setup(
    name="climalysis",
    version=VERSION,
    author="Jake Casselman",
    author_email="<jake.casselman@climalinks.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
    ],
    keywords=['python', 'climate', 'analysis', 'climate analysis', 'climate data', 'impact analysis'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ]
)
