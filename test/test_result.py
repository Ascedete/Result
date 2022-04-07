from __future__ import unicode_literals
from functools import partial, reduce
from typing import Any, Callable
from result.result import Success, Error
from result import result


def test_success():
    assert Success("")


def test_error():
    assert not Error("")


def test_map():
    """
    Test if map correctly defined for Result Type
    """
    f2 = lambda x: (x, x)
    f3 = lambda x: x[0] + x[1]

    def chain(functions: "list[Callable[[Any], Any]]"):
        def inner(f1, f2):
            m1 = partial(result.map, f1)
            m2 = partial(result.map, f2)
            return lambda x: m2(m1(x))

        return reduce(inner, functions)

    m = chain([f2, f3])
    assert m(result.unit(1)) == Success(2)
    assert m(Error("0")) == Error("0")
