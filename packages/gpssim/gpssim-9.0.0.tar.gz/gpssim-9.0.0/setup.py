import sys

if not 'sdist' in sys.argv:
    sys.exit('\n*** Please install the `nmeasim` package (instead of `gpssim`) ***\n')

from setuptools import setup
setup()
