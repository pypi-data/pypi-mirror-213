"""__init__.py
Meta classes for class versioning.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .versionedmeta import VersionedMeta
from .versionedinitmeta import VersionedInitMeta
from .cachingversionedinitmeta import CachingVersionedInitMeta
