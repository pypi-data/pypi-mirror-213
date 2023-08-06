#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from contextvars import ContextVar
from dataclasses import dataclass, field
import functools
from typing import Callable, Optional, TYPE_CHECKING, TypeVar, Union

from trafaret import DataError
from typing_extensions import ParamSpec

from .errors import ClientError

if TYPE_CHECKING:
    from .models.use_cases.use_case import UseCase

DefaultUseCase = Optional[Union["UseCase", str]]

P = ParamSpec("P")
T = TypeVar("T")


def _init_context(func: Callable[P, T]) -> Callable[P, T]:
    """
    Ensures that context has been initialized before executing the decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # ensure that context has been initialized (this is done as a side effect of creating the client)
        from .client import get_client  # pylint: disable=import-outside-toplevel, cyclic-import

        get_client()
        return func(*args, **kwargs)

    return wrapper


@dataclass
class _ContextGlobals:
    """
    Interface for initializing, accessing, and setting variables that should persist.

    This class should not be used directly; rather, reference `datarobot.context.Context`.

    Examples
    --------
        .. code-block:: python

            from datarobot.context import Context

            >>> def foobar(value: str) -> None:
            ...  print(f"hey {value}")
            ...  Context.use_case = value
            ...
            >>> foobar("Jude")
            hey Jude
            >>>
    """

    _use_case: DefaultUseCase = field(init=False, default=None)

    @property
    def use_case(self) -> DefaultUseCase:
        """Returns the default Use Case. If a string representing the Use Case ID
        was provided, lookup, cache, and return the actual entity."""
        return self.get_use_case()

    @use_case.setter
    def use_case(self, value: DefaultUseCase = None) -> None:
        self._use_case = value

    @_init_context
    def get_use_case(self, raw: bool = False) -> DefaultUseCase:
        """Returns the default Use Case. If a string representing the Use Case ID
        was provided and raw=False, lookup, cache, and return the actual entity.
        Otherwise, simply return the stored default Use Case in its current form"""
        if not raw:
            if isinstance(self._use_case, str):
                try:
                    from .models.use_cases.use_case import (  # pylint: disable=import-outside-toplevel
                        UseCase,
                    )

                    self._use_case = UseCase.get(use_case_id=self._use_case)
                except (DataError, ClientError) as e:
                    raise ValueError("Current use case is invalid.", e)
        return self._use_case or None


_context: ContextVar[_ContextGlobals] = ContextVar("current_context", default=_ContextGlobals())

Context = _context.get()
