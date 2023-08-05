""" timespectragroup.py

"""
# Package Header #
from ....header import *

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
from ...bases import BasePlot, PlotGroup, YAssignments
from .timeseriesplot import TimeSeriesPlot
from .spectraplot import SpectraPlot


# Definitions #
# Classes #
class TimeSpectraGroup(PlotGroup):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_layout_settings: dict[str, Any] = PlotGroup.default_layout_settings | dict(
        dragmode="zoom",
        legend=dict(traceorder="reversed"),
        template="plotly_white",
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
    default_subplot_settings: dict[str, Any] = dict(rows=1, cols=2, horizontal_spacing=0.01)
    default_plots: Mapping[str, BasePlot | PlotGroup] = dict(timeseries=TimeSeriesPlot, spectra=SpectraPlot)
    default_locations: dict[str, tuple[int, int]] = dict(timeseries=(0, 0), spectra=(0, 1))
    default_plot_settings: dict[str, dict[str, Any]] = dict(
        timeseries=dict(title=dict(text="Time Series")),
        spectra=dict(title=dict(text="Spectra")),
    )
    default_yaxes_assignment: YAssignments = (("spectra", "timeseries"),)
    default_legend_group = "all"
