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

# # Day 20

# ## Part 1

import math
from enum import Enum
from itertools import islice, product

import numpy as np


# +
def process_raw_tile(raw_tile):
    tile_id = int(raw_tile.split("\n")[0].replace("Tile ", "").replace(":", ""))
    tile_data = np.array(
        tuple(
            tuple(1 if val == "#" else 0 for val in row)
            for row in raw_tile.split("\n")[1:]
            if row
        )
    )
    return tile_id, tile_data


with open("./input.txt", mode="r") as file_pointer:
    tiles = dict(
        process_raw_tile(raw_tile)
        for raw_tile in file_pointer.read().split("\n\n")
        if raw_tile
    )


# -


class Directions(Enum):
    up = (-1, 0)
    down = (1, 0)
    right = (0, 1)
    left = (0, -1)


# +
def tile_border(tile, direction):
    if direction in (Directions.up, Directions.up.value):
        border = (0, slice(None))
    elif direction in (Directions.down, Directions.down.value):
        border = (-1, slice(None))
    elif direction in (Directions.right, Directions.right.value):
        border = (slice(None), -1)
    elif direction in (Directions.left, Directions.left.value):
        border = (slice(None), 0)
    else:
        raise KeyError(direction)
    return tile[border]


def gen_borders(tile):
    for direction in Directions:
        yield tile_border(tile, direction)


def gen_all_borders(tile):
    """
    Yields all borders, including the flipped ones.
    """
    for border in gen_borders(tile):
        yield border
        yield border[::-1]


# -

tiles_borders = {key: tuple(gen_all_borders(tile)) for key, tile in tiles.items()}


def compatible_borders(borders_1, borders_2):
    return any(
        (border_1 == border_2).all() for border_2 in borders_2 for border_1 in borders_1
    )


compatible_tiles = {
    tile_id_1: set(
        tile_id_2
        for tile_id_2, borders_2 in tiles_borders.items()
        if tile_id_1 != tile_id_2 and compatible_borders(borders_1, borders_2)
    )
    for tile_id_1, borders_1 in tiles_borders.items()
}


def gen_corner_tile_ids(compatible_tiles):
    for tile_id, compatible_tile_ids in compatible_tiles.items():
        if len(compatible_tile_ids) == 2:
            yield tile_id


def create_empty_image(n_tiles):
    dim = int(math.sqrt(n_tiles))
    return {(x, y): None for y in range(dim) for x in range(dim)}


# +
def gen_neighbor_positions(position):
    assert len(position) == 2
    for direction in Directions:
        direction = direction.value
        yield direction, (position[0] + direction[0], position[1] + direction[1])


def gen_neighbors(position, image):
    for direction, neighbor_position in gen_neighbor_positions(position):
        if neighbor_position in image:
            yield direction, neighbor_position, image[neighbor_position]


# -

availabe_corner_tile_ids = set(gen_corner_tile_ids(compatible_tiles))
availabe_non_corner_tile_ids = set(tiles.keys())
availabe_non_corner_tile_ids -= availabe_corner_tile_ids

first_corner_tile = availabe_corner_tile_ids.pop()

image = create_empty_image(len(tiles))
image[(0, 0)] = first_corner_tile


def is_corner(position, image):
    dim = int(math.sqrt(len(image)))
    return position[0] in (0, dim - 1) and position[1] in (0, dim - 1)


# +
def calc_possible_tiles(
    position, image, available_corner_tiles, available_non_corner_tiles
):
    if is_corner(position, image):
        possible_tiles = available_corner_tiles
    else:
        possible_tiles = available_non_corner_tiles
    for _, _, neighbor_tile_id in gen_neighbors(position, image):
        if neighbor_tile_id is not None:
            possible_tiles = possible_tiles.intersection(
                compatible_tiles[neighbor_tile_id]
            )
    return position, possible_tiles


def gen_possible_tiles(image, available_corner_tiles, available_non_corner_tiles):
    for position, tile in image.items():
        if tile is not None:
            continue
        yield calc_possible_tiles(
            position, image, available_corner_tiles, available_non_corner_tiles
        )


def is_solvable(possible_tiles):
    return all(len(val) > 0 for val in possible_tiles.values())


# -

availabe_corner_tile_ids


def find_most_constrained_position(possible_tiles):
    return min(possible_tiles, key=lambda key: len(possible_tiles[key]))


def is_complete(image):
    return not any(tile is None for tile in image.values())


def search_positions(image, available_corner_tiles, available_non_corner_tiles):
    """
    Finds the right position for each tile.
    """
    if is_complete(image):
        yield image
        return
    possible_tiles = dict(
        gen_possible_tiles(image, available_corner_tiles, available_non_corner_tiles)
    )
    if not is_solvable(possible_tiles):
        return
    position = find_most_constrained_position(possible_tiles)
    available_tiles = possible_tiles[position]
    for tile in available_tiles:
        new_image = {**image, position: tile}
        new_available_corner_tiles = available_corner_tiles - set([tile])
        new_available_non_corner_tiles = available_non_corner_tiles - set([tile])
        for solution in search_positions(
            new_image, new_available_corner_tiles, new_available_non_corner_tiles
        ):
            yield solution


def solve_part_one(image, available_corner_tiles, available_non_corner_tiles):
    position_tiles = tuple(
        islice(
            search_positions(
                image, availabe_corner_tile_ids, availabe_non_corner_tile_ids
            ),
            1,
        )
    )[0]
    solution = math.prod(
        tile_id
        for position, tile_id in position_tiles.items()
        if is_corner(position, position_tiles)
    )
    return position_tiles, solution


position_tiles, solution_1 = solve_part_one(
    image, availabe_corner_tile_ids, availabe_non_corner_tile_ids
)

assert solution_1 == 2699020245973

print(f"The solution to part 1 is '{solution_1}'.")


# ## Find Matching Variations

# +
def calc_variation(tile, flip_0, flip_1, rotation):
    if flip_0:
        tile = np.flip(tile, 0)
    if flip_1:
        tile = np.flip(tile, 1)
    return np.rot90(tile, rotation)


def gen_variations(tile):
    for config in tuple(product(range(4), (False, True), (False, True))):
        yield calc_variation(tile, *config)


INVERSE_DIRECTIONS = {
    Directions.up: Directions.down,
    Directions.down: Directions.up,
    Directions.left: Directions.right,
    Directions.right: Directions.left,
    Directions.up.value: Directions.down,
    Directions.down.value: Directions.up,
    Directions.left.value: Directions.right,
    Directions.right.value: Directions.left,
}


def match_border(tile_1, tile_2, direction):
    return (
        tile_border(tile_1, direction)
        == tile_border(tile_2, INVERSE_DIRECTIONS[direction])
    ).all()


def gen_matching_variations(tile_1, tile_2, direction):
    for var_2 in gen_variations(tile_2):
        if match_border(tile_1, var_2, direction):
            yield var_2


# -


def calc_constrains(image):
    return {
        position: len(
            tuple(
                neighbor
                for _, _, neighbor in gen_neighbors(position, image)
                if neighbor is not None
            )
        )
        for position, tile in image.items()
        if tile is None
    }


def search_variations(image, old_image):
    """
    Search, but now for the variation of each tile.
    """
    if is_complete(image):
        yield image
        return
    constrains = calc_constrains(image)
    position = max(constrains, key=constrains.get)
    tile = tiles[old_image[position]]
    possible_variations = tuple(gen_variations(tile))
    for direction, neighbor_position, neighbor_tile in gen_neighbors(position, image):
        if neighbor_tile is None:
            continue
        possible_variations = tuple(
            variation
            for variation in gen_matching_variations(
                neighbor_tile, tile, INVERSE_DIRECTIONS[direction]
            )
            if any((variation == other).all() for other in possible_variations)
        )
    for variation in possible_variations:
        new_image = {**image, position: variation}
        for solution in search_variations(new_image, old_image):
            yield solution


def calc_matching_variations(position_tiles):
    start_position = (0, 0)
    for variation in gen_variations(tiles[position_tiles[start_position]]):
        new_image = {key: None for key in position_tiles}
        new_image[start_position] = variation
        solutions = tuple(islice(search_variations(new_image, position_tiles), 1))
        if solutions:
            return solutions[0]


position_variations = calc_matching_variations(position_tiles)


# ## Reconstruct Image


def remove_border(tile):
    return tile[1:-1, 1:-1]


# +
def reconstruct_image(position_variations):
    dim = int(math.sqrt(len(position_variations)))
    return np.vstack(
        tuple(
            np.hstack(
                tuple(remove_border(position_variations[(x, y)]) for y in range(dim))
            )
            for x in range(dim)
        )
    )


reconstructed_image = reconstruct_image(position_variations)
reconstructed_image.shape
# -

# ## Part 2

sea_monster_str = """
                  #
#    ##    ##    ###
 #  #  #  #  #  #
""".strip(
    "\n"
)

print(sea_monster_str)

sea_monster_image = np.array(
    tuple(
        tuple(val == "#" for val in row) for row in sea_monster_str.split("\n") if row
    )
)


# +
def gen_indices(shape1, shape2):
    x1, y1 = shape1
    x2, y2 = shape2
    for x, y in product(range(x2, x1), range(y2, y1)):
        yield (x - x2, x), (y - y2, y)


def gen_slices(shape1, shape2):
    for x, y in gen_indices(shape1, shape2):
        yield slice(*x), slice(*y)


def gen_window_arrays(array, shape):
    for slices in gen_slices(array.shape, shape):
        yield array[slices]


# -


def solve_part_two(reconstructed_image, sea_monster_image):
    def sea_monster_in_section(section):
        return ((section == sea_monster_image) | section).all()

    for variation in gen_variations(reconstructed_image):
        sea_monsters_seen = len(
            tuple(
                section
                for section in gen_window_arrays(variation, sea_monster_image.shape)
                if sea_monster_in_section(section)
            )
        )
        if sea_monsters_seen:
            break
    return reconstructed_image.sum() - sea_monster_image.sum() * sea_monsters_seen


solution_2 = solve_part_two(reconstructed_image, sea_monster_image)

assert solution_2 == 2012

print(f"The solution to part 2 is '{solution_2}'.")
