"""
https://adventofcode.com/2020/day/1#part1
"""

import itertools


def solve_part_one(expense_report):
    for a, b in itertools.product(expense_report, expense_report):
        if a + b == 2020:
            return a * b


def solve_part_two(expense_report):
    for a, b, c in itertools.product(expense_report, expense_report, expense_report):
        if a + b + c == 2020:
            return a * b * c


if __name__ == "__main__":
    with open("./input.txt", mode="r") as file_pointer:
        expense_report = [
            int(expense) for expense in file_pointer.read().split("\n") if expense
        ]
    print(f"The solution to part 1 is '{solve_part_one(expense_report)}'.")
    print(f"The solution to part 2 is '{solve_part_two(expense_report)}'.")
