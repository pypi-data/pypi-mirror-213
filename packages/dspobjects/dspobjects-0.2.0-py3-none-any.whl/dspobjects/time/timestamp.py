""" timestamp.py
Extends the pandas Timestamp class.
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
from datetime import datetime, timezone, tzinfo, timedelta
from decimal import Decimal
import time

# Third-Party Packages #
import numpy as np
import pandas as pd

# Local Packages #
from .getlocalzone import get_localzone


# Definitions #
NANO_SCALE = np.uint64(10**9)


# Classes #
class Timestamp(pd.Timestamp):
    """Extends the pandas Timestamp class."""

    _UNIX_EPOCH = pd.Timestamp(1970, 1, 1)
    UNIX_EPOCH = pd.Timestamp(1970, 1, 1).replace(tzinfo=timezone.utc)

    # Class Methods #
    @classmethod
    def fromnanostamp(cls, t: float | int | np.dtype | Decimal, tz: tzinfo | None = None) -> "Timestamp":
        """Creates a Timestamp object from a nanostamp.

        Args:
            t: The nanostamp to create a Timestamp from.
            tz: The time zone information.

        Returns:
            A Timestamp that is the time of the nanostamp.
        """
        if isinstance(t, Decimal):
            t = int(t)

        if tz is None:
            local_time = time.localtime()
            return cls._UNIX_EPOCH + pd.Timedelta(seconds=local_time.tm_gmtoff, nanoseconds=t)
        else:
            return cls.UNIX_EPOCH.astimezone(tz=tz) + pd.Timedelta(nanoseconds=t)

    @classmethod
    def fromdecimal(cls, t: Decimal, tz: tzinfo | None = timezone.utc) -> "Timestamp":
        """Creates a Timestamp object from a numeric timestamp as Decimal object.

        Args:
            t: The timstamp to creat a Timestamp object from.
            tz: THe time zone information

        Returns:
            A Timestamp that is the time of the Decimal timestamp.
        """
        integer = np.uint64(round(t))
        nts = integer * NANO_SCALE + np.uint64(t - integer) * NANO_SCALE

        if tz is None:
            local_time = time.localtime()
            return cls._UNIX_EPOCH + pd.Timedelta(seconds=local_time.tm_gmtoff, nanoseconds=nts)
        else:
            return cls.UNIX_EPOCH.astimezone(tz=tz) + pd.Timedelta(nanoseconds=nts)

    # Instance Methods #
    # def nanostamp(self) -> np.uint64:
    #     return np.uint64((self - self.UNIX_EPOCH.replace(tzinfo=self.tz)).value)
