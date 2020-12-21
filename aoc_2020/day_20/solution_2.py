from collections import namedtuple
from copy import deepcopy
from enum import Enum
from math import prod
from typing import Set

from aoc_2020.day_20.solution import matching_border

N_DIM = 10
FLIP_NUMBERS = {i: int(format(i, f"0{N_DIM}b")[::-1], 2) for i in range(2 ** N_DIM)}


def bools_to_int(bools):
    return int("".join("1" if val else "0" for val in bools), 2)


class Array:
    """
    A simple array that you can add and multiply with other arrays and scalars.
    """

    def __init__(self, *args):
        self._vals = tuple(args)

    def __len__(self):
        return len(self._vals)

    def __getitem__(self, index):
        return self._vals[index]

    def __iter__(self):
        return iter(self._vals)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other)
            return self.__class__(*[val_1 + val_2 for val_1, val_2 in zip(self, other)])
        if isinstance(other, int):
            return self.__class__(*[val + other for val in self])
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other)
            return self.__class__(*[val_1 * val_2 for val_1, val_2 in zip(self, other)])
        if isinstance(other, int):
            return self.__class__(*[val * other for val in self])
        return NotImplemented

    def __repr__(self):
        return f"{self.__class__.__name__}{self._vals}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._vals == other._vals
        raise NotImplemented

    def __hash__(self) -> int:
        return self._vals.__hash__()


class Matrix:
    """
    A 2-dimensional matrix.
    """

    def __init__(self, values):
        self._values = tuple(tuple(val for val in row) for row in values)
        self._shape = len(values[0]), len(values)

    def __getitem__(self, index):
        y, x = index
        item = self._values[y]
        if not isinstance(y, slice):
            return item[x]
        return tuple(tuple(i[x] for i in item))

    def __iter__(self):
        for row in self._values:
            yield row

    @property
    def rows(self):
        return iter(self)

    @property
    def cols(self):
        for i in range(self._shape[1]):
            yield self[:, i]

    def __len__(self):
        return self._shape[0]

    def _rot(self):
        """
        Rotates matrix clockwise by 90 degrees.
        """
        values = tuple(col[::-1] for col in self.cols)
        return self.__class__(values)

    def rot(self, k=1):
        """
        Rotates matrix clockwise by 90 degrees k times.
        """
        k = k % 4
        if not k:
            return deepcopy(self)
        matrix = self._rot()
        for _ in range(1, k):
            matrix = matrix._rot()
        return matrix

    def __repr__(self):
        return f"{self.__class__.__name__}(values={self._values})"


class Directions(Enum):
    up = Array(0, 1)
    down = Array(0, -1)
    left = Array(-1, 0)
    right = Array(1, 0)


class Tile:
    def __init__(self, id_, borders):
        self._id = id_
        self._borders = deepcopy(borders)

    @classmethod
    def from_input(cls, input_):
        id_ = int(input_.split("\n")[0].replace("Tile ", "").replace(":", ""))
        m = Matrix(
            tuple(
                tuple(val == "#" for val in row)
                for row in input_.split("\n")[1:]
                if row
            )
        )
        borders = {}
        for direction, bools in zip(
            (Directions.up, Directions.down, Directions.left, Directions.right),
            (m[0, :], m[-1, :], m[:, 0], m[:, -1]),
        ):
            borders[direction] = bools_to_int(bools)
        return cls(id_, borders)

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


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(
            Tile.from_input(image) for image in file_pointer.read().split("\n\n")
        )


def solve_part_one(tiles):
    matching_border_map = {
        tile1._id: set(
            tile2._id
            for tile2 in tiles
            if tile1.matches_border(tile2) and tile1 != tile2
        )
        for tile1 in tiles
    }
    border_ids = set(key for key, val in matching_border_map.items() if len(val) == 2)
    assert len(border_ids) == 4
    solution = prod(border_ids)
    return None, solution


def gen_neighbors(position, image):
    for direction in Directions:
        new_position = position + direction.value
        if new_position in image:
            yield direction, new_position, image[new_position]


class NoSolutionError(Exception):
    pass


def find_most_constrained_position(image, tiles: Set, matching_borders):
    position_constrains = {}
    for position, tile in image.items():
        possible_tiles = set(tiles)
        if tile is None:
            for _, _, neighbor in gen_neighbors(position, image):
                if not possible_tiles:
                    raise NoSolutionError(image, tiles, position)
                if neighbor is not None:
                    possible_tiles = possible_tiles.intersection(
                        matching_borders[neighbor.id]
                    )
        position_constrains[position] = possible_tiles
    return min(position_constrains, key=lambda key: len(position_constrains[key]))


def gen_images(image, tile_ids, border_tile_ids):

    pass


if __name__ == "__main__":
    tiles = read_input()
    image, solution_1 = solve_part_one(tiles)
    assert solution_1 == 2699020245973
    print(f"The solution to part 1 is '{solution_1}'.")
