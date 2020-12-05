"""
https://adventofcode.com/2020/day/1#part1
"""

import itertools


def solve(expense_report):
    for a, b in itertools.product(expense_report, expense_report):
        if a + b == 2020:
            return a * b


if __name__ == "__main__":
    with open("./expense_report.txt", mode="r") as file_pointer:
        expense_report = [
            int(expense) for expense in file_pointer.read().split("\n") if expense
        ]
    print(f"The solution is '{solve(expense_report)}'.")
