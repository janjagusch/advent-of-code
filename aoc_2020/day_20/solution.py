"""

"""

from collections import namedtuple
from copy import copy
from enum import Enum
from itertools import islice, product
from math import prod, sqrt
from typing import Dict, Set

import numpy as np

Image = namedtuple("Image", ("image_id", "data"))


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


def _process_image_data(image_data):
    return np.array(tuple(tuple(val == "#" for val in line) for line in image_data))


def _process_image(image):
    image_str = image.split("\n")[0].replace("Tile ", "").replace(":", "").strip()
    image_id = int(image_str)
    data = _process_image_data(tuple(line for line in image.split("\n")[1:] if line))
    return Image(image_id, data)


def read_input():
    with open("./test.txt", mode="r") as file_pointer:
        return tuple(
            _process_image(image) for image in file_pointer.read().split("\n\n")
        )


def transform(image_data, flip_x, flip_y, rotate):
    if flip_x:
        image_data = np.flip(image_data, 0)
    if flip_y:
        image_data = np.flip(image_data, 1)
    return np.rot90(image_data, rotate)


def gen_transformations(image_data):
    for flip_x, flip_y, rotate in product((False, True), (False, True), range(4)):
        yield transform(image_data, flip_x, flip_y, rotate)


class Directions(Enum):
    up = Array(0, 1)
    down = Array(0, -1)
    left = Array(-1, 0)
    right = Array(1, 0)


def matching_border(image_data_1, image_data_2, direction):
    if direction == Directions.up:
        border1 = image_data_1[0, :]
        border2 = image_data_2[-1, :]
    elif direction == Directions.down:
        border1 = image_data_1[-1, :]
        border2 = image_data_2[0, :]
    elif direction == Directions.left:
        border1 = image_data_1[:, 0]
        border2 = image_data_2[:, -1]
    elif direction == Directions.right:
        border1 = image_data_1[:, -1]
        border2 = image_data_2[:, 0]
    else:
        raise KeyError(direction)
    return (border1 == border2).all()


def test_matching_border():
    def run_test(img1, img2, direction):
        assert matching_border(img1, img2, direction)
        for other_direction in Directions:
            if other_direction != direction:
                assert not matching_border(img1, img2, other_direction)

    img = np.array([[1, 2, 3], [4, 5, 6]])
    img_right = np.array([[3, 4, 5], [6, 7, 8]])
    run_test(img, img_right, Directions.right)
    run_test(img_right, img, Directions.left)

    img_down = np.array([[4, 5, 6], [7, 8, 9]])
    run_test(img, img_down, Directions.down)
    run_test(img_down, img, Directions.up)

    print("Matching border tests passed.")


def test_gen_transformations():
    img = np.array([[1, 2, 3], [4, 5, 6]])
    transformations = tuple(gen_transformations(img))
    np.testing.assert_equal(img, transformations[0])
    print("Transformation generation tests passed.")


def gen_neighbors(position, composition):
    for direction in Directions:
        new_position = position + direction.value
        if new_position in composition:
            yield direction, new_position, composition[new_position]


def find_most_constrained_position(composition: Dict) -> Array:
    constrain_map = {
        position: len(
            tuple(
                neighbor
                for _, _, neighbor in gen_neighbors(position, composition)
                if neighbor is not None
            )
        )
        for position, occupant in composition.items()
        if occupant is None
    }
    return max(constrain_map, key=constrain_map.get)


def solve_part_one(images):
    shape = int(sqrt(len(images)))
    composition = {Array(x, y): None for x in range(shape) for y in range(shape)}
    # print(tuple(gen_neighbors(Array(2, 2), composition)))
    # print(find_most_constrained_position(composition))
    sol = tuple(islice(solve(composition, images), 0, 1))[0]
    # sol = solutions[0]
    corners = tuple(Array(x, y) for x, y in product((0, shape - 1), (0, shape - 1)))
    return prod(sol[c].image_id for c in corners)
    print({key: value.image_id for key, value in solutions[-1].items()})


def matches_border_with_neighbors(image: Image, position: Array, composition: Dict):
    for direction, _, neighbor in gen_neighbors(position, composition):
        if neighbor is not None:
            if not matching_border(image.data, neighbor.data, direction):
                return False
    return True


def solve(composition: Dict, images: Set):
    if not images:
        yield composition
    else:
        position = find_most_constrained_position(composition)
        for image in images:
            for transformation in gen_transformations(image.data):
                transformation = Image(image.image_id, transformation)
                if matches_border_with_neighbors(transformation, position, composition):
                    new_composition = {**composition, position: transformation}
                    new_images = tuple(i for i in images if i != image)
                    for solution in solve(new_composition, new_images):
                        yield solution


# def solve(compositions: Set, images: Set):
#     if not images:
#         return compositions
#     new_compositions = []
#     for composition in compositions:
#         position = find_most_constrained_position(composition)
#         for image in images:
#             for transformation in gen_transformations(image.data):
#                 transformation = Image(image.image_id, transformation)
#                 if matches_border_with_neighbors(transformation, position, composition):
#                     new_composition = {**composition, position: transformation}

#                     new_compositions.append(new_composition)
#     print(f"{len(new_compositions)} possible compositions.")
#     return solve(new_compositions, images[1:])


if __name__ == "__main__":
    test_matching_border()
    test_gen_transformations()
    images = read_input()
    print(len(images))
    solution_1 = solve_part_one(images)
    print(solution_1)
