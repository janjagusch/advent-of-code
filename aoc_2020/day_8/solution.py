"""

"""

from collections import namedtuple

Instruction = namedtuple("Instruction", ["line_number", "type", "value"])


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return {
            line_number: Instruction(line_number, line.split()[0], int(line.split()[1]))
            for line_number, line in enumerate(file_pointer.readlines())
        }


def run(instructions):
    accumulator = 0
    current_line = 0
    visited_lines = set()
    while True:
        if current_line in visited_lines:
            return accumulator, False
        if current_line == len(instructions):
            return accumulator, True
        visited_lines.add(current_line)
        instruction = instructions[current_line]
        if instruction.type == "acc":
            accumulator += instruction.value
            current_line += 1
        elif instruction.type == "jmp":
            current_line += instruction.value
        elif instruction.type == "nop":
            current_line += 1
        else:
            raise ValueError(instruction.type)


def solve_part_one(instructions):
    solution, _ = run(instructions)
    return solution


def gen_possible_instructions(instructions):
    for line_number, line in instructions.items():
        if line.type in ("nop", "jmp"):
            new_instructions = dict(instructions)
            new_type = "nop" if line.type == "jmp" else "jmp"
            new_instructions[line_number] = Instruction(
                line.line_number, new_type, line.value
            )
            yield new_instructions


def solve_part_two(instructions):
    for possible_instructions in gen_possible_instructions(instructions):
        accumulator, terminated = run(possible_instructions)
        if terminated:
            return accumulator
    raise RuntimeError


if __name__ == "__main__":
    instructions = read_input()
    solution_1 = solve_part_one(instructions)
    assert solution_1 == 1501
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(instructions)
    print(f"The solution to part 2 is '{solution_2}'.")
