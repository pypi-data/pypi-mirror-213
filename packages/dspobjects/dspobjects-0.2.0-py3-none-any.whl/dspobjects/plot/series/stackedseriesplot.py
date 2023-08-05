""" stackedseriesplot.py

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

# Local Packages #
from ..bases import Figure, Subplot
from .seriesplot import SeriesPlot


# Definitions #
# Classes #
class StackedSeriesPlot(SeriesPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_layout_settings: dict[str, Any] = SeriesPlot.default_layout_settings | dict(
        legend=dict(traceorder="reversed"),
    )
    default_xaxis_settings: dict[str, Any] = dict(
        showspikes=True,
        spikemode="across",
        autorange=True,
        fixedrange=True,
        rangeslider=dict(visible=True, autorange=False, thickness=0.04, borderwidth=1, yaxis=dict(rangemode="auto")),
    )
    default_yaxis_settings: dict[str, Any] = dict(
        showgrid=False,
        tickmode="array",
        autorange=False,
        fixedrange=False,
        showline=True,
        type="linear",
        zeroline=False,
    )
    default_hovertemplate: str | None = "%{text} %{_y_unit}<br>" + "%{x:.4f} %{_x_unit}"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: Iterable[str] | None = None,
        label_axis: bool = True,
        label_index: bool = True,
        tick_index_only: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        z_score: bool = True,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                labels=labels,
                label_axis=label_axis,
                label_index=label_index,
                tick_index_only=tick_index_only,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
                z_score=z_score,
                build=build,
                **kwargs,
            )
