""" spectrogramgroup.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Mapping
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BasePlot, PlotGroup, XAssignments
from ..series import TimeSeriesPlot
from .spectrogramplot import SpectrogramPlot


# Definitions #
# Classes #
class SpectrogramGroup(PlotGroup):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_layout_settings: dict[str, Any] = PlotGroup.default_layout_settings | dict(
        modebar_add=[
            "zoom",
            "pan",
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
        ],
    )
    default_subplot_settings: dict[str, Any] = dict(rows=2, cols=1, vertical_spacing=0.01, row_heights=[0.9, 0.1])
    default_plots: Mapping[str, BasePlot | PlotGroup] = dict(spectrogram=SpectrogramPlot, timeseries=TimeSeriesPlot)
    default_locations: dict[str, tuple[int, int]] = dict(spectrogram=(0, 0), timeseries=(1, 0))
    default_plot_settings: dict[str, dict[str, Any]] = dict(
        timeseries=dict(label_index=False, label_axis=False, trace_settings=dict(showlegend=False))
    )
    default_xaxes_assignment: XAssignments = (("spectrogram", "timeseries"),)
