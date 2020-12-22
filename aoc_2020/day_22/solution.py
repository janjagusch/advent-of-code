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

# ## Part 1

from collections import deque
from copy import copy
from itertools import count
from typing import List


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

assert solution_1 == 32598

print(f"The solution to part 1 is '{solution_1}'.")

# ## Part 2

# Using a list is more useful here.

deck1, deck2 = read_decks("./input.txt")
deck1 = list(gen_cards(deck1, bottom_up=False))
deck2 = list(gen_cards(deck2, bottom_up=False))


def score(deck: List) -> int:
    """
    This does not empty the deck.
    """
    return sum(
        card * multiplier for card, multiplier in zip(deck[::-1], count(start=1))
    )


def play_game(deck1, deck2):
    decks = deck1, deck2
    previous_rounds = set()
    while not is_finished(deck1, deck2):
        # if there was a previous round in this
        # game that had exactly the same cards
        # in the same order in the same players' decks,
        # the game instantly ends in a win for player 1
        memory = (tuple(deck1), tuple(deck2))
        if memory in previous_rounds:
            winner = 0
            return winner, None
        previous_rounds.add(memory)
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        cards = card1, card2
        # If both players have at least as many cards
        # remaining in their deck as the value of the card they just drew,
        # the winner of the round is determined by
        # playing a new game of Recursive Combat
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner, _ = play_game(copy(deck1[:card1]), copy(deck2[:card2]))
        elif card1 > card2:
            winner = 0
        # cannot draw
        else:
            winner = 1
        looser = 0 if winner else 1
        decks[winner].append(cards[winner])
        decks[winner].append(cards[looser])
    winner = 0 if len(deck1) else 1
    return winner, (deck1, deck2)


def solve_part_two(deck1, deck2):
    winner, decks = play_game(deck1, deck2)
    return score(decks[winner])


solution_2 = solve_part_two(deck1, deck2)

assert solution_2 == 35836

print(f"The solution to part 2 is '{solution_2}'.")
