from pdb import set_trace
import pkg_resources

from .write.writer_nc import write_nc_legacy
from .config import get_config
from . import config, parse, write

__version__ = pkg_resources.get_distribution("linc").version

__all__ = [
    "write_nc_legacy",
    "get_config",
    "parse",
    "write",
    "config",
]