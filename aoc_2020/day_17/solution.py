"""

"""

from collections import namedtuple
from itertools import product


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


Cube = namedtuple("Cube", ["position", "state"])


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        z = 0
        return set(
            Array(x, y, z)
            for y, line in enumerate(file_pointer.read().split("\n"))
            for x, val in enumerate(line)
            if line and val == "#"
        )


def gen_neighbor_positions(position, directions):
    for direction in directions:
        yield position + direction


def gen_neighbor_positions_values(pocket_dimension, position, directions):
    for neighbor_position in gen_neighbor_positions(position, directions):
        yield Cube(neighbor_position, neighbor_position in pocket_dimension)


def change_state(current_state, neighbor_states):
    """
    If a cube is active and exactly 2 or 3 of its neighbors are also active,
    the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active,
    the cube becomes active. Otherwise, the cube remains inactive.

    """
    neighbors_active = sum(neighbor_states)
    if current_state:
        return neighbors_active in (2, 3)
    return neighbors_active == 3


def cycle(pocket_dimension, directions):
    new_pocket_dimension = set()
    for cube in set(
        cube
        for position in pocket_dimension
        for cube in gen_neighbor_positions_values(
            pocket_dimension, position, directions
        )
    ):

        neighbors = tuple(
            gen_neighbor_positions_values(pocket_dimension, cube.position, directions)
        )
        neighbor_states = tuple(neighbor.state for neighbor in neighbors)
        new_cube = Cube(cube.position, change_state(cube.state, neighbor_states))
        if new_cube.state:
            new_pocket_dimension.add(new_cube.position)
    return new_pocket_dimension


def solve_part_one(pocket_dimension):
    n_dim = 3
    directions = tuple(
        Array(*direction)
        for direction in product(*tuple((-1, 0, 1) for _ in range(n_dim)))
        if any(val for val in direction)
    )
    for _ in range(6):
        pocket_dimension = cycle(pocket_dimension, directions)
    return len(pocket_dimension)


def solve_part_two(pocket_dimension):
    n_dim = 4
    directions = tuple(
        Array(*direction)
        for direction in product(*tuple((-1, 0, 1) for _ in range(n_dim)))
        if any(val for val in direction)
    )
    for _ in range(6):
        pocket_dimension = cycle(pocket_dimension, directions)
    return len(pocket_dimension)


if __name__ == "__main__":
    pocket_dimension = read_input()
    solution_1 = solve_part_one(pocket_dimension)
    # assert solution_1 == 386
    print(solution_1)
    # Adding another dimension.
    pocket_dimension = set(Array(*array._vals, 0) for array in pocket_dimension)
    solution_2 = solve_part_two(pocket_dimension)
    assert solution_2 == 2276
    print(solution_2)
