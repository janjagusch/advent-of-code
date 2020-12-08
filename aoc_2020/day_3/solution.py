"""
Solution to https://adventofcode.com/2020/day/3
"""

from functools import reduce
from operator import mul

TREE_CHAR = "#"


def is_tree(x, y, forest, width):
    return forest[y][x % width]


def traverse(forest, height, width, right, down):
    x, y = 0, 0
    while y < height:
        yield is_tree(x, y, forest, width)
        x += right
        y += down


def solve_part_one(forest, height, width):
    return sum(traverse(forest, height, width, 3, 1))


def solve_part_two(forest, height, width):
    slopes = (
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    )
    return reduce(
        mul, (sum(traverse(forest, height, width, *slope)) for slope in slopes)
    )


if __name__ == "__main__":
    with open("./input.txt", mode="r") as file_pointer:
        forest = [
            [char == TREE_CHAR for char in line]
            for line in file_pointer.read().split("\n")
            if line
        ]
    shape = len(forest), len(forest[0])
    print(f"The solution for part 1 is '{solve_part_one(forest, *shape)}'.")
    print(f"The solution for part 2 is '{solve_part_two(forest, *shape)}'.")
