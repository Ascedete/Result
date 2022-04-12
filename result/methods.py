from .type_defines import *
from typing import Any, Callable


def bind(f: "Callable[[ResO], Result[ResT, ErrT2]]", o: "Result[ResO, ErrT]"):
    """Bind for Result Type -> if item is of instance Success, apply f to it
    else return item directly without evaluating f
    """
    if isinstance(o, Success):
        return f(o)
    else:
        return o


def map(f: "Callable[[ResO], ResT]", o: "Result[ResO, ErrT]"):
    if isinstance(o, Success):
        return unit(f(o.val))
    else:
        return o


def unit(input: ResT) -> Success[ResT]:
    return Success(input)


def expect(input: Result[ResT, Any], err_msg: str = ""):
    if isinstance(input, Error):
        raise ValueError(err_msg) if err_msg else ValueError(f"Got Error {input.val}")
    else:
        return input.val
