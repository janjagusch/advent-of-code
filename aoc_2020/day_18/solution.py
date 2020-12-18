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


if __name__ == "__main__":
    print(process_expression("1 + (2 * 3) + (4 * (5 + 6))").calculate())
    print(process_expression("2 * 3 + (4 * 5)").calculate())
    print(process_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))").calculate())
    print(
        process_expression(
            "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
        ).calculate()
    )
