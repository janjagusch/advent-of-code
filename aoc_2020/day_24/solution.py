# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: aoc-2020-20
#     language: python
#     name: aoc-2020-20
# ---

# # Day 24

# # Part 1

from copy import copy


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


DIRECTIONS = {
    "e": Array(1, -1, 0),
    "se": Array(0, -1, 1),
    "sw": Array(-1, 0, 1),
    "w": Array(-1, 1, 0),
    "nw": Array(0, 1, -1),
    "ne": Array(1, 0, -1),
}


def process_directions(directions):
    """
    These directions are given in your list,
    respectively, as e, se, sw, w, nw, and ne.
    A tile is identified by a series of these directions
    with no delimiters;
    for example, esenee identifies the tile
    you land on if you start at the reference tile
    and then move one tile east, one tile southeast,
    one tile northeast, and one tile east.
    """
    if not directions:
        return
    if directions[0] in DIRECTIONS:
        yield directions[0]
        directions = directions[1:]
    else:
        yield directions[:2]
        directions = directions[2:]
    for direction in process_directions(directions):
        yield direction


assert tuple(process_directions("esenee")) == ("e", "se", "ne", "e")


def directions_to_coord(directions):
    coord = Array(0, 0, 0)
    for direction in directions:
        coord += DIRECTIONS[direction]
    return coord


directions = tuple(process_directions("nwwswee"))
assert directions_to_coord(directions) == Array(0, 0, 0)


def read_instructions(file_path):
    with open(file_path, mode="r") as file_pointer:
        return tuple(
            tuple(process_directions(directions))
            for directions in file_pointer.read().split("\n")
            if directions
        )


instructions = read_instructions("./input.txt")


# +
def apply_instructions(instructions):
    tiles = {}
    for directions in instructions:
        coord = directions_to_coord(directions)
        tiles[coord] = not tiles.get(coord, True)
    return tiles


def count_black(tiles):
    return sum(not is_white for is_white in tiles.values())


# -


def solve_part_one(instructions):
    tiles = apply_instructions(instructions)
    return tiles, count_black(tiles)


tiles, solution_1 = solve_part_one(instructions)
assert solution_1 == 339
print(f"The solution to part 1 is '{solution_1}'.")


# ## Part 2

# +
def gen_neigbor_positions(position):
    for direction in DIRECTIONS.values():
        yield position + direction


def gen_neighbors(position, tiles):
    for position in gen_neigbor_positions(position):
        yield tiles.get(position, True)


# -


def possibly_flip(is_white, neighbors):
    """
    Any black tile with zero or more than 2
    black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles
    immediately adjacent to it is flipped to black.
    """
    black_neighbors = sum(not is_white for is_white in neighbors)
    if not is_white:
        if black_neighbors == 0 or black_neighbors > 2:
            return True
    else:
        if black_neighbors == 2:
            return False
    return is_white


def play_round(tiles):
    tiles = copy(tiles)
    update_tiles = {}
    relevant_positions = set(tiles).union(
        relevant_position
        for position in tiles
        for relevant_position in gen_neigbor_positions(position)
    )
    for relevant_position in relevant_positions:
        is_white = tiles.get(relevant_position, True)
        neighbors = tuple(gen_neighbors(relevant_position, tiles))
        update_tiles[relevant_position] = possibly_flip(is_white, neighbors)
    tiles.update(update_tiles)
    return update_tiles


def solve_part_two(tiles):
    for i in range(100):
        tiles = play_round(tiles)
    return count_black(tiles)


solution_2 = solve_part_two(tiles)
assert solution_2 == 3794
print(f"The solution to part 2 is '{solution_2}'.")
