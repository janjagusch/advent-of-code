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

from collections import namedtuple
from itertools import count, islice

# +
card_public_key = 5764801
door_public_key = 17807724

card_loop_size = 8
door_loop_size = 11

encryption_key = 14897079
# -

Transformation = namedtuple("Transformation", ("loop_size", "value"))


# +
def transform(value, subject_number):
    """
    Then, perform the following steps:
        * Set the value to itself multiplied by the subject number.
        * Set the value to the remainder after dividing the value by 20201227.
    """
    return (value * subject_number) % 20201227


def gen_transformations(subject_number=7, value=1):
    """
    The handshake used by the card and the door involves
    an operation that transforms a subject number.
    To transform a subject number, start with the value 1.
    """
    for loop_size in count(start=1):
        yield Transformation(loop_size, (value := transform(value, subject_number)))


def calc_encryption_key(subject_number, loop_size):
    return tuple(islice(gen_transformations(subject_number), loop_size))[-1].value


# -

assert tuple(islice(gen_transformations(), card_loop_size))[-1].value == card_public_key
assert tuple(islice(gen_transformations(), door_loop_size))[-1].value == door_public_key

assert calc_encryption_key(card_public_key, door_loop_size) == calc_encryption_key(
    door_public_key, card_loop_size
)


# ## Not Knowing Loop Size

# You can use either device's loop size with the other device's public key to calculate the encryption key.


def find_loop_size(transformation_value, subject_number=7, value=1):
    for transformation in gen_transformations(subject_number, value):
        if transformation.value == transformation_value:
            return transformation.loop_size


assert find_loop_size(card_public_key) == card_loop_size
assert find_loop_size(door_public_key) == door_loop_size

card_public_key = 11404017
door_public_key = 13768789

card_loop_size = find_loop_size(card_public_key)
door_loop_size = find_loop_size(door_public_key)

encryption_key = calc_encryption_key(card_public_key, door_loop_size)

assert encryption_key == calc_encryption_key(door_public_key, card_loop_size)

print(f"The solution to part 1 is '{encryption_key}'.")
