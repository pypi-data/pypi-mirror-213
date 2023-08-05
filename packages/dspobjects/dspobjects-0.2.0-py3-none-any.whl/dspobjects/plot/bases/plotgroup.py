""" plotgroup.py

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
from collections.abc import Iterable, Mapping
from typing import Any, Union

# Third-Party Packages #
from baseobjects import BaseDict, search_sentinel
from baseobjects.functions import singlekwargdispatch
from baseobjects.operations import union_recursive
import plotly.graph_objects as go

# Local Packages #
from .figure import Figure
from .subplot import Subplot
from .baseplot import BasePlot


# Definitions #
# Types #
PlotOrKey = Union[BasePlot, str, Iterable[str]]
XAssignments = Iterable[Iterable[PlotOrKey, PlotOrKey | go.layout.XAxis]]
YAssignments = Iterable[Iterable[PlotOrKey, PlotOrKey | go.layout.YAxis]]


# Classes #
class PlotGroup(BaseDict):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_layout_settings: dict[str, Any] = dict(
        title=dict(font=dict(size=30), y=1.0, x=0.5, xanchor="center", yanchor="top"),
        margin=dict(t=50, b=50),
    )
    default_subplot_settings: dict[str, Any] = {}
    default_plots: Mapping[str, Any] = {}
    default_plot_settings: dict[str, dict[str, Any]] = {}
    default_locations: dict[str, tuple[int, int]] = {}
    default_xaxes_assignment: XAssignments = ()
    default_yaxes_assignment: YAssignments = ()
    default_legend_group: Iterable[Iterable[PlotOrKey]] | str = "None"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        layout_settings: dict[str, Any] | None = None,
        subplot_settings: dict[str, Any] | None = None,
        plot_settings: dict[str, dict[str, Any]] | None = None,
        locations: dict[str, tuple[int, int]] | None = None,
        build: bool = False,
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__()

        # New Attributes #
        self._figure: go.Figure | None = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                layout_settings=layout_settings,
                subplot_settings=subplot_settings,
                plot_settings=plot_settings,
                locations=locations,
                build=build,
            )

    @property
    def figure(self) -> go.Figure | None:
        return self._figure

    @property
    def plots(self):
        return self.data

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure: go.Figure | None = None,
        layout_settings: dict[str, Any] | None = None,
        subplot_settings: dict[str, Any] | None = None,
        plot_settings: dict[str, dict[str, Any]] | None = None,
        locations: Mapping[str, Mapping[str, int]] | None = None,
        build: bool = False,
    ) -> None:
        if figure is not None:
            self._figure = figure
        elif self._figure is None:
            layout_settings = layout_settings if layout_settings is not None else {}
            subplot_settings = subplot_settings if subplot_settings is not None else {}
            self._figure = Figure()
            self._figure.update_layout(union_recursive(self.default_layout_settings, layout_settings))
            self._figure.set_subplots(**union_recursive(self.default_subplot_settings, subplot_settings))

        if locations is not None:
            locations = union_recursive(self.default_locations, locations)
        else:
            locations = self.default_locations

        if plot_settings is not None:
            plot_settings = union_recursive(self.default_plot_settings, plot_settings)
        else:
            plot_settings = self.default_plot_settings

        default_kwargs = dict(figure=self._figure, build=build)
        for name, plot in self.default_plots.items():
            kwargs = default_kwargs.copy()
            location = locations.get(name, search_sentinel)

            if isinstance(location, tuple):
                kwargs["subplot"] = self._figure.subplots[location[0]][location[1]]
            elif isinstance(location, Mapping):
                kwargs["locations"] = location

            kwargs.update(plot_settings.get(name, {}))

            self.data[name] = plot(**kwargs)

        self.assign_xaxes(axes=self.default_xaxes_assignment)
        self.assign_yaxes(axes=self.default_yaxes_assignment)

        if isinstance(self.default_legend_group, str):
            if self.default_legend_group.lower() == "all":
                self.group_all_same_lengend_items()
        else:
            self.group_same_lengend_items(plots=self.default_legend_group)

    def get_subplots(self) -> dict[str : Subplot | dict]:
        subplots = {}
        for name, plot in self.data.items():
            if isinstance(plot, BasePlot):
                subplots[name] = plot.subplot
            else:
                subplots[name] = plot.get_subplots()

        return subplots

    def set_subplots(self, dict_: dict[str, Any] | None = None, /, **kwargs: Any):
        if dict_ is None:
            subplots = kwargs
        else:
            subpolts = dict_ | kwargs

        for name, set_kwargs in subpolts.items():
            plot = self.data[name]
            if isinstance(plot, BasePlot):
                if isinstance(set_kwargs, Mapping):
                    plot.set_subplot(**set_kwargs)
                elif isinstance(set_kwargs, Iterable):
                    plot.set_subplot(*set_kwargs)
                else:
                    plot.set_subplot(set_kwargs)
            else:
                plot.set_subplots(**set_kwargs)

    def get_locations(self) -> dict[str, tuple[int] | dict]:
        loctions = {}
        for name, plot in self.data.items():
            if isinstance(plot, BasePlot):
                loctions[name] = (plot.subplot.row, plot.subplot.col)
            else:
                loctions[name] = plot.get_locations()

        return loctions

    def set_locations(self, dict_: dict[str, Any] | None = None, /, **kwargs: Any):
        self.set_subplots(dict_, **kwargs)

    def get_all_plots(self) -> tuple[BasePlot]:
        all_plots = []
        for plot in self.data.values():
            if isinstance(plot, BasePlot):
                all_plots.append(plot)
            else:
                all_plots.extend(plot.get_all_plots())

        return tuple(all_plots)

    @singlekwargdispatch("key")
    def get_plot(self, key: Iterable[str] | str) -> BasePlot:
        raise ValueError(f"{type(key)} is an invalid type for get_plot")

    @get_plot.register(Iterable)
    def _get_plot(self, key: Iterable[str]) -> BasePlot:
        plot = self
        for k in key:
            plot = plot[k]

        return plot

    @get_plot.register
    def _get_plot(self, key: str) -> BasePlot:
        return self[key]

    def assign_xaxes(self, axes: XAssignments) -> None:
        for target, other in axes:
            if not isinstance(target, BasePlot):
                target = self.get_plot(key=target)

            if isinstance(other, go.layout.XAxis):
                pass
            elif isinstance(other, (str | Iterable)):
                other = self.get_plot(key=other).xaxis
            elif isinstance(other, BasePlot):
                other = other.xaxis

            target.set_xaxis(other)

    def assign_yaxes(self, axes: YAssignments) -> None:
        for target, other in axes:
            if not isinstance(target, BasePlot):
                target = self.get_plot(key=target)

            if isinstance(other, go.layout.YAxis):
                pass
            elif isinstance(other, (str | Iterable)):
                other = self.get_plot(key=other).yaxis
            elif isinstance(other, BasePlot):
                other = other.yaxis

            target.set_yaxis(other)

    def group_same_lengend_items(self, plots: Iterable[Iterable[PlotOrKey]]) -> None:
        for target, *others in axes:
            if not isinstance(target, BasePlot):
                target = self.get_plot(key=target)

            other_plots = (self.get_plot(other) for other in others)
            target.group_same_legend_items(plots=other_plots)

    def group_all_same_lengend_items(self):
        all_plots = iter(self.get_all_plots())
        first_plot = next(all_plots)
        first_plot.group_same_legend_items(plots=all_plots)
