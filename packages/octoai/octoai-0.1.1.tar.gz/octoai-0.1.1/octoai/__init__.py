"""Initializes the octoai module."""
from importlib.metadata import version

from . import client, errors, models, types, utils

__version__ = version("octoai")
__all__ = ["client", "errors", "models", "server", "service", "types", "utils"]
