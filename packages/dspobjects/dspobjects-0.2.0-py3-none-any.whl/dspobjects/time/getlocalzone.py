""" getlocalzone.py
Gets the local time zone.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from datetime import timedelta, timezone
import time

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def get_localzone() -> timezone:
    """Gets the local time zone.

    Returns:
        The system's current time zone.
    """
    local_time = time.localtime()
    return timezone(timedelta(seconds=local_time.tm_gmtoff), local_time.tm_zone)
