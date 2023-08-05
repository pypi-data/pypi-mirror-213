""" numbackenddispatch.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #
from collections.abc import Callable
import pathlib
from types import ModuleType
from typing import Any

# Third-Party Packages #
from baseobjects import BaseDecorator
from baseobjects.dataclasses import Parameters
from baseobjects.typing import AnyCallable
import numpy as np

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import warnings

try:
    import cupy as cp
    import cupyx

    cp_array_types = (
        cp.ndarray,
        cupyx.scipy.sparse.spmatrix,
        cp._core.fusion._FusionVarArray,
        cp._core.new_fusion._ArrayProxy,
    )
except ModuleNotFoundError:
    warnings.warn("cupy module not found, num backend will remain default (numpy).")
    cp = None
    cupyx = None
    cp_array_types = ()

# Local Packages #


# Definitions #
# Classes #
class NumBackendDispatch(BaseDecorator):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    config_path = pathlib.Path.cwd().joinpath("num_backend_dispatch.toml")
    class_backend: ModuleType = np

    # Class Methods #
    @classmethod
    def load_config(cls) -> None:
        if cls.config_path.exists():
            with cls.config_path.open(mode="rb") as file:
                config_dict = tomllib.load(file)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        kwarg: AnyCallable | str = "xp",
        dispatch_method: Callable[..., ModuleType] | str | None = None,
        call_method: AnyCallable | str | None = None,
        func: AnyCallable | None = None,
        init: bool | None = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # Override Attributes #
        self._default_call_method: AnyCallable = self.dispatch_cast_call

        # New Attributes #
        self.default_backend: ModuleType = np
        self.instance_backend: ModuleType = np

        self.kwarg_name: str = "xp"

        self._default_dispatch_method: Callable[..., ModuleType] = self.no_dispatch
        self._dispatch_method: Callable[..., ModuleType] = self.no_dispatch

        # Object Construction #
        if init:
            if isinstance(kwarg, str):
                self.construct(kwarg=kwarg, dispatch_method=dispatch_method, call_method=call_method, func=func)
            else:
                self.construct(func=kwarg)

    @property
    def dispatch_method(self) -> AnyCallable:
        """The method that will be used for dispatch.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._dispatch_method

    @dispatch_method.setter
    def dispatch_method(self, value: AnyCallable | str) -> None:
        self.set_dispatch_method(value)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        kwarg: str | None = None,
        dispatch_method: Callable[..., ModuleType] | str | None = None,
        call_method: AnyCallable | str | None = None,
        func: AnyCallable | None = None,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            kwarg: The name of kwarg to assign the num backend module to.
            dispatch_method: The dispatch method to use.
            call_method: The default call method to use.
            func: The function to wrap.
            **kwargs: The other keyword arguments to construct a BaseMethod.
        """
        if kwarg is not None:
            self.kwarg_name = kwarg

        if dispatch_method is not None:
            self.set_dispatch_method(dispatch_method)

        if call_method is not None:
            self.set_default_call_method(call_method)  # The call method should be set to the default.

        super().construct(func=func, **kwargs)

    # Object Calling
    def dispatch_only_call(self, *args: Any, **kwargs: Any) -> Any:
        """Dispatches the correct num backend and evaluates the function/method.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        # Dispatch the backend if not given
        if self.kwarg_name not in kwargs:
            xp = self._dispatch_method(*args, **kwargs)
            kwargs[self.kwarg_name] = xp

        # Evaluate Function with backend
        return self.__func__(*args, **kwargs)

    def dispatch_cast_call(self, *args: Any, **kwargs: Any) -> Any:
        """Dispatches the correct num backend, casts the input, and evaluates the function/method.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        # Dispatch the backend if not given
        if self.kwarg_name not in kwargs:
            xp = self._dispatch_method(*args, **kwargs)
            kwargs[self.kwarg_name] = xp

        # Cast the inputs to the correct types
        if xp is np:
            args, kwargs = self.cast_input_to_np(*args, **kwargs)
        else:
            args, kwargs = self.cast_input_to_cp(*args, **kwargs)

        # Evaluate Function with backend
        return self.__func__(*args, **kwargs)

    # Casting
    def cast_input_to_np(self, *args: Any, **kwargs: Any) -> Parameters:
        """Casts the inputs into the correct numpy object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The args and kwargs casted to the correct types.
        """
        new_args = list(args)
        for arg, value in enumerate(new_args):
            if isinstance(value, cp_array_types):
                new_args[arg] = cp.asnumpy(value)

        new_kwargs = kwargs.copy()
        for name, value in kwargs.items():
            if isinstance(value, cp_array_types):
                new_kwargs[name] = cp.asnumpy(value)

        return Parameters(new_args, new_kwargs)

    def cast_input_to_cp(self, *args: Any, **kwargs: Any) -> Parameters:
        """Casts the inputs into the correct cupy object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The args and kwargs casted to the correct types.
        """
        new_args = list(args)
        for arg, value in enumerate(new_args):
            if isinstance(value, np.ndarray):
                new_args[arg] = cp.asarray(value)

        new_kwargs = kwargs.copy()
        for name, value in kwargs.items():
            if isinstance(value, np.ndarray):
                new_kwargs[name] = cp.asarray(value)

        return Parameters(new_args, new_kwargs)

    # Num Backend Dispatching
    def set_dispatch_method(self, method: AnyCallable | str) -> None:
        """Sets the dispatch method to another function or a method within this object can be given to select it.

        Args:
            method: The function or name to set the dispatch method to.
        """
        if callable(method):
            self._dispatch_method = method
        elif cp or cupyx is None:
            self._dispatch_method = self.no_dispatch
        elif isinstance(method, str):
            self._dispatch_method = getattr(self, method)
        else:
            raise TypeError(f"A {type(method)} cannot be used to set a dispatch method.")

    def no_dispatch(self, *args: Any, **kwargs: Any) -> ModuleType:
        """This dispatch passes a default backend.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The num backend to use.
        """
        return kwargs.get("xp", self.default_backend)

    def input_dispatch(self, *args: Any, **kwargs: Any) -> ModuleType:
        """This dispatch determines the backend based on the input.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The num backend to use.
        """
        # Check args for cupy object
        for arg in args:
            if isinstance(arg, cp_array_types):
                return cp

        # Check kwargs for cupy object
        for kwarg in kwargs.values():
            if isinstance(kwarg, cp_array_types):
                return cp

        # Return numpy if no cupy objects are found
        return np

    def class_backend_dispatch(self, *args: Any, **kwargs: Any) -> ModuleType:
        """This dispatch will return the backend set in the class attributes.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The num backend to use.
        """
        return self.class_backend

    def instance_backend_dispatch(self, *args: Any, **kwargs: Any) -> ModuleType:
        """This dispatch will return the backend set in the instance's attributes.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The num backend to use.
        """
        return self.instance_backend

    def config_file_dispatch(self):
        pass


if cp is None:
    NumBackendDispatch


# Functions #
def num_backend_dispatch(
    kwarg: AnyCallable | str = "xp",
    dispatch_method: AnyCallable | str | None = None,
    call_method: AnyCallable | str | None = None,
    func: AnyCallable | None = None,
) -> NumBackendDispatch:
    """A factory to be used as a decorator

    Args:


    Returns:
        The result or the caching_method.
    """
    return NumBackendDispatch(kwarg=kwarg, dispatch_method=dispatch_method, call_method=call_method, func=func)
