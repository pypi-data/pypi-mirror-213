""" classifierpreformancegroup.py

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
from ...bases import BasePlot, PlotGroup
from .rocpercisionrecallgroup import ROCPrecisionRecallGroup


# Definitions #
# Classes #
class ClassifierPerformanceGroup(PlotGroup):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_layout_settings: dict[str, Any] = PlotGroup.default_layout_settings | dict(
        title=dict(text="Classifier Performance", font=dict(size=30), y=1.0, x=0.5, xanchor="center", yanchor="top"),
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
    default_subplot_settings: dict[str, Any] = dict(rows=2, cols=2, horizontal_spacing=0.05, vertical_spacing=0.05)
    default_plots: Mapping[str, BasePlot | PlotGroup] = dict(all=ROCPrecisionRecallGroup, test=ROCPrecisionRecallGroup)
    default_plot_settings: dict[str, dict[str, Any]] = dict(
        all=dict(
            plot_settings=dict(
                roc=dict(title=dict(text="All ROC", yanchor="bottom"), yaxis=dict(constraintoward="bottom")),
                precisionrecall=dict(title=dict(text="All Precision Recall"), yaxis=dict(constraintoward="bottom")),
            )
        ),
        test=dict(
            plot_settings=dict(
                roc=dict(title=dict(text="Test ROC"), yaxis=dict(constraintoward="top")),
                precisionrecall=dict(title=dict(text="Test Precision Recall"), yaxis=dict(constraintoward="top")),
            )
        ),
    )
    default_locations: dict[str, tuple[int, int]] = dict(
        all=dict(roc=(0, 0), precisionrecall=(0, 1)),
        test=dict(roc=(1, 0), precisionrecall=(1, 1)),
    )
    default_legend_group = "all"
