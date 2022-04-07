"""
Module defines Result Sum Type and allows to specify Success and Errors more clearly
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import partial, reduce
from typing import Any, Callable, Generic, Iterable, TypeVar, Union, overload

# from dataclasses import dataclass
ResT = TypeVar("ResT")
# Currently only strings supported

ResO = TypeVar("ResO")


def bind(
    f: "Callable[[ResO], Result[ResT]]", o: "Result[ResO]"
) -> Error | Success[ResT]:
    """Bind for Result Type -> if item is of instance Success, apply f to it
    else return item directly without evaluating f
    """
    if isinstance(o, Success):
        return f(o.val)
    else:
        return o


def map(f: "Callable[[ResO], ResT]", o: "Result[ResO]") -> Error | Success[ResT]:
    if isinstance(o, Success):
        return Success(f(o.val))
    else:
        return o


def unit(input: ResT) -> Success[ResT]:
    return Success(input)


def do(fs: "Iterable[Callable[[Any], Result[Any]]]", input: "ResO"):
    init = unit(input)
    binded_functions = [partial(bind, f) for f in fs]

    def f(start: Result[Any]):
        init = start
        for _f in binded_functions:
            init: Result[Any] = _f(init)
        return init

    return f(init)


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


@dataclass(frozen=True, eq=True)
class Error:
    """Signify erronous operation of function.
    val -> Error Message to be returned from function
    """

    __slots__ = "val"
    val: str

    def __bool__(self):
        return False

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Error):
            return False
        else:
            return o.val == self.val

    @overload
    @classmethod
    def error(cls, msg: None) -> "Error":
        ...

    @overload
    @classmethod
    def error(cls, msg: str) -> "Error":
        ...

    @classmethod
    def error(cls, msg: Union[None, str]) -> "Error":
        if msg is None:
            return Error("")
        else:
            return Error(msg)


Result = Union[Success[ResT], Error]
ResFunction = Callable[[ResT], Result[ResO]]
