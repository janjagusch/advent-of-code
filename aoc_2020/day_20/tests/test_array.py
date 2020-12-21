"""
Tests for the `array.py` module.
"""

import pytest
from day_20.array import Array, Matrix


@pytest.mark.parametrize(
    "first,second,target",
    ((Array(1, 1), Array(1, 1), Array(2, 2)), (Array(1, 1), 1, Array(2, 2))),
)
def test_array_add(first, second, target):
    assert first + second == target


@pytest.mark.parametrize(
    "first,second,target",
    ((Array(2, 2), Array(2, 2), Array(4, 4)), (Array(2, 2), 2, Array(4, 4))),
)
def test_array_mul(first, second, target):
    assert first * second == target


@pytest.fixture(name="matrix")
def matrix_():
    return Matrix(((1, 2), (3, 4)))


@pytest.mark.parametrize(
    "index,target", (((0, 0), 1), ((1, 1), 4), ((slice(1), 0), (1,)))
)
def test_matrix_index(matrix, index, target):
    assert matrix[index] == target
