"""

"""

_DIRS = (-1, 0, 1)
_DIRECTIONS = tuple((x, y) for x in _DIRS for y in _DIRS if x or y)


def _format_seat(seat):
    if seat is None:
        return "."
    if seat:
        return "#"
    if not seat:
        return "L"
    raise ValueError(seat)


def display(seats):
    return "\n".join("".join(_format_seat(seat) for seat in row) for row in seats)


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


def gen_neighbors(seats, pos):
    x, y = pos
    for direction in _DIRECTIONS:
        dx, dy = direction
        nx, ny = x + dx, y + dy
        if any(val < 0 for val in (nx, ny)):
            continue
        try:
            yield seats[ny][nx]
        except IndexError:
            pass


def _apply_rule(seats, pos):
    x, y = pos
    if (seat := seats[y][x]) is None:
        return None
    n_occupied = sum(neighbor for neighbor in gen_neighbors(seats, pos) if neighbor)
    if not seat and not n_occupied:
        return True
    if seat and n_occupied >= 4:
        return False
    return seat


def calc_new_seats(seats, shape):
    width, height = shape
    return tuple(
        tuple(_apply_rule(seats, (x, y)) for x in range(width)) for y in range(height)
    )


def solve_part_one(seats):
    shape = len(seats[0]), len(seats)
    old_seats = None
    new_seats = seats
    while old_seats != new_seats:
        old_seats = new_seats
        new_seats = calc_new_seats(new_seats, shape)
    return sum(seat for row in new_seats for seat in row if seat)


if __name__ == "__main__":
    seats = read_input()
    solution_1 = solve_part_one(seats)
    assert solution_1 == 2254
    print(f"The solution to part 1 is '{solution_1}'.")
