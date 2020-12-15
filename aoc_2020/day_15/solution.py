"""

"""

from itertools import count, islice
from operator import sub


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(int(val) for val in file_pointer.read().split(","))


def store_in_memory(memory, num, turn):
    memory_cell = memory.get(num)
    if not memory_cell:
        memory_cell = (None, turn)
    else:
        memory_cell = (memory_cell[1], turn)
    memory[num] = memory_cell


def calc_num(memory, num):
    try:
        return -sub(*memory[num])
    except TypeError:
        return 0
    except KeyError:
        return num


def play_game(numbers):
    memory = {}
    last_number = None
    turn = count(start=1)
    for num in numbers:
        last_number = calc_num(memory, num)
        store_in_memory(memory, last_number, next(turn))
        yield last_number
    while True:
        last_number = calc_num(memory, last_number)
        store_in_memory(memory, last_number, next(turn))
        yield last_number


def solve_part_one(numbers):
    return tuple(islice(play_game(numbers), 2020))[-1]


if __name__ == "__main__":
    numbers = read_input()
    solution_1 = solve_part_one(numbers)
    assert solution_1 == 249
    print(f"The solution to part 1 is '{solve_part_one(numbers)}'.")
