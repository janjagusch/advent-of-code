"""

"""

from itertools import count

_DIRS = (-1, 0, 1)
_DIRECTIONS = tuple((x, y) for x in _DIRS for y in _DIRS if x or y)


def look_into_direction(seats, pos, direction, max_horizon):
    for multiplier in count(start=1):
        if max_horizon is not None and multiplier > max_horizon:
            break
        vector = direction[0] * multiplier, direction[1] * multiplier
        new_pos = pos[0] + vector[0], pos[1] + vector[1]
        if any(val < 0 for val in new_pos):
            break
        try:
            seat = seats[new_pos[1]][new_pos[0]]
        except IndexError:
            break
        if seat is not None:
            return seat
    return None


def _decode_value(val):
    if val == "L":
        return False
    if val == "#":
        return True
    if val == ".":
        return None
    raise ValueError(val)


def read_input():
    with open(
        "./input.txt",
        mode="r",
    ) as file_pointer:
        return tuple(
            tuple(_decode_value(val) for val in line)
            for line in file_pointer.read().split("\n")
            if line
        )


def gen_neighbors(seats, pos, max_horizon):
    for direction in _DIRECTIONS:
        yield look_into_direction(seats, pos, direction, max_horizon)


def rule_1(seat, neighbors):
    if seat is None:
        return None
    n_occupied = sum(neighbor for neighbor in neighbors if neighbor)
    if not seat and not n_occupied:
        return True
    if seat and n_occupied >= 4:
        return False
    return seat


def rule_2(seat, neighbors):
    if seat is None:
        return None
    n_occupied = sum(neighbor for neighbor in neighbors if neighbor)
    if not seat and not n_occupied:
        return True
    if seat and n_occupied >= 5:
        return False
    return seat


def calc_new_seats(seats, shape, max_horizon, rule):
    width, height = shape
    return tuple(
        tuple(
            (rule(seats[y][x], gen_neighbors(seats, (x, y), max_horizon)))
            for x in range(width)
        )
        for y in range(height)
    )


def evolve(seats, max_horizon, rule):
    shape = len(seats[0]), len(seats)
    old_seats = None
    new_seats = seats
    while old_seats != new_seats:
        old_seats = new_seats
        new_seats = calc_new_seats(new_seats, shape, max_horizon, rule)
    return sum(seat for row in new_seats for seat in row if seat)


def solve_part_one(seats):
    return evolve(seats, 1, rule_1)


def solve_part_two(seats):
    return evolve(seats, None, rule_2)


if __name__ == "__main__":
    seats = read_input()
    solution_1 = solve_part_one(seats)
    assert solution_1 == 2254
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(seats)
    assert solution_2 == 2004
    print(f"The solution to part 2 is '{solution_2}'.")
