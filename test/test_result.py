from __future__ import unicode_literals
from functools import partial, reduce
from typing import Any, Callable

import pytest
from result.type_defines import Success, Error
from result.methods import expect, map, unit


def test_success():
    assert Success("")


def test_error():
    e1 = Error(0)
    assert not e1 and isinstance(e1.val, int)


def test_map():
    """
    Test if map correctly defined for Result Type
    """

    f2 = lambda x: (x, x)
    f3 = lambda x: x[0] + x[1]

    def chain(functions: "list[Callable[[Any], Any]]"):
        def inner(f1, f2):
            m1 = partial(map, f1)
            m2 = partial(map, f2)
            return lambda x: m2(m1(x))

        return reduce(inner, functions)

    m = chain([f2, f3])
    assert m(unit(1)) == Success(2)
    assert m(Error(0)) == Error(0)


def test_method_chaining():
    input = Success(10)
    res = (
        input.map(lambda x: x + x)
        .bind(lambda x: Success(x) if x == 0 else Error("Expected 0"))
        .map(lambda x: Success(x))
    )
    assert not res
    assert res.val == "Expected 0"

    with pytest.raises(ValueError):
        res.expect()

    assert Success(2).expect() == 2


def test_expect():
    def div(a: float, b: float):
        if b == 0:
            return Error(0)
        else:
            return Success(a / b)

    assert expect(div(2, 3)) == 2 / 3
    with pytest.raises(ValueError):
        expect(div(2, 0))
