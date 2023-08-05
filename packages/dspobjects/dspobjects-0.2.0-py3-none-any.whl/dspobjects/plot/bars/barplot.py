""" barplot.py

"""
# Package Header #
import itertools

from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Iterable, Iterator, Mapping, Sized
from typing import Any

# Third-Party Packages #
import numpy as np
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go

# Local Packages #
from ...operations import iteraxis
from ..bases import Figure, Subplot, BasePlot


# Definitions #
# Classes #
class BarPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str = "v",
        separated: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._separated_categories: bool = False
        self._orientation: str = "v"
        self._names: Iterable[str] | None = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                labels=labels,
                names=names,
                orientation=orientation,
                separated=separated,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
                build=build,
                **kwargs,
            )

    @property
    def separated_categories(self) -> bool:
        return self._separated_categories

    @property
    def orientation(self) -> str:
        return self._orientation

    @property
    def names(self) -> Iterable[str]:
        return self._names

    # Instance Methods #
    # Constructors/Destructors
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        **kwargs: Any,
    ) -> None:
        if names is not None:
            self._names = names

        if orientation is not None:
            if orientation in {"v", "h"}:
                self._orientation = orientation
            else:
                raise ValueError(f"{orientation} is not a valid orientation. [v, h]")

        if separated is not None:
            self._separated_categories = separated

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
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        **kwargs: Any,
    ) -> None:
        super().build(
            x=x,
            y=y,
            labels=labels,
            names=names,
            orientation=orientation,
            separated=separated,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

        if self._orientation == "v" and self.y is not None or self._orientation == "h" and self.x is not None:
            # Apply Data
            self.update_plot()

    # TraceContainer
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.update(base=dict(color=color))

    def x_iterator(self, lengths: Iterable[int] | None = None) -> Iterator:
        if self.x is None:
            return (np.arange(length) * self._trace_offset for length in lengths)
        elif isinstance(self.x, np.ndarray):
            return iteraxis(self.x, self._c_axis)
        elif isinstance(self.x, Sized) and len(self.x) == 1:
            return itertools.repeat(self.x[0], len(lengths))
        else:
            return iter(self.x)

    def generate_x(self, lengths: Iterable[int] | None = None) -> Iterable:
        if self.x is None:
            return [np.arange(length) * self._trace_offset for length in lengths]
        elif isinstance(self.x, np.ndarray):
            return self.x
        elif isinstance(self.x, Sized) and len(self.x) == 1:
            return self.x * len(lengths)
        else:
            return self.x

    def y_iterator(self, lengths: Iterable[int] | None = None) -> Iterator:
        if self.y is None:
            return (np.arange(length) * self._trace_offset for length in lengths)
        elif isinstance(self.y, np.ndarray):
            return iteraxis(self.y, self._c_axis)
        elif isinstance(self.y, Sized) and len(self.y) == 1:
            return itertools.repeat(self.y[0], len(lengths))
        else:
            return iter(self.y)

    def generate_y(self, lengths: Iterable[int] | None = None) -> Iterable:
        if self.y is None:
            return [np.arange(length) * self._trace_offset for length in lengths]
        elif isinstance(self.y, np.ndarray):
            return self.y
        elif isinstance(self.y, Sized) and len(self.y) == 1:
            return self.y * len(lengths)
        else:
            return self.y

    def apply_single_bar_traces(self, data_iter, locations_iter, lengths, b_axis, l_axis, names):
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_group = self._figure.get_legendgroups()
        else:
            existing_group = {}

        n_traces = len(lengths)
        n_additions = n_traces - len(self._traces["data"])

        default_trace = go.Bar()
        self.add_traces((default_trace,) * n_additions, group="data")

        text_iter = self.text_iterator(lengths=lengths)
        trace_iter = iter(self._traces["data"])
        trace_data = zip(text_iter, data_iter, locations_iter, trace_iter)
        for i, (text, bars, locations, trace) in enumerate(trace_data):
            data = {l_axis: locations, b_axis: bars}
            trace.update(data)
            trace.name = names[i]
            if self._group_existing_legend:
                trace.legendgroup = names[i]
            if names[i] in existing_group:
                trace.showlegend = False
            trace.text = text
            trace.orientation = self._orientation
            trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def apply_separate_bar_traces(self, data_iter, locations_iter, lengths, b_axis, l_axis, names):
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_group = self._figure.get_legendgroups()
        else:
            existing_group = {}

        n_traces = sum(lengths)
        n_additions = n_traces - len(self._traces["data"])

        default_trace = go.Bar()
        self.add_traces((default_trace,) * n_additions, group="data")

        text_iter = self.text_iterator(lengths=lengths)
        trace_iter = iter(self._traces["data"])
        for g, (text_c, bars, locations) in enumerate(zip(text_iter, data_iter, locations_iter)):
            if text_c is None:
                text_c = itertools.repeat(None, len(bars))
            for i, (text, bar, location, trace) in enumerate(zip(text_c, bars, locations, trace_iter)):
                updates = {l_axis: [location], b_axis: [bar]}
                trace.update(updates)
                trace.name = names[i]
                trace.legendgroup = trace.name
                if g > 0 or names[i] in existing_group:
                    trace.showlegend = False
                trace.text = text
                trace.orientation = self._orientation
                trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def update_plot(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        **kwargs: Any,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            names=names,
            orientation=orientation,
            separated=separated,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

        # Prepare Data to go in the correct orientation
        if self._orientation == "v":
            data_iter = self.y_iterator([1])
            n_bars = [len(d_c) for d_c in self.y_iterator([1])]
            n_sets = len(n_bars)
            locations_iter = self.x_iterator(n_bars)
            locations = next(itertools.islice(self.x_iterator(n_bars), np.argmax(n_bars), None))
            l_axis = "x"
            b_axis = "y"
        elif self._orientation == "h":
            data_iter = self.x_iterator([1])
            n_bars = [len(d_c) for d_c in self.x_iterator([1])]
            n_sets = len(n_bars)
            locations_iter = self.y_iterator(n_bars)
            locations = next(itertools.islice(self.y_iterator(n_bars), np.argmax(n_bars), None))
            l_axis = "y"
            b_axis = "x"
        else:
            raise ValueError(f"{self._orientation} is not a valid orientation. [v, h]")

        # Generate Labels
        labels = self.generate_labels(n_labels=max(n_bars))

        names = self.generate_names(n_names=n_sets)
        tick_labels = self.generate_tick_labels(labels=labels)

        # Apply Data to TraceContainer
        if self._separated_categories:
            self.apply_separate_bar_traces(data_iter, locations_iter, n_bars, b_axis, l_axis, labels)
        else:
            self.apply_single_bar_traces(data_iter, locations_iter, n_bars, b_axis, l_axis, names)

        # Apply Labels and Range
        tick_info = dict(
            range=[-1 * self._trace_offset, max(n_bars) * self._trace_offset],
            tickvals=locations,
            ticktext=tick_labels,
        )

        if self._orientation == "v":
            self.update_xaxis(tick_info)
        else:
            self.update_yaxis(tick_info)
