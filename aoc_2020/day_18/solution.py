"""

"""

from math import prod


class Node:
    def __init__(self, operator, children):
        self._operator = operator
        self._children = children

    def calculate(self):
        return self._operator(
            tuple(
                child.calculate() if isinstance(child, self.__class__) else child
                for child in self._children
            )
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(operator={self._operator.__name__}, children={self._children})"


OPERATOR_MAP = {
    "+": sum,
    "*": prod,
}


def find_splitting_operator_index(expression):
    nested = 0
    for i, char in enumerate(reversed(expression)):
        if char in OPERATOR_MAP and not nested:
            return len(expression) - (i + 1)
        if char == "(":
            nested += 1
        if char == ")":
            nested -= 1
        assert nested <= 0
    raise RuntimeError(expression)


def has_removeable_paranthesis(expression):
    nested = 0
    for char in expression[:-1]:
        if char == "(":
            nested += 1
        if char == ")":
            nested -= 1
        assert nested >= 0
        if not nested:
            return False
    return True


def process_expression(expression):
    if has_removeable_paranthesis(expression):
        expression = expression[1:-1]
    splitting_index = find_splitting_operator_index(expression)
    first_part = expression[: splitting_index - 1]
    if first_part.startswith("("):
        first_part = process_expression(first_part)
    else:
        try:
            first_part = int(first_part)
        except ValueError:
            first_part = process_expression(first_part)
    second_part = expression[splitting_index + 2 :]
    if second_part.startswith("("):
        second_part = process_expression(second_part)
    else:
        try:
            second_part = int(second_part)
        except ValueError:
            second_part = process_expression(second_part)
    operator = OPERATOR_MAP[expression[splitting_index]]
    return Node(operator, (first_part, second_part))


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(line for line in file_pointer.read().split("\n") if line)


def solve_part_one(expressions):
    return sum(process_expression(expression).calculate() for expression in expressions)


if __name__ == "__main__":
    expressions = read_input()
    solution_1 = solve_part_one(expressions)
    assert solution_1 == 2743012121210
    print(f"The solution to part 1 is '{solution_1}'.")
