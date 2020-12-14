"""

"""

from itertools import chain, combinations
from collections import namedtuple


Instruction = namedtuple("Instruction", ["type", "value", "address"])


def _highest_power_of_two(val, max_power=36):
    for power in range(max_power + 1):
        if 2 ** power > val:
            return 2 ** (power - 1)
    raise ValueError(val)


def gen_power_two_decomposition(val, max_power=36):
    while val:
        power_of_two = _highest_power_of_two(val, max_power)
        val -= power_of_two
        yield power_of_two


def powerset(iterable):
    """
    https://stackoverflow.com/a/1482316/7380270
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def gen_possible_or_masks(floating_mask):
    for ps in powerset(gen_power_two_decomposition(floating_mask)):
        yield sum(ps)


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

    def floating_mask(mask):
        return int("".join(str(int(char == "X")) for char in mask), 2)

    return and_mask(mask), or_mask(mask), floating_mask(mask)


def apply_mask(value, and_mask, or_mask):
    return value & and_mask | or_mask


def run_program_1(program):
    masks = None
    memory = {}
    for instruction in program:
        if instruction.type == "mask":
            and_mask, or_mask, _ = convert_mask(instruction.value)
            masks = and_mask, or_mask
        if instruction.type == "mem":
            memory[instruction.address] = apply_mask(instruction.value, *masks)
    return memory


def run_program_2(program):
    masks = None
    memory = {}
    for instruction in program:
        if instruction.type == "mask":
            _, or_mask, floating_mask = convert_mask(instruction.value)
            possible_or_masks = tuple(gen_possible_or_masks(floating_mask))
            masks = or_mask, floating_mask, possible_or_masks

        if instruction.type == "mem":
            for address in gen_mem_addresses(instruction.address, *masks):
                memory[address] = instruction.value
    return memory


def gen_mem_addresses(address, or_mask, floating_mask, possible_or_masks):
    address &= ~floating_mask
    address |= or_mask
    for mask in possible_or_masks:
        yield address | mask


def solve_part_one(program):
    return sum(run_program_1(program).values())


def solve_part_two(program):
    return sum(run_program_2(program).values())


if __name__ == "__main__":
    program = read_input()
    solution_1 = solve_part_one(program)
    assert solution_1 == 8570568288597
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(program)
    assert solution_2 == 3289441921203
    print(f"The solution to part 2 is '{solution_2}'.")
