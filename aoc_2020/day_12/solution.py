"""

"""

from collections import namedtuple

NavigationInstruction = namedtuple("NavigationInstruction", ("action", "value"))


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

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other)
            return self.__class__(*[val_1 * val_2 for val_1, val_2 in zip(self, other)])
        if isinstance(other, int):
            return self.__class__(*[val * other for val in self])

    def __repr__(self):
        return f"{self.__class__.__name__}{self._vals}"


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(
            NavigationInstruction(line[0], int(line[1:]))
            for line in file_pointer.read().split("\n")
            if line
        )


DEGREE_TO_DIRECTION = {0: "N", 90: "E", 180: "S", 270: "W"}

DIRECTION_TO_VECTOR = {
    "N": Array(1, 0),
    "E": Array(0, 1),
    "S": Array(-1, 0),
    "W": Array(0, -1),
}


def navigate_1(navigation_instructions):
    pos = Array(0, 0)
    degree = 90
    for instruction in navigation_instructions:
        if instruction.action in ("N", "S", "E", "W"):
            pos += DIRECTION_TO_VECTOR[instruction.action] * instruction.value
        elif instruction.action in ("L", "R"):
            val = (
                instruction.value * -1
                if instruction.action == "L"
                else instruction.value
            )
            degree += val
        elif instruction.action == "F":
            pos += (
                DIRECTION_TO_VECTOR[DEGREE_TO_DIRECTION[degree % 360]]
                * instruction.value
            )
        else:
            raise KeyError(instruction.action)

    return pos


def navigate_2(navigation_instructions):
    waypoint = Array(1, 10)
    pos = Array(0, 0)
    for instruction in navigation_instructions:
        if instruction.action in ("N", "S", "E", "W"):
            waypoint += DIRECTION_TO_VECTOR[instruction.action] * instruction.value
        elif instruction.action in ("L", "R"):
            val = (
                instruction.value * -1
                if instruction.action == "L"
                else instruction.value
            ) % 360
            if val == 180:
                waypoint *= -1
            elif val == 90:
                waypoint = Array(-1 * waypoint[1], waypoint[0])
            elif val == 270:
                waypoint = Array(waypoint[1], -1 * waypoint[0])
            else:
                raise KeyError(val)
        elif instruction.action == "F":
            pos += waypoint * instruction.value
        else:
            raise KeyError(instruction.action)

    return pos


def solve_part_one(navigation_instructions):
    return sum(abs(val) for val in navigate_1(navigation_instructions))


def solve_part_two(navigation_instructions):
    return sum(abs(val) for val in navigate_2(navigation_instructions))


if __name__ == "__main__":
    navigation_instructions = read_input()
    solution_1 = solve_part_one(navigation_instructions)
    assert solution_1 == 362
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(navigation_instructions)
    assert solution_2 == 29895
    print(f"The solution to part 2 is '{solution_2}'.")
