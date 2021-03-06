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

# # Day 23

# ## Day 1

from array import array
from itertools import count, islice
from math import prod
from typing import Iterable


# +
class LinkedNode:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node

    def __repr__(self):
        return f"{self.__class__.__name__}(data={self.data})"

    def gen_next_n_nodes(self, n):
        node = self.next_node
        yield node
        for _ in range(1, n):
            node = node.next_node
            if not node:
                raise IndexError(n)
            yield node


class LinkedList:
    """
    A linked list with O(1) lookup for individual nodes.
    Loops between the last and the first node.
    """

    def __init__(self, nodes):
        self._head = nodes[0]
        self._nodes_map = {node.data: node for node in nodes}
        for node, next_node in zip(nodes[:-1], nodes[1:]):
            node.next_node = next_node
        nodes[-1].next_node = nodes[0]

    def __getitem__(self, index) -> LinkedNode:
        return self._nodes_map[index]

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node
            node = node.next_node

    def __len__(self):
        return len(self._nodes_map)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"

    def __str__(self):
        return "".join([str(node.data) for node in self.data])


# -

CUP_LABELLING = "368195742"

nodes = tuple(LinkedNode(int(val) - 1) for val in CUP_LABELLING)
cups = LinkedList(nodes)


def find_destination(
    current: LinkedNode, pick_ups: Iterable[LinkedNode], cups: LinkedList
) -> LinkedNode:
    """
    The crab selects a destination cup: the cup with a label equal
    to the current cup's label minus one. If this would select
    ne of the cups that was just picked up, the crab will keep
    subtracting one until it finds a cup that wasn't just picked up.
    If at any point in this process the value goes below the lowest
    value on any cup's label, it wraps around to the highest value
    on any cup's label instead.
    """
    for i in range(1, len(cups)):
        destination = cups[(current.data - i) % len(cups)]
        if destination not in pick_ups:
            return destination
    raise ValueError(current, pick_ups)


def play_game(cups, n_pick_ups=3):
    for current in cups:
        pick_ups = tuple(current.gen_next_n_nodes(n_pick_ups))
        destination = find_destination(current, pick_ups, cups)
        current.next_node = pick_ups[-1].next_node
        pick_ups[-1].next_node = destination.next_node
        destination.next_node = pick_ups[0]
        yield cups


def solve_part_one(cups):
    cups = tuple(islice(play_game(cups), 100))[0]
    return "".join(str(val.data + 1) for val in cups[0].gen_next_n_nodes(8))


solution_1 = solve_part_one(cups)

assert solution_1 == "95648732"

print(f"The solution to part 1 is '{solution_1}'.")

# ## Part 2

nodes = tuple(LinkedNode(int(val) - 1) for val in CUP_LABELLING)
nodes += tuple(
    (LinkedNode(val) for val in range(max(node.data for node in nodes) + 1, 1_000_000))
)
cups = LinkedList(nodes)


def solve_part_two(cups):
    cups = tuple(islice(play_game(cups), 10_000_000))[0]
    return prod(node.data + 1 for node in cups[0].gen_next_n_nodes(2))


solution_2 = solve_part_two(cups)

assert solution_2 == 192515314252

print(f"The solution to part 2 is '{solution_2}'.")
