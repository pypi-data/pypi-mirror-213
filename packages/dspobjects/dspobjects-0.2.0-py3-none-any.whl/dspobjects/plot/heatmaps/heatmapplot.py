""" heatmapplot.py

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
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #
import numpy as np
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go

# Local Packages #
from ..bases import Subplot, BasePlot


# Definitions #
# Classes #
class HeatmapPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_hovertemplate: str | None = "%{z:.4f} %{_z_unit}<br>" + "%{y:.4f} %{_y_unit}<br>" + "%{x:.4f} %{_x_unit}"
    default_color_sequence: list | None = None

    # Instance Methods #
    # Constructors/Destructors
    def build(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        labels: list | None = None,
        **kwargs: Any,
    ) -> None:
        super().build(
            x=x,
            y=y,
            z=z,
            labels=labels,
            **kwargs,
        )

        if self.z is not None:
            self.update_plot()

    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.colorscale = color

    def update_plot(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        labels: list | None = None,
        **kwargs: Any,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            z=z,
            labels=labels,
            **kwargs,
        )
        if len(self._traces["data"]) < 1:
            default_trace = go.Heatmap()
            self.add_traces((default_trace,), group="data")

        trace_iter = iter(self._traces["data"])
        trace = next(trace_iter)

        trace.update(
            dict(
                x=np.squeeze(self.generate_x(lengths=[self.z.shape[0]])),
                y=np.squeeze(self.generate_y(lengths=[self.z.shape[1]])),
                z=self.z,
            )
        )

        # Todo: Figure out how to add text

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.z = None
            trace.visible = False
