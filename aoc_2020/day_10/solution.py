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


def calc_compatibility_map(adapters):
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


def recur_solve(compat_map, i_compat_map, solve_map, solve_tuple):
    k, v = solve_tuple
    solve_map[k] = v
    for possible_solve_key in i_compat_map[k]:
        if possible_solve_key not in solve_map and all(
            kk in solve_map for kk in compat_map[possible_solve_key]
        ):
            recur_solve(
                compat_map,
                i_compat_map,
                solve_map,
                (
                    possible_solve_key,
                    sum(solve_map[kkk] for kkk in compat_map[possible_solve_key]),
                ),
            )
    return solve_map


def solve_part_two(adapters):
    compat_map = calc_compatibility_map(add_first_and_last_adapter(adapters))
    i_compat_map = {
        i_key: set(key for key, val in compat_map.items() if i_key in val)
        for i_key in compat_map
    }
    return recur_solve(compat_map, i_compat_map, {}, (max(adapters), 1))[0]


if __name__ == "__main__":
    adapters = read_input()
    solution_1 = solve_part_one(adapters)
    assert solution_1 == 2030
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(adapters)
    assert solution_2 == 42313823813632
    print(f"The solution to part 2 is '{solution_2}'.")
