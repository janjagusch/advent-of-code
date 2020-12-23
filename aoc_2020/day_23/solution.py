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

from itertools import count, islice

CUP_LABELLING = "389125467"


def process_cup_labelling(cup_labelling):
    return [int(val) - 1 for val in cup_labelling]


def wrapped_indexing(iterable, start, end):
    actual_end = end % len(iterable)
    if actual_end <= start:
        return iterable[start:] + iterable[:actual_end]
    return iterable[start:actual_end]


circle = process_cup_labelling(CUP_LABELLING)


# +
def gen_current_position(cup_len):
    for i in count():
        yield i % cup_len
        
        
def pick_up(circle, current_index, n_pick_ups):
    """
    The crab picks up the three cups that are immediately
    clockwise of the current cup. They are removed from the circle.
    """
    pick_ups = wrapped_indexing(circle, current_index, current_index + n_pick_ups)
    circle = [val for val in circle if val not in pick_ups]
    return circle, pick_ups   
    
        
def find_destination(current, possible_cups, cup_len):
    """
    The crab selects a destination cup: the cup with a label equal
    to the current cup's label minus one. If this would select 
    ne of the cups that was just picked up, the crab will keep
    subtracting one until it finds a cup that wasn't just picked up.
    If at any point in this process the value goes below the lowest
    value on any cup's label, it wraps around to the highest value
    on any cup's label instead.
    """
    for i in range(1, cup_len):
        destination = (current - i) % cup_len
        if destination in possible_cups:
            return destination
    raise ValueError(current, cup_len, possible_cup)
    
def place_cups(circle, pick_ups, destination_index):
    """
    The crab places the cups it just picked up so that they are
    immediately clockwise of the destination cup.
    They keep the same order as when they were picked up.
    
    Alters circle inplace!
    """
    circle[destination_index:destination_index] = pick_ups

def reorder_circle(circle, current, current_index):
    """
    Current needs to stay at current_index.
    """
    start_index = circle.index(current) - current_index
    return circle[start_index:] + circle[:start_index]


def relabel_cups(circle):
    return [label + 1 for label in circle]


# -

def play_game(circle, n_pick_ups=3):
    circle = list(val for val in circle)
    circle_len = len(circle)
    for current_index in gen_current_position(circle_len):
        # print(circle)
        # print(f"cups: {' '.join(str(val) for val in circle)}")
        current = circle[current_index]
        circle, pick_ups = pick_up(circle, current_index + 1, n_pick_ups)
        # print(f"current: {current}")
        # print(f"pick up: {pick_ups}")
        destination = find_destination(current, circle, circle_len)
        # print(f"destination: {destination}")
        destination_index = circle.index(destination)
        # print(f"sub circle: {circle}")
        place_cups(circle, pick_ups, destination_index + 1)
        # print(f"new circle: {circle}")
        circle = reorder_circle(circle, current, current_index)
        # print("")
        yield circle


def solve_part_one(circle):
    circle = tuple(islice(play_game(circle), 100))[-1]
    circle = relabel_cups(circle)
    start_index = circle.index(1)
    circle = (circle[start_index:] + circle[:start_index])[1:]
    return "".join(str(val) for val in circle)


solution_1 = solve_part_one(circle)

assert solution_1 == "67384529"
