"""
This module contains a tile class.
"""

from .utils import Directions

N_DIM = 10
FLIP_NUMBERS = {i: int(format(i, f"0{N_DIM}b")[::-1], 2) for i in range(2 ** N_DIM)}


def _bools_to_int(bools):
    return int("".join("1" if val else "0" for val in bools), 2)


def _gen_borders(tile_data):
    for direction, bools in zip(
        (Directions.up, Directions.down, Directions.left, Directions.right),
        (tile_data[0, :], tile_data[-1, :], tile_data[:, 0], tile_data[:, -1]),
    ):
        yield direction, _bools_to_int(bools)


class Tile:
    def __init__(self, id, data):
        self._id = id
        self._data = data
        self._borders = dict(_gen_borders(data))

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id}, borders={self._borders})"

    def flip(self, axis):
        # if you flip horizontally,
        # up and down turn into their flip numbers and
        # left and right switch places.
        # if you flip vertically,
        # left and right turn into their flip numbers and
        # up and down switch places.
        assert axis in (0, 1)
        if axis == 0:
            borders = {
                Directions.up: FLIP_NUMBERS[self._borders[Directions.up]],
                Directions.down: FLIP_NUMBERS[self._borders[Directions.down]],
                Directions.left: self._borders[Directions.right],
                Directions.right: self._borders[Directions.left],
            }
        else:
            borders = {
                Directions.up: self._borders[Directions.down],
                Directions.down: self._borders[Directions.up],
                Directions.left: FLIP_NUMBERS[self._borders[Directions.left]],
                Directions.right: FLIP_NUMBERS[self._borders[Directions.right]],
            }
        return self.__class__(self._id, borders)

    def _rot90(self):
        """
        When you rotate by 90 degrees,
            * up becomes right,
            * right becomes down,
            * down becomes left,
            * left becomes up.
        """
        borders = {
            Directions.up: self._borders[Directions.left],
            Directions.right: self._borders[Directions.up],
            Directions.down: self._borders[Directions.right],
            Directions.left: self._borders[Directions.down],
        }
        return self.__class__(self._id, borders)

    @property
    def flip_borders(self):
        return tuple(FLIP_NUMBERS[border] for border in self.borders)

    @property
    def borders(self):
        return tuple(self._borders.values())

    def rot90(self, k=1):
        """
        Rotates the tile 90 degress clockwise k times.
        """
        k = k % 4
        if k == 0:
            return deepcopy(self)
        tile = self._rot90()
        for _ in range(1, k):
            tile = tile._rot90()
        return tile

    def matches_border(self, other):
        return any(
            border in other.borders + other.flip_borders for border in self.borders
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._id == other._id
            and (self._data == other._data).all()
            and self._borders == other._borders
        )
