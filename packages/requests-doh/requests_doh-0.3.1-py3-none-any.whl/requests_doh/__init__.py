"""
DNS over HTTPS resolver for python requests
"""

__version__ = "0.3.1"
__description__ = "DNS over HTTPS resolver for python requests"
__author__ = "Rahman Yusuf"
__author_email__ = "danipart4@gmail.com"
__license__ = "MIT"
__repository__ = "mansuf/requests-doh"

from .session import *
from .adapter import *
from .resolver import *
from .connector import *
from .exceptions import *