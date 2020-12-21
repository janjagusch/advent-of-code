"""
Tests the io.py module.
"""

import pytest
from day_20.array import Matrix
from day_20.io import process_raw_tile
from day_20.tile import Tile


@pytest.fixture(name="raw_tile")
def raw_tile_():
    return "Tile 2311:\n..#\n##."


@pytest.fixture(name="target")
def target_():
    return Tile(id=2311, data=Matrix(((False, False, True), (True, True, False))))


def test_process_raw_tile(raw_tile, target):
    assert process_raw_tile(raw_tile) == target
