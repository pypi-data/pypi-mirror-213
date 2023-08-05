""" _figure.py

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

# Third-Party Packages #
import plotly.graph_objects as go

# Local Packages #
from .subplot import Subplot
from .tracecontainer import TraceContainer


# Definitions #
# Classes #
class Figure(go.Figure):
    """An extension of the plotly Figure, which gives it more flexibilty with its trace objects.

    Attributes:
        _traces: The traces of this figure.
        _subplots: The subplots of this figure.

    Args:
        data: The traces to add to this figure.
        layout: The layout of this figure.
        frames: The frames of this figure
        skip_invalid: Determines if invalid property assigments will be skipped.
        figure: A plotly figure to convert to a this new object.
        **kwargs: Other keyword arguments used to construct a plotly figure.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, data=None, layout=None, frames=None, skip_invalid=False, figure=None, **kwargs) -> None:
        # New Attributes #
        self._traces: TraceContainer = TraceContainer(figure=self)
        self._subplots: list[Subplot] = []

        # Object Construction #
        self.construct(data=data, layout=layout, frames=frames, skip_invalid=skip_invalid, figure=figure, **kwargs)

    @property
    def traces(self) -> TraceContainer:
        """The traces of this figure."""
        return self._traces

    @property
    def subplots(self) -> list[Subplot]:
        """The sublots of this figure."""
        return self._subplots

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, data=None, layout=None, frames=None, skip_invalid=False, figure=None, **kwargs) -> None:
        """Construct this object.

        Args:
            data: The traces to add to this figure.
            layout: The layout of this figure.
            frames: The frames of this figure
            skip_invalid: Determines if invalid property assigments will be skipped.
            figure: A plotly figure to convert to a this new object.
            **kwargs: Other keyword arguments used to construct a plotly figure.
        """
        data = figure or data  # Override the data to _figure if given.
        super().__init__(data=data, layout=layout, frames=frames, skip_invalid=skip_invalid, **kwargs)

    def set_subplots(self, rows: int = None, cols: int = None, **make_subplots_args) -> "Figure":
        """Creates subplots within this figure.

        Args:
            rows: The number of rows of subplots this figure will have.
            cols: The number of columns of subplots this figure will have.
            **make_subplots_args: The other keyword arguments to create subplots.

        Returns:
            This object.
        """
        # Ensure there are titles for annotations
        if "subplot_titles" not in make_subplots_args:
            make_subplots_args["subplot_titles"] = [f" " for i in range(rows * cols)]

        super().set_subplots(rows=rows, cols=cols, **make_subplots_args)

        self._subplots.clear()
        self._subplots.extend([None] * cols for r in range(rows))
        for row in range(rows):
            for col in range(cols):
                title = self.layout.annotations[(row * cols) + col]
                self._subplots[row][col] = Subplot(figure=self, row=row + 1, col=col + 1, title=title)

        return self

    def create_trace_group(self, name: str) -> TraceContainer:
        """Creates a new trace group in the trace continer.

        Args:
            name: The name of the new trace group.

        Returns:
            The new trace group.
        """
        return self.traces.create_group(name=name)

    def require_trace_group(self, name: str) -> TraceContainer:
        """Either gets a group from the trace container or creates the group if it is not present.

        Args:
            name: The name of the group to either get or create.

        Returns:
            The new trace group.
        """
        return self.traces.require_group(name=name)

    def get_legendgroups(self) -> set[str]:
        """Gets the names of the legend groups for the traces within this figure.

        Returns:
            The names of the the legend groups.
        """
        return set(trace.legendgroup for trace in self.data if trace.legendgroup is not None)

    def to_dict(self) -> dict:
        """Creates a dictionary representation of this figure.

        Returns:
            The dictionary representation if this figure.
        """
        self.data = self._traces.as_flat_tuple()
        return super().to_dict()

    def to_ordered_dict(self, skip_uid: bool = True) -> dict:
        """Creates an ordered dictionary representation of this figure.

        Args:
            skip_uid: Determines if the uid will be skipped durring dictionary creation.

        Returns:
            The ordered dictionary representation of this figure.
        """
        self.data = self._traces.as_flat_tuple()
        return super().to_ordered_dict(skip_uid=skip_uid)

    def to_image(self, *args, rangeslider_visible=False, **kwargs):
        """Creates a static image bytes string representation of this figure.

        Args:
            *args: The argments used to create the byte string.
            rangeslider_visible: Determines if the range sliders will be visable.
            **kwargs: The keyword argments used to create the byte string.

        Returns
            The static image bytes string representation of this figure.
        """
        self.data = self._traces.as_flat_tuple()

        if not rangeslider_visible:
            self.update_xaxes(dict(rangeslider={"visible": False}))

        return super().to_image(*args, *kwargs)
