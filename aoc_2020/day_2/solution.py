"""
Solution for https://adventofcode.com/2020/day/2
"""

from operator import xor


def process_pwp(pwp):
    range_, char, password = pwp.split()
    range_ = [int(val) for val in range_.split("-")]
    char = char[0]
    return range_, char, password


def is_valid_one(range_, char, password):
    return range_[0] <= password.count(char) <= range_[1]


def is_valid_two(range_, char, password):
    return xor(password[range_[0] - 1] == char, password[range_[1] - 1] == char)


def solve(password_policies, is_valid_func):
    return sum(is_valid_func(*process_pwp(pwp)) for pwp in password_policies)


if __name__ == "__main__":
    with open("./input.txt", mode="r") as file_pointer:
        password_policies = [pwp for pwp in file_pointer.read().split("\n") if pwp]
    print(f"The solution to part 1 is '{solve(password_policies, is_valid_one)}'.")
    print(f"The solution to part 2 is '{solve(password_policies, is_valid_two)}'.")
