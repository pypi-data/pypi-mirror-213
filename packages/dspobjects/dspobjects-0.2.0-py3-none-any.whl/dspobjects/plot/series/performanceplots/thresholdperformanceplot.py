""" thresholdperformanceplot.py

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
from collections.abc import Iterable, Iterator, Sized
from typing import Any
import itertools

# Third-Party Packages #
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go
import numpy as np

# Local Packages #
from ....operations import iteraxis
from ...bases import Figure, Subplot, BasePlot
from ..zeroonedomainplot import ZeroOneDomainPlot


# Definitions #
# Classes #
class ThresholdPerformancePlot(ZeroOneDomainPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_hovertemplate: str | None = "%{y:.4f} %{_y_unit}<br>" + "%{x:.4f} %{_x_unit}<br>" + "Threshold: %{text}"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        thresholds: np.ndarray | None = None,
        labels: Iterable[str] | None = None,
        axis: int = 0,
        c_axis: int = 1,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._thresholds: np.ndarray | None = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                thresholds=thresholds,
                labels=labels,
                axis=axis,
                c_axis=c_axis,
                build=build,
                **kwargs,
            )

    @property
    def thresholds(self) -> Iterable | None:
        return self._thresholds

    @thresholds.setter
    def thresholds(self, value) -> None:
        if isinstance(value, np.ndarray) and value.ndim == 1:
            value = [value]
        self._thresholds = value

    # Instance Methods #
    # Constructors/Destructors
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        thresholds: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        **kwargs: Any,
    ) -> None:
        super()._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            **kwargs,
        )

        if thresholds is not None:
            self.thresholds = thresholds

    def threshold_iterator(self, lengths: Iterable[int] | None = None) -> Iterator:
        return self._data_iterator(data=self.thresholds, lengths=lengths)

    def text_iterator(self, lengths: Iterable[int] | None = None) -> Iterator:
        if self._text is None:
            if self._thresholds is not None:
                return (tuple(f"{v:.4f}" for v in c) for c in self.threshold_iterator(lengths=lengths))
            elif self._z_score:
                return (tuple(f"{v:.4f}" for v in c) for c in self.y_iterator(lengths=lengths))
            else:
                return ([""] * length for length in lengths)
        elif isinstance(self._text, np.ndarray):
            return iteraxis(self._text, self._c_axis)
        elif isinstance(self._text, Sized) and len(self._text) == 1:
            return itertools.repeat(self._text[0], len(lengths))
        else:
            return iter(self._text)
