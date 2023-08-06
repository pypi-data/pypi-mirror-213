""" A conversion system to ease converting between different types.

This will be especially useful types <-> models conversions.
"""
# Initialize all optional integrations.
from . import integrations  # noqa: F401, E402
from .conversion import convert  # noqa: F401
from .enums import Strategy  # noqa: F401
from .exc import (  # noqa: F401
    ConverterAlreadyExists,
    Error,
    NoConverter,
    TypeNotSupported,
)
from .iterators import field_iterator  # noqa: F401
from .mappers import alias, set_const, use_default  # noqa: F401
from .registry import register, register_iso  # noqa: F401
from .types import ConverterFn, FieldIterator, MappingFn, TypeConverter  # noqa: F401


__version__ = '0.3.5'
