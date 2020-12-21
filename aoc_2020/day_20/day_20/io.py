"""
Contains functions for reading and writing.
"""

import numpy as np

from .array import Matrix
from .tile import Tile


def process_raw_tile(raw_tile):
    raw_tile = raw_tile.strip()
    tile_id = int(raw_tile.split("\n")[0].replace("Tile ", "").replace(":", ""))
    tile_data = np.array(
        tuple(
            tuple(val == "#" for val in row) for row in raw_tile.split("\n")[1:] if row
        )
    )
    return Tile(tile_id, tile_data)


def read_files(file_path):
    with open(file_path, mode="r") as file_pointer:
        return tuple(
            process_raw_tile(raw_tile) for raw_tile in file_pointer.read().split("\n\n")
        )
