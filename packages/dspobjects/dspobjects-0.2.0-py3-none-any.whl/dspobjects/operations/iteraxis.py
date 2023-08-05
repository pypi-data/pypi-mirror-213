""" iteraxis.py
A function that iterates over a specific dimension of a ndarray.
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

# Third-Party Packages #
import numpy as np

# Local Packages #


# Definitions #
# Functions #
def iteraxis(a: np.ndarray, axis: int = 0) -> np.ndarray:
    """Iterates over a given axis of an array.

    Args:
        a: The array to iterate through.
        axis: The axis to iterate over.

    Returns:
        The data at an element of the axis.
    """
    if axis == 0:
        return a
    else:
        return np.moveaxis(a, axis, 0)
