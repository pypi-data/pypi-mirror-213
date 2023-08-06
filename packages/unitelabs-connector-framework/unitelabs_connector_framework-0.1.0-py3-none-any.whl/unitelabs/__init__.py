from importlib.metadata import version

from .connector import Connector

__version__ = version("unitelabs_connector_framework")
__all__ = ["__version__", "Connector"]
