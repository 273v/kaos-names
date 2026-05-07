"""Friendly legal-flavored name generation for KAOS sessions and agents."""

from kaos_names._version import __version__
from kaos_names.names import (
    DEFAULT_DESCRIPTORS,
    DEFAULT_NOUNS,
    generate_combination,
    generate_name,
    generate_session_name,
)

__all__ = [
    "DEFAULT_DESCRIPTORS",
    "DEFAULT_NOUNS",
    "__version__",
    "generate_combination",
    "generate_name",
    "generate_session_name",
]
