"""

"""

from itertools import count


def _process_messages(messages):
    return tuple(line for line in messages.split())


def _process_rule(rule):
    key, value = rule.split(": ")
    value = tuple(value.replace('"', "").split(" | "))
    value = tuple(tuple(val.split(" ")) for val in value)
    return key, value


def _process_rules(rules):
    return dict(_process_rule(rule) for rule in rules.split("\n") if rule)


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        rules, messages = file_pointer.read().split("\n\n")
        return _process_rules(rules), _process_messages(messages)


def _apply_pattern(expression, pattern):
    if expression.startswith(pattern):
        return expression[len(pattern) :]
    return None


def solve_expressions(expressions, sub_rules, rules):
    for rule_chain in sub_rules:
        possible_expressions = set(expressions)
        for rule in rule_chain:
            if rule in rules:
                possible_expressions = set(
                    solve_expressions(possible_expressions, rules[rule], rules)
                )
            else:
                new_possible_expressions = set()
                for expression in possible_expressions:
                    exp = _apply_pattern(expression, rule)
                    if exp is not None:
                        new_possible_expressions.add(exp)
                possible_expressions = new_possible_expressions
        for expression in possible_expressions:
            yield expression


def solve(message, rules, start_key):
    return "" in solve_expressions((message,), rules[start_key], rules)


def solve_part_one(messages, rules):
    return sum(solve(message, rules, "0") for message in messages)


def _solve_part_two(message, rules):
    """
    Explanation:
        * `8 = 42 or (42 and 8)`: *one or more* occurences of rule 42.
        * `11 = (42 and 31) or (41 and 11 and 31)`: *one or more* occurences of rule 42
            followed by the *same number* of occurences of rules 31.
        * `0 = 8 and 11`: *two or more* occurences of rule 42
            followed by *one or more* occurences of rule 31,
            where rule 42 occurs more often than rule 31.
    """

    def chain_apply_rule(expressions, rule, rules):
        for c in count(start=0):
            if (new_expressions := set(solve_expressions(expressions, rule, rules))) :
                expressions = new_expressions
            else:
                break
        return expressions, c

    expressions = (message,)
    expressions, count_42 = chain_apply_rule(expressions, rules["42"], rules)
    expressions, count_31 = chain_apply_rule(expressions, rules["31"], rules)
    return "" in expressions and count_42 > 1 and count_31 in range(1, count_42)


def solve_part_two(messages, rules):
    return sum(_solve_part_two(message, rules) for message in messages)


if __name__ == "__main__":
    rules, messages = read_input()
    solution_1 = solve_part_one(messages, rules)
    assert solution_1 == 285
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(messages, rules)
    assert solution_2 == 412
    print(f"The solution to part 2 is '{solution_2}'.")
