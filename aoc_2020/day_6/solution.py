"""

"""

from collections import Counter


def solve_part_one(customs_forms):
    return sum(len(Counter("".join(group)).keys()) for group in customs_forms)


def present_in_all(group):
    counter = Counter("".join(group))
    return sum(all(char in person for person in group) for char in counter)


def solve_part_two(customs_forms):
    return sum(present_in_all(group) for group in customs_forms)


if __name__ == "__main__":
    with open("./input.txt", mode="r") as file_pointer:
        customs_forms = [
            [person for person in group.split()]
            for group in file_pointer.read().split("\n\n")
        ]
    print(f"The solution to part 1 is '{solve_part_one(customs_forms)}'")
    print(f"The solution to part 2 is '{solve_part_two(customs_forms)}'")
