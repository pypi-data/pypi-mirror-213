"""
toolkit library, for Discord Catho bot ("dkto")
"""

# Errors
from .exceptions import ParseError

# Variables
from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
    __pkg_name__,
)

# Functions
from .dict import dict2obj
from .list import replace_with_mask, castList
from .str import str2digit
from .datestr import parser_date, date2str
from .envvar import load_dotenv, getEnvironVar, getTimesReminder
from .exceptions import ParseError
from .functions import compatMode
from .function_recursive import recurs_function
from .parserhtml import ParserHTML

# Declaration explicite de tous les modules (pep8)
__all__ = [
    'ParseError',
    '__author__', '__author_email__',
    '__copyright__', '__description__', '__license__',
    '__title__', '__version__', '__pkg_name__',
    'dict2obj',
    'replace_with_mask', "castList",
    'str2digit',
    'parser_date', 'date2str',
    'load_dotenv', 'getEnvironVar', 'getTimesReminder',
    'compatMode', 'recurs_function',
    'ParserHTML'
]
