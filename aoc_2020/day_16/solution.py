"""

"""


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


def find_invalid_values(tickets, fields):
    for value in walk_values(tickets):
        if not any(is_valid(value, field) for field in fields.values()):
            yield value


def solve_part_one(fields, nearby_tickets):
    return sum(find_invalid_values(nearby_tickets, fields))


if __name__ == "__main__":
    fields, my_ticket, nearby_tickets = read_input()
    solution_1 = solve_part_one(fields, nearby_tickets)
    assert solution_1 == 25961
    print(f"The solution to part 1 is '{solution_1}'.")
