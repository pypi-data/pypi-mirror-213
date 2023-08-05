""" tracecontainer.py

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
from collections import deque
from collections.abc import Iterable, Iterator
from typing import Any, Union, Optional

# Third-Party Packages #
from baseobjects import search_sentinel
from baseobjects.collections import GroupedList
from plotly.basedatatypes import BaseTraceType

# Local Packages #


# Definitions #
# Classes #
class TraceContainer(GroupedList):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure=None,
        items: Iterable[Any] | None = None,
        parent: GroupedList | None = None,
        parents: Iterable[GroupedList] | None = None,
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._figure = None

        # Object Construction #
        if init:
            self.construct(figure=figure, items=items, parent=parent, parents=parents)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure=None,
        items: Iterable[Any] | None = None,
        parent: GroupedList | None = None,
        parents: Iterable[GroupedList] | None = None,
    ) -> None:
        if figure is not None:
            self._figure = figure

        super().construct(items=items, parent=parent, parents=parents)

    def create_group(self, name: str, items: Iterable | None = None) -> "TraceContainer":
        if name not in self.groups:
            new_group = self.__class__(figure=self._figure, items=items, parent=self)
            self.groups[name] = new_group
            self.data.append(new_group)
            return new_group
        else:
            raise KeyError(f"{name} group already exists.")

    def require_group(self, name: str | Iterable[str]) -> "TraceContainer":
        if isinstance(name, str):
            names = [name]
        else:
            names = list(name)

        # Require name at this level
        first = names.pop()
        new_group = self.groups.get(first, search_sentinel)
        if new_group is search_sentinel:
            new_group = self.__class__(figure=self._figure, parent=self)
            self.groups[first] = new_group
            self.data.append(new_group)

        # Recurse if needed
        if names:
            new_group = new_group.require_group(names)

        return new_group

    def append_trace(
        self,
        trace,
        row: int | None = None,
        col: int | None = None,
        secondary_y: bool | None = None,
        exclude_empty_subplots: bool = False,
        group: str | None = None,
    ) -> BaseTraceType:
        self._figure.add_trace(
            trace=trace,
            row=row,
            col=col,
            secondary_y=secondary_y,
            exclude_empty_subplots=exclude_empty_subplots,
        )

        new_trace = self._figure.data[-1]
        self.append(new_trace, group=group)

        return new_trace

    def append_traces(
        self,
        data,
        row: int | None = None,
        col: int | None = None,
        secondary_y: bool | None = None,
        exclude_empty_subplots: bool = False,
        group: str | None = None,
    ) -> tuple[BaseTraceType]:
        self._figure.add_traces(
            data=data,
            row=row,
            col=col,
            secondary_y=secondary_y,
            exclude_empty_subplots=exclude_empty_subplots,
        )

        new_traces = self._figure.data[-len(data)]
        self.extend(new_traces, group=group)

        return new_traces
