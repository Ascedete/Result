from .type_defines import *
from typing import Callable


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
