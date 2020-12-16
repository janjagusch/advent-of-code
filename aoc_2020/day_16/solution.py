"""
Solution to https://adventofcode.com/2020/day/16
"""

from math import prod


def _proces_rules(rules):
    def adjust_range(min, max):
        return min, max + 1

    return {
        line.split(":")[0]: tuple(
            range(*adjust_range(*(int(c) for c in val.strip().split("-"))))
            for val in line.split(":")[1].split(" or ")
        )
        for line in rules.split("\n")
        if line
    }


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        rules, my_ticket, nearby_tickets = tuple(
            chunk.strip() for chunk in file_pointer.read().split("\n\n")
        )
    rules = _proces_rules(rules)
    my_ticket = tuple(int(val) for val in my_ticket.split("\n")[1].split(","))
    nearby_tickets = tuple(
        tuple(int(val) for val in ticket.split(","))
        for ticket in nearby_tickets.split("\n")[1:]
    )
    return rules, my_ticket, nearby_tickets


def is_valid(value, rules):
    return any(value in rule for rule in rules)


def walk_values(tickets):
    for ticket in tickets:
        for value in ticket:
            yield value


def walk_ticket_positions(tickets):
    for i in range(len(tickets[0])):
        yield tuple(ticket[i] for ticket in tickets)


def find_invalid_values(tickets, fields):
    for value in walk_values(tickets):
        if not any(is_valid(value, field) for field in fields.values()):
            yield value


def solve_part_one(fields, nearby_tickets):
    return sum(find_invalid_values(nearby_tickets, fields))


def filter_invalid_tickets(fields, tickets):
    for ticket in tickets:
        if all(
            any(is_valid(value, rules) for rules in fields.values()) for value in ticket
        ):
            yield ticket


def solve_part_two(fields, nearby_tickets, my_ticket):
    nearby_tickets = tuple(filter_invalid_tickets(fields, nearby_tickets))
    possibilities = tuple(
        set(
            field_name
            for field_name, rules in fields.items()
            if all(is_valid(value, rules) for value in ticket_position)
        )
        for ticket_position in walk_ticket_positions(nearby_tickets)
    )
    solution = find_solution(possibilities, ())
    ticket_labelled = {field: value for field, value in zip(solution, my_ticket)}
    return prod(
        val for key, val in ticket_labelled.items() if key.startswith("departure")
    )


def find_solution(possibilities, current_solution):
    if not possibilities:
        return current_solution
    for field in possibilities[0]:
        if field not in current_solution:
            new_solution = find_solution(possibilities[1:], (*current_solution, field))
            if new_solution:
                return new_solution


if __name__ == "__main__":
    fields, my_ticket, nearby_tickets = read_input()
    solution_1 = solve_part_one(fields, nearby_tickets)
    assert solution_1 == 25961
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(fields, nearby_tickets, my_ticket)
    assert solution_2 == 603409823791
    print(f"The solution to part 2 is '{solution_2}'.")
