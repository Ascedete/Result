"""
Module defines Result Sum Type and allows to specify Success and Errors more clearly
"""
from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    NamedTuple,
    Optional,
    TypeVar,
    Union,
    overload,
)

# from dataclasses import dataclass
ResT = TypeVar("ResT")
# Currently only strings supported


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


def unwrap(result: Result[ResT]) -> ResT:
    """In case Success is expected return ResT in Success else raise ValueError"""
    if not isinstance(result, Success):
        raise ValueError
    return result.val


ResO = TypeVar("ResO")
ResFunction = Callable[[ResO], Result[ResT]]


def bind(f: ResFunction[ResO, ResT], res: Result[ResO]):
    """Bind for Result Type -> if item is of instance Success, apply f to it
    else return item directly without evaluating f
    """
    if isinstance(res, Success):
        return f(res.val)
    else:
        return res


def map(f: Callable[[ResO], ResT], res: Result[ResO]) -> Result[ResT]:
    if isinstance(res, Success):
        return Success(f(res.val))
    else:
        return res


IOResult = Optional[Error]
