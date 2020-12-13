"""
Solution to https://adventofcode.com/2020/day/13
"""

from itertools import count
from math import ceil, prod


def read_file():
    with open("./input.txt", mode="r") as file_pointer:
        lines = file_pointer.read().split("\n")
        earliest_departure = int(lines[0])
        bus_schedule = tuple(
            int(val) if val != "x" else None for val in lines[1].split(",")
        )
        return earliest_departure, bus_schedule


def solve_part_one(earliest_departure, bus_schedule):
    bus_schedule = tuple(val for val in bus_schedule if val)
    waiting_times = tuple(
        (
            bus * ceil(earliest_departure / bus) % earliest_departure
            for bus in bus_schedule
        )
    )
    return min(waiting_times) * bus_schedule[waiting_times.index(min(waiting_times))]


def assert_relative_prime(num_1, num_2):
    """
    Asserts that two numbers don't share a common prime factor.
    Currently not implemented!

    Raises:
        ValueError: If the two numbers share a least one common prime factor.
    """
    pass


def guess_mod_inverse(n, mod):
    """
    Guesses the modulo inverse x, such that
        <n> * x = 1 (mod <mod>)

    This is a trivial implementation that works well for rather small numbers.
    For big numbers, the extended euclidean algorithm would be best.
    """
    for c in count(start=1):
        if (c * n) % mod == 1:
            return c


def chinese(remainder, moduli):
    """
    Applies the chinese remainder theorem.
    """
    assert len(remainder) == len(moduli)
    for num_1 in moduli:
        for num_2 in moduli:
            if num_1 != num_2:
                assert_relative_prime(num_1, num_2)
    N_prod = prod(moduli)
    N = tuple(int(N_prod / mod) for mod in moduli)
    X = tuple(guess_mod_inverse(n, mod) for n, mod in zip(N, moduli))
    x = sum(prod((bi, ni, xi)) for bi, ni, xi in zip(remainder, N, X))
    x %= prod(moduli)
    return x, prod(moduli)


def solve_part_two(bus_schedule):
    moduli = tuple(val for val in bus_schedule if val)
    remainder = tuple(-i for i, val in enumerate(bus_schedule) if val)
    return chinese(remainder, moduli)[0]


if __name__ == "__main__":
    earliest_departure, bus_schedule = read_file()
    solution_1 = solve_part_one(earliest_departure, bus_schedule)
    assert solution_1 == 2382
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(bus_schedule)
    assert solution_2 == 906332393333683, f"Wrong solution: {solution_2}."
    print(f"The solution to part 2 is '{solution_2}'.")
