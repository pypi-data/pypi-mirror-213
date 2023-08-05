"""versionedinitmeta.py
A mixed class of the InitMeta and VersionMeta.
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
from baseobjects.metaclasses import InitMeta

# Local Packages #
from .versionedmeta import VersionedMeta


# Definitions #
# Meta Classes #
class VersionedInitMeta(InitMeta, VersionedMeta):
    """A mixed class of the InitMeta and VersionMeta."""
    ...
