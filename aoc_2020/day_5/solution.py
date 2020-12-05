"""

"""

from operator import mul

ROW_ONE = "B"
COLUMN_ONE = "R"


def bitlist_to_int(bitlist):
    """
    https://stackoverflow.com/a/12461400/7380270
    """
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out


def process_boarding_pass(boarding_pass):
    return (
        bitlist_to_int(char == ROW_ONE for char in boarding_pass[:7]),
        bitlist_to_int(char == COLUMN_ONE for char in boarding_pass[-3:]),
    )


def seat_id(row, column):
    return row * 8 + column


def solve_part_one(boarding_passes):
    return max(
        seat_id(*process_boarding_pass(boarding_pass))
        for boarding_pass in boarding_passes
    )


def solve_part_two(boarding_passes):
    seat_ids = set(
        seat_id(*process_boarding_pass(boarding_pass))
        for boarding_pass in boarding_passes
    )
    for possible_seat_id in range(min(seat_ids), max(seat_ids)):
        if possible_seat_id not in seat_ids:
            return possible_seat_id


assert process_boarding_pass("FBFBBFFRLR") == (44, 5)


if __name__ == "__main__":
    with open("./input.txt", mode="r") as file_pointer:
        boarding_passes = [
            boarding_pass
            for boarding_pass in file_pointer.read().split("\n")
            if boarding_pass
        ]
    print(f"The solution for part 1 is '{solve_part_one(boarding_passes)}'.")
    print(f"The solution for part 2 is '{solve_part_two(boarding_passes)}'.")
