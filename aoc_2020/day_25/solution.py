# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: aoc-2020-20
#     language: python
#     name: aoc-2020-20
# ---

# # Day 25

# ## Part 1

# +
card_public_key = 5764801
door_public_key = 17807724

card_loop_size = 8
door_loop_size = 11

encryption_key = 14897079
# -

from itertools import count, islice


# +
def calc_possible_public_key(prev_possible_public_key, subject_number):
    """
    Then, perform the following steps:
        * Set the value to itself multiplied by the subject number.
        * Set the value to the remainder after dividing the value by 20201227.
    """
    return (prev_possible_public_key * subject_number) % 20201227

def gen_possible_public_keys(subject_number=7):
    """
    The handshake used by the card and the door involves
    an operation that transforms a subject number.
    To transform a subject number, start with the value 1.
    """
    possible_public_key = 1
    for secret_loop_size in count(start=1):
        yield (possible_public_key := calc_possible_public_key(possible_public_key, subject_number))


# -

assert tuple(islice(gen_possible_public_keys(), card_loop_size))[-1] == card_public_key
assert tuple(islice(gen_possible_public_keys(), door_loop_size))[-1] == door_public_key

assert tuple(islice(gen_possible_public_keys(card_public_key), door_loop_size))[-1] == encryption_key
assert tuple(islice(gen_possible_public_keys(door_public_key), card_loop_size))[-1] == encryption_key


