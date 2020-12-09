"""
Solution to https://adventofcode.com/2020/day/9
"""

def read_input():
    with open("./input.txt", mode="r") as file_pointer:
        return tuple(int(line.strip()) for line in file_pointer.readlines())


def walk(encrypted_data, preamble=25):
    for pos, data_point in enumerate(encrypted_data[preamble:]):
        yield data_point, encrypted_data[pos:pos+preamble]


def gen_preable_pairs(preamble):
    return ((a, b) for b in preamble for a in preamble if a < b)


def solve_part_one(encrypted_data):
    for data_point, preamble in walk(encrypted_data):
        if not any(data_point == sum(preamble_pair) for preamble_pair in gen_preable_pairs(preamble)):
            return data_point


def gen_possible_weak_sets(encrypted_data):
    for set_len in range(2, len(encrypted_data)):
        for end_pos in range(set_len, len(encrypted_data)):
            yield encrypted_data[end_pos-set_len:end_pos]


def find_weak_set(encrypted_data, invalid_number):
    for possible_weak_set in gen_possible_weak_sets(encrypted_data):
        if sum(possible_weak_set) == invalid_number:
            return possible_weak_set
    raise RuntimeError

def solve_part_two(encrypted_data, invalid_number):
    weak_set = find_weak_set(encrypted_data, invalid_number)
    return min(weak_set) + max(weak_set)

if __name__ == "__main__":
    encrypted_data = read_input()
    solution_1 = solve_part_one(encrypted_data)
    assert solution_1 == 1124361034
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(encrypted_data, solution_1)
    assert solution_2 == 129444555
    print(f"The solution to part 2 is '{solution_2}'.")
