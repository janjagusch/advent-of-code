"""

"""

from functools import partial


class RuleError(Exception):
    """
    Error that is thrown when applying rule fails.
    """


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
    raise RuleError(expression, pattern)


def _call(rule_chain, rules, ind):
    for rule in rule_chain:
        if rule not in rules:
            print((rule, ind))
            ind += 1
        else:
            ind = _call(rules[rule], rules, ind)
    return ind


def _call_2(sub_rules, rules, indices):
    new_indices = []
    for index in indices:
        for rule_chain in sub_rules:
            for rule in rule_chain:
                if rule not in rule:
                    print((rule, ind))
                    ind += 1


def _call_2(sub_rules, rules, ind):

    for rule in rule_chain:
        if rule not in rules:
            print((rule, ind))
            ind += 1
        else:
            ind = _call(rules[rule], rules, ind)
    return ind


def _apply_rule(expression, rule, rules):
    print(expression)
    rule_applies = False
    for sub_rule in rule:
        sub_rule_applies = True
        for pattern in sub_rule:
            print(pattern)
            if pattern in rules:
                func = partial(_apply_rule, rule=rules[pattern], rules=rules)
            else:
                func = partial(_apply_pattern, pattern=pattern)
            try:
                expression = func(expression)
            except RuleError:
                sub_rule_applies = False
                break
        if sub_rule_applies:
            rule_applies = True
            break
    if not rule_applies:
        error = RuleError(expression, rule)
        print(error)
        raise error
    return expression


def match_rule(message, start_rule, rules):
    try:
        expression = _apply_rule(message, start_rule, rules)
    except RuleError:
        return False
    return not expression


def solve_expressions(expressions, sub_rules, rules):
    for rule_chain in sub_rules:
        possible_expressions = tuple(expressions)
        for rule in rule_chain:
            if rule in rules:
                possible_expressions = tuple(
                    solve_expressions(possible_expressions, rules[rule], rules)
                )
            else:
                new_possible_expressions = []
                for expression in possible_expressions:
                    try:
                        new_possible_expressions.append(
                            _apply_pattern(expression, rule)
                        )
                    except RuleError:
                        continue
                possible_expressions = new_possible_expressions
        for expression in possible_expressions:
            yield expression


def solve(message, rules, start_key):
    return "" in solve_expressions((message,), rules[start_key], rules)


def solve_part_one(messages, rules):
    return sum(solve(message, rules, "0") for message in messages)


if __name__ == "__main__":
    rules, messages = read_input()
    solution_1 = solve_part_one(messages, rules)
    print(f"The solution to part 1 is '{solution_1}'.")
    # messages = (
    #     "aaaabb",
    #     "aaabab",
    #     "abbabb",
    #     "abbbab",
    #     "aabaab",
    #     "aabbbb",
    #     "abaaab",
    #     "ababbb",
    # )
    # for message in messages:
    #     assert solve(message, rules, "0")
