"""
Solution to https://adventofcode.com/2020/day/1.
"""

import itertools


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return [int(expense) for expense in file_pointer.read().split("\n") if expense]


def solve_part_one(expense_report):
    for a, b in itertools.product(expense_report, expense_report):
        if a + b == 2020:
            return a * b


def solve_part_two(expense_report):
    for a, b, c in itertools.product(expense_report, expense_report, expense_report):
        if a + b + c == 2020:
            return a * b * c


if __name__ == "__main__":
    expense_report = read_input()
    solution_1 = solve_part_one(expense_report)
    assert solution_1 == 838624
    solution_2 = solve_part_two(expense_report)
    assert solution_2 == 52764180
    print(f"The solution to part 1 is '{solve_part_one(expense_report)}'.")
    print(f"The solution to part 2 is '{solve_part_two(expense_report)}'.")
