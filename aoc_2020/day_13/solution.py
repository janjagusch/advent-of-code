"""

"""

from math import ceil


def read_file():
    with open("./input.txt", mode="r") as file_pointer:
        lines = file_pointer.read().split("\n")
        earliest_departure = int(lines[0])
        bus_schedule = tuple(int(val) for val in lines[1].split(",") if val != "x")
        return earliest_departure, bus_schedule


def solve_part_one(earliest_departure, bus_schedule):
    waiting_times = tuple(
        (
            bus * ceil(earliest_departure / bus) % earliest_departure
            for bus in bus_schedule
        )
    )
    return min(waiting_times) * bus_schedule[waiting_times.index(min(waiting_times))]


if __name__ == "__main__":
    earliest_departure, bus_schedule = read_file()
    solution_1 = solve_part_one(earliest_departure, bus_schedule)
    assert solution_1 == 2382
    print(f"The solution to part 1 is '{solution_1}'.")
