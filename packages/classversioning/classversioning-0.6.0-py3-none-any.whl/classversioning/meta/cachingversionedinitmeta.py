"""cachingversionedinitmeta.py
A mixed class of the CachingInitMeta and VersionMeta.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #
from baseobjects.cachingtools import CachingInitMeta

# Local Packages #
from .versionedmeta import VersionedMeta


# Definitions #
# Meta Classes #
class CachingVersionedInitMeta(CachingInitMeta, VersionedMeta):
    """A mixed class of the CachingInitMeta and VersionMeta."""
    ...
