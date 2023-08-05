""" precisionrecallplot.py

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
from typing import Any

# Third-Party Packages #
import plotly.graph_objects as go
from plotly.basedatatypes import BaseTraceType

# Local Packages #
from .thresholdperformanceplot import ThresholdPerformancePlot


# Definitions #
# Classes #
class PrecisionRecallPlot(ThresholdPerformancePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_title_settings: dict[str, Any] = dict(text="Precision Recall")
    default_xaxis_settings: dict[str, Any] = ThresholdPerformancePlot.default_xaxis_settings | dict(
        title="Recall",
    )
    default_yaxis_settings: dict[str, Any] = ThresholdPerformancePlot.default_yaxis_settings | dict(
        title="Precision",
    )
    default_static_traces: dict[str, BaseTraceType] = {
        "performance_line": go.Scattergl(
            x=[0, 1],
            y=[0, 0],
            mode="lines",
            line=dict(width=6, color="black", dash="dash"),
        ),
    }
    default_x_unit = "Recall"
    default_y_unit = "Precision"
