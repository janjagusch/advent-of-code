"""

"""

from collections import namedtuple


Instruction = namedtuple("Instruction", ["type", "value", "address"])


def process_line(line):
    """
    mask = X111000X0101100001000000100011X0000X
    mem[4812] = 133322396
    """
    type = line.split("=")[0].strip()
    value = line.split("=")[1].strip()
    if type == "mask":
        address = None
    elif type.startswith("mem"):
        address = int(type.split("[")[1][:-1])
        value = int(value)
        type = "mem"
    else:
        raise KeyError(type)
    return Instruction(type, value, address)


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(process_line(line) for line in file_pointer.readlines())


def convert_mask(mask):
    def and_mask(mask):
        return int("".join(str(int(char != "0")) for char in mask), 2)

    def or_mask(mask):
        return int("".join(str(int(char == "1")) for char in mask), 2)

    return and_mask(mask), or_mask(mask)


def apply_mask(value, and_mask, or_mask):
    return value & and_mask | or_mask


def run_program(program):
    masks = None
    memory = {}
    for instruction in program:
        if instruction.type == "mask":
            masks = convert_mask(instruction.value)
        if instruction.type == "mem":
            memory[instruction.address] = apply_mask(instruction.value, *masks)
    return memory


def solve_part_one(program):
    return sum(run_program(program).values())


if __name__ == "__main__":
    program = read_input()
    solution_1 = solve_part_one(program)
    assert solution_1 == 8570568288597
    print(f"The solution to part 1 is '{solution_1}'.")
