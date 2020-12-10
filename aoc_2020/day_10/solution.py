"""
Solution to https://adventofcode.com/2020/day/10
"""

from collections import Counter


def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(sorted(int(line.strip()) for line in file_pointer.readlines()))


def add_first_and_last_adapter(adapters):
    outlet = 0
    device = max(adapters) + 3
    return tuple([outlet, *adapters, device])


def gen_jolt_difference(adapters):
    for jolt_in, jolt_out in zip(adapters[:-1], adapters[1:]):
        yield jolt_out - jolt_in


def solve_part_one(adapters):
    counter = Counter(gen_jolt_difference(add_first_and_last_adapter(adapters)))
    return counter[1] * counter[3]


def calc_compat_map(adapters):
    return {
        adapter: tuple(
            sorted(
                compat_adapter
                for compat_adapter in adapters
                if compat_adapter > adapter and compat_adapter <= adapter + 3
            )
        )
        for adapter in adapters
    }


def calc_solved_map(compat_map, i_compat_map, solved_map, solved_tuple):
    solved_key, solved_value = solved_tuple
    solved_map[solved_key] = solved_value
    for possibly_solved_key in i_compat_map[solved_key]:
        if possibly_solved_key not in solved_map and all(
            k in solved_map for k in compat_map[possibly_solved_key]
        ):
            calc_solved_map(
                compat_map,
                i_compat_map,
                solved_map,
                (
                    possibly_solved_key,
                    sum(solved_map[k] for k in compat_map[possibly_solved_key]),
                ),
            )
    return solved_map


def solve_part_two(adapters):
    compat_map = calc_compat_map(add_first_and_last_adapter(adapters))
    i_compat_map = {
        i_key: set(key for key, val in compat_map.items() if i_key in val)
        for i_key in compat_map
    }
    return calc_solved_map(compat_map, i_compat_map, {}, (max(adapters), 1))[0]


if __name__ == "__main__":
    adapters = read_input()
    solution_1 = solve_part_one(adapters)
    assert solution_1 == 2030
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(adapters)
    assert solution_2 == 42313823813632
    print(f"The solution to part 2 is '{solution_2}'.")
