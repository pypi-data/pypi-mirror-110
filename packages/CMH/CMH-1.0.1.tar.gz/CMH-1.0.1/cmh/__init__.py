"""Cochran-Mantel-Haenzsel Chi2 Test.

Code ported from/based on "Categorical Data Analysis", page 295 by Agresti
(2002) and R implementation of the function `mantelhaen.test()`.
"""
__author__ = """Melle Sieswerda"""
__email__ = 'm.sieswerda@iknl.nl'

# __version__
from ._version import __version__  # noqa

# main code
from .cmh import CMH # noqa
