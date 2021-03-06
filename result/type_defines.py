"""
Module defines Result Sum Type and allows to specify Success and Errors more clearly
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union

# from dataclasses import dataclass
ResT = TypeVar("ResT")
ErrT = TypeVar("ErrT")
ErrT2 = TypeVar("ErrT2")
# Currently only strings supported

ResO = TypeVar("ResO")


@dataclass(frozen=True, eq=True)
class Success(Generic[ResT]):
    """Wrap a ResT Type in an Success object to signify successful function return

    Args:
        Generic (ResT): from function actually expected type
    """

    __slots__ = "val"
    val: ResT

    def __bool__(self):
        return True

    def map(self, f: Callable[[ResT], ResO]):
        return Success(f(self.val))

    def bind(self, f: Callable[[ResT], Result[ResO, Any]]):
        return f(self.val)

    def expect(self, msg: str = ""):
        return self.val


@dataclass(frozen=True, eq=True)
class Error(Generic[ErrT]):
    """Signify erronous operation of function.
    val -> Error Message to be returned from function
    """

    __slots__ = "val"
    val: ErrT

    def __bool__(self):
        return False

    def map(self, f: Callable[[ResT], ResO]):
        return self

    def bind(self, f: Callable[[ResT], Result[ResO, Any]]):
        return self

    def expect(self, msg: str = ""):
        raise ValueError(msg if msg else f"Error! {self.val}")


Result = Union[Success[ResT], Error[ErrT]]
