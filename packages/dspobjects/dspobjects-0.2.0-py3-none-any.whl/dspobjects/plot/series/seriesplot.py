""" seriesplot.py

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
from collections.abc import Iterable, Iterator, Sized
from typing import Any
import itertools

# Third-Party Packages #
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go
import numpy as np

# Local Packages #
from ...operations import iteraxis
from ..bases import Figure, Subplot, BasePlot


# Definitions #
# Classes #
class SeriesPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_layout_settings: dict[str, Any] = BasePlot.default_layout_settings | dict(
        dragmode="zoom",
        template="plotly_white",
        margin=dict(t=50, b=50),
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
    default_xaxis_settings: dict[str, Any] = {}
    default_yaxis_settings: dict[str, Any] = {}
    default_trace_settings: dict[str, Any] = dict(
        mode="lines",
        line={"width": 1},
        showlegend=True,
    )

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: Iterable[str] | None = None,
        label_axis: bool = False,
        label_index: bool = True,
        tick_index_only: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 0,
        z_score: bool = False,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._z_score: bool = False

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

    @property
    def z_score(self) -> bool:
        return self._z_score

    # Instance Methods #
    # Constructors/Destructors
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs: Any,
    ) -> None:
        if z_score is not None:
            self._z_score = z_score

        super()._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

    def build(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs: Any,
    ) -> None:
        super().build(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )

        if self.y is not None:
            self.update_plot()

    def text_iterator(self, lengths: Iterable[int] | None = None) -> Iterator:
        if self._text is None:
            if self._z_score:
                return (tuple(f"{v:.4f}" for v in c) for c in self.y_iterator(lengths=lengths))
            else:
                return ([""] * length for length in lengths)
        elif isinstance(self._text, np.ndarray):
            return iteraxis(self._text, self._c_axis)
        elif isinstance(self._text, Sized) and len(self._text) == 1:
            return itertools.repeat(self._text[0], len(lengths))
        else:
            return iter(self._text)

    # TraceContainer
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.update(line=dict(color=color))

    def _update_data(self, lengths, labels) -> None:
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_legend_group = self._figure.get_legendgroups()
        else:
            existing_legend_group = {}

        # Trace Names
        names = self.generate_names(names=labels)

        # Z Score Y Data
        if self.z_score:
            y_iter = (((y_c - np.nanmean(y_c)) / np.nanstd(y_c)) for y_c in self.y_iterator(lengths=lengths))
        else:
            y_iter = self.y_iterator(lengths=lengths)

        # Apply Data to TraceContainer
        x_iter = self.x_iterator(lengths=lengths)
        text_iter = self.text_iterator(lengths=lengths)
        trace_iter = iter(self._traces["data"])
        trace_data = zip(x_iter, y_iter, text_iter, trace_iter)
        for i, (x_c, y_c, text_c, trace) in enumerate(trace_data):
            trace.x = x_c
            trace.y = y_c + (i * self._trace_offset)
            trace.name = names[i]
            if self._group_existing_legend:
                trace.legendgroup = names[i]
            if names[i] in existing_legend_group:
                trace.showlegend = False
            trace.text = text_c
            trace.visible = True

        # Turn Off Unused TraceContainer
        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def update_data(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )
        # Data Info
        lengths = [len(y_c) for y_c in self.y_iterator()]
        n_channels = len(lengths)
        n_additions = n_channels - len(self._traces["data"])

        # Create New TraceContainer
        default_trace = go.Scattergl()
        self.add_traces((default_trace,) * n_additions, group="data")

        # Generate Labels
        labels = self.generate_labels(n_labels=n_channels)

        # Generate X Data
        self._update_data(lengths=lengths, labels=labels)

    def update_plot(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )
        # Data Info
        lengths = [len(y_c) for y_c in self.y_iterator([1])]
        n_channels = len(lengths)
        n_additions = n_channels - len(self._traces["data"])

        # Create New TraceContainer
        default_trace = go.Scattergl()
        self.add_traces((default_trace,) * n_additions, group="data")

        # Generate Labels
        labels = self.generate_labels(n_labels=n_channels)

        # Generate X Data
        self._update_data(lengths=lengths, labels=labels)

        # Apply Labels and Range
        y_axis = dict()

        if self.yaxis.range is None:
            y_axis["range"] = [-1 * self._trace_offset, n_channels * self._trace_offset]

        if self._label_axis:
            y_axis["tickvals"] = np.arange(n_channels) * self._trace_offset
            y_axis["ticktext"] = self.generate_tick_labels(labels=labels)

        self.update_yaxis(y_axis)

        # Apply Range and Slider
        x_axis = dict()
        x_min = min([x_c.min() for x_c in self.x_iterator(lengths=lengths)])
        x_max = max([x_c.max() for x_c in self.x_iterator(lengths=lengths)])
        x_range = [x_min, x_max]

        if self.xaxis.range is None:
            x_axis["range"] = x_range

        if self.xaxis.rangeslider.visible:
            x_axis["rangeslider"] = dict(range=x_range)

        self.update_xaxis(x_axis)
