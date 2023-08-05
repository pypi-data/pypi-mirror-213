"""versionedclass.py
VersionedClass is an abstract class which has an associated version which can be used to compare against other
VersionedClasses. Typically, a base class for a version schema should directly inherit from VersionedClass then the
actual versions should inherit from that base class.
"""
# Package Header #
from .header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any, Iterable

# Third-Party Packages #
from baseobjects.versioning import VersionType
from baseobjects.versioning import Version

# Local Packages #
from .meta import VersionedMeta
from .versionregistry import VersionRegistry


# Definitions #
# Classes #
class VersionedClass(metaclass=VersionedMeta):
    """An abstract class allows child classes to specify its version which it can use to compare.

    Class Attributes:
        _registry: A registry of all subclasses and versions of this class.
        _dispatch_kwarg: The name of the kwarg to use for version dispatching when a new object is made.
        _registration: Specifies if versions will be tracked and will recurse to parent.
        _VERSION_TYPE: The type of version this object will be.
        VERSION: The version of this class as a string.
    """
    _registry: VersionRegistry = VersionRegistry()
    _dispatch_kwarg: str = "obj"
    _registration: bool = True
    _VERSION_TYPE: VersionType = None
    VERSION: Version = None

    # Meta Magic Methods
    # Construction/Destruction
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Adds the future child classes to the registry upon class instantiation"""
        super().__init_subclass__(**kwargs)

        if cls._VERSION_TYPE.head_class is None:
            cls._VERSION_TYPE.head_class = cls

        type_ = cls._VERSION_TYPE
        class_ = cls._VERSION_TYPE.class_

        if not isinstance(cls.VERSION, class_):
            cls.VERSION = class_(cls.VERSION)

        cls.VERSION.version_type = type_

        if cls._registration:
            cls._registry.add_item(cls, type_)

    # Class Methods
    @classmethod
    def get_version_from_object(cls, obj: Any) -> Version | str | Iterable:
        """An optional abstract method that must return a version from an object."""
        raise NotImplementedError("This method needs to be set in the version head to dispatch the propper class.")

    @classmethod
    def get_version_class(
        cls,
        version: Version | str | Iterable,
        type_: str | None = None,
        exact: bool = False,
        sort: bool = False,
    ) -> "VersionedClass":
        """Gets a class based on the version.

        Args:
            version: The key to search for the class with.
            type_: The type of class to get.
            exact: Determines whether the exact version is need or return the closest version.
            sort: If True, sorts the registry before getting the class.

        Returns:
            obj: The class found.
        """
        if type_ is None:
            type_ = cls._VERSION_TYPE

        if sort:
            cls._registry.sort(type_)

        return cls._registry.get_version(type_, version, exact=exact)

    @classmethod
    def get_latest_version_class(cls, type_: str | VersionType | None = None, sort: bool = False) -> "VersionedClass":
        """Gets a class based on the latest version.

        Args:
            type_: The type of class to get.
            sort: If True, sorts the registry before getting the class.

        Returns:
            obj: The class found.
        """
        if type_ is None:
            type_ = cls._VERSION_TYPE

        if sort:
            cls._registry.sort(type_)

        return cls._registry.get_latest_version(type_, cls)

    # Magic Methods
    # Construction/Destruction
    def __new__(cls, *args: Any, **kwargs: Any) -> "VersionedClass":
        """With given input, will return the correct subclass."""
        version_type = cls._registry.get_version_type(cls._VERSION_TYPE.name, None)
        if version_type is not None and version_type.head_class is cls and (kwargs or args):
            version = cls.get_version_from_object(args[0] if args else kwargs[cls._dispatch_kwarg])
            class_ = cls.get_version_class(version, type_=cls._VERSION_TYPE.name)
            return class_(*args, **kwargs)
        else:
            return super().__new__(cls)
