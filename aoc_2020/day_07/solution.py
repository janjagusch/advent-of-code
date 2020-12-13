"""
Solution to https://adventofcode.com/2020/day/7
"""

from collections import namedtuple

_Container = namedtuple("Container", ("bag", "quantity"))


def _process_bag_rule(bag_rule):
    bag = " ".join(bag_rule.split()[:2])
    contains = set(
        _Container(" ".join(container.split()[1:3]), int(container.split()[0]))
        for container in bag_rule.split("contain")[-1].split(",")
        if container.strip() != "no other bags."
    )
    return bag, contains


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return dict(
            _process_bag_rule(bag_rule)
            for bag_rule in file_pointer.read().split("\n")
            if bag_rule
        )


def eventually_contain(bag_rules, bags):
    bags = set(bags)
    new_bags = set(
        key
        for key, value in bag_rules.items()
        if any(container.bag in bags for container in value)
    )
    diff_bags = new_bags - bags
    if diff_bags:
        more_bags = eventually_contain(bag_rules, diff_bags)
        new_bags |= more_bags
    return bags | new_bags


def solve_part_one(bag_rules):
    initial_bags = set(["shiny gold"])
    return len(eventually_contain(bag_rules, initial_bags) - initial_bags)


def _walk_bags(bag_rules, bag):
    contains = bag_rules[bag]
    for container in contains:
        for _ in range(container.quantity):
            for sub_container in _walk_bags(bag_rules, container.bag):
                yield sub_container
            yield container.quantity


def solve_part_two(bag_rules):
    return len(tuple(_walk_bags(bag_rules, "shiny gold")))


if __name__ == "__main__":
    bag_rules = read_input()
    solution_1 = solve_part_one(bag_rules)
    assert solution_1 == 121
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(bag_rules)
    assert solution_2 == 3805
    print(f"The solution to part 2 is '{solution_2}'.")
