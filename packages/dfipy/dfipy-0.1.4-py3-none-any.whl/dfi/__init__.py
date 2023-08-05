from importlib.metadata import version

__version__ = version("dfipy")

from .analysis import DFIAnalyse
from .connection import DFIConnect
from .getters import DFIGet
from .show import DFIShow
