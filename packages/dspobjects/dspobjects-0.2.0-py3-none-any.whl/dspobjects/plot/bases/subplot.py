""" _subplot.py

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
from typing import Any

# Third-Party Packages #
from baseobjects import BaseObject
import plotly.graph_objects as go

# Local Packages #


# Definitions #
# Classes #
class Subplot(BaseObject):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        row: int | None = None,
        col: int | None = None,
        title: go.layout.Annotation | None = None,
        init: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, int=init, **kwargs)

        # New Attributes #
        self.figure: go.Figure | None = None
        self.row: int = 1
        self.col: int = 1

        self.title: go.layout.Annotation | None = None
        self.xaxis: go.layout.XAxis | None = None
        self.yaxis: go.layout.YAxis | None = None

        # Object Construction #
        if init:
            self.construct(figure=figure, row=row, col=col, title=title)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure: go.Figure | None = None,
        row: int | None = None,
        col: int | None = None,
        title: go.layout.Annotation | None = None,
    ) -> None:
        if row is not None:
            self.row = row

        if col is not None:
            self.col = col

        if figure is not None:
            self.figure = figure

        if title is not None:
            self.title = title

        if self.figure is not None and (figure is not None or row is not None or col is not None):
            self.xaxis, self.yaxis = self.figure.get_subplot(self.row, self.col)

    def update_title(self, dict1=None, overwrite=False, **kwargs) -> None:
        self.title.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_xaxis(self, dict1=None, overwrite=False, **kwargs) -> None:
        self.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_yaxis(self, dict1=None, overwrite=False, **kwargs) -> None:
        self.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def add_trace(self, trace, secondary_y=None, exclude_empty_subplots=False, traces=None):
        if traces is not None:
            return traces.append_trace(
                trace,
                row=self.row,
                col=self.col,
                secondary_y=secondary_y,
                exclude_empty_subplots=exclude_empty_subplots,
            )
        else:
            self.figure.add_trace(
                trace,
                row=self.row,
                col=self.col,
                secondary_y=secondary_y,
                exclude_empty_subplots=exclude_empty_subplots,
            )
            return self.figure.data[-1]
