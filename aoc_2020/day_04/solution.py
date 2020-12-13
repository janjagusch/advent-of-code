"""
Solution to https://adventofcode.com/2020/day/4
"""

import re

REQUIRED_KEYS = (
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    # "cid",
)

HCL_PATTERN = re.compile(r"^#[a-f|\d]{6}$")
PID_PATTERN = re.compile(r"^\d{9}$")


def is_valid_one(passport):
    return all(key in passport for key in REQUIRED_KEYS)


def is_valid_height(height):
    h, unit = int(height[:-2]), height[-2:]
    if unit == "cm":
        return 150 <= h <= 193
    if unit == "in":
        return 59 <= h <= 76
    return False


def is_valid_hair_color(hair_color):
    return bool(re.search(HCL_PATTERN, hair_color))


def is_valid_passport_id(passport_id):
    return bool(re.search(PID_PATTERN, passport_id))


def is_valid_two(passport):
    return (
        is_valid_one(passport)
        and 1920 <= int(passport["byr"]) <= 2002
        and 2010 <= int(passport["iyr"]) <= 2020
        and 2020 <= int(passport["eyr"]) <= 2030
        and is_valid_height(passport["hgt"])
        and is_valid_hair_color(passport["hcl"])
        and passport["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
        and is_valid_passport_id(passport["pid"])
    )


def solve(passports, is_valid_func):
    return sum(is_valid_func(passport) for passport in passports)


if __name__ == "__main__":
    with open("./input.txt", mode="r") as file_pointer:
        passports = [
            dict((kv.split(":") for kv in passport.split()))
            for passport in file_pointer.read().split("\n\n")
        ]
    print(f"The solution for part 1 is '{solve(passports, is_valid_one)}'.")
    print(f"The solution for part 2 is '{solve(passports, is_valid_two)}'.")
