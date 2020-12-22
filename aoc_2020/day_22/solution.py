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

# # Day 22

# ## Part 2

from collections import deque
from itertools import count


# +
def create_queue(items, maxsize=None):
    maxsize = maxsize or len(items)
    queue = deque(maxlen=maxsize)
    for item in items:
        queue.append(item)
    return queue


def process_deck(raw_deck):
    """
    Player 2:
    5
    8
    4
    7
    10
    """
    cards = tuple(int(val) for val in raw_deck.strip().split("\n")[1:])
    queue = create_queue(cards, len(cards) * 2)
    return queue


def read_decks(file_path):
    with open(file_path, mode="r") as file_pointer:
        return tuple(
            process_deck(raw_deck)
            for raw_deck in file_pointer.read().strip().split("\n\n")
        )


# -

deck1, deck2 = read_decks("./input.txt")


# +
def gen_cards(deck, bottom_up=True):
    """
    Empties the deck!
    """
    func = deck.pop if bottom_up else deck.popleft
    while True:
        try:
            yield func()
        except IndexError:
            return


def score(deck):
    """
    Empties the deck!
    """
    return sum(
        card * multiplier
        for card, multiplier in zip(gen_cards(deck, bottom_up=True), count(start=1))
    )


# +
def is_finished(deck1, deck2):
    return not len(deck1) or not len(deck2)


def play_game(deck1, deck2):
    while not is_finished(deck1, deck2):
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    return score(deck1), score(deck2)


# -


def solve_part_one(deck1, deck2):
    return max(play_game(deck1, deck2))


solution_1 = solve_part_one(deck1, deck2)

solution_1

assert solution_1 == 32598
