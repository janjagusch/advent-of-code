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

# # Day 21

# ## Part 1

from collections import namedtuple
from copy import copy
from itertools import islice, product

Food = namedtuple("Food", ["ingredients", "allergens"])


def process_raw_food(raw_food):
    """
    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    """
    ingredients, allergens = raw_food.split("(contains")
    ingredients = set(ingredients.strip().split())
    allergens = set(allergens[:-1].strip().replace(",", "").split())
    return Food(ingredients, allergens)


def read_foods(file_path):
    with open(file_path, mode="r") as file_pointer:
        return tuple(
            process_raw_food(raw_food)
            for raw_food in file_pointer.read().split("\n")
            if raw_food
        )


foods = read_foods("./input.txt")


# +
def calc_ingredient_intersection(foods, allergen, ingredients):
    for food in foods:
        if allergen in food.allergens:
            ingredients = ingredients.intersection(food.ingredients)
    return ingredients


def gen_possibilities(foods, allergens, ingredients):
    return {
        allergen: calc_ingredient_intersection(foods, allergen, ingredients)
        for allergen in allergens
    }


def find_easiest_to_solve(possibilities):
    return min(possibilities, key=lambda allergen: len(possibilities[allergen]))


def is_complete(allergens):
    return not allergens


def is_broken(ingredients, allergens):
    return ingredients and not allergens


# -


def search_allergen_ingredients(foods, ingredients, allergens, allergen_ingredients):
    if is_complete(allergens):
        yield allergen_ingredients
        return
    if is_broken(ingredients, allergens):
        return
    possibilities = gen_possibilities(foods, allergens, ingredients)
    allergen = find_easiest_to_solve(possibilities)
    for ingredient in possibilities[allergen]:
        new_allergen_ingredients = {**allergen_ingredients, allergen: ingredient}
        new_foods = tuple(
            Food(
                set(filter(lambda x: x != ingredient, food.ingredients)),
                set(filter(lambda x: x != allergen, food.allergens)),
            )
            for food in foods
        )
        new_allergens = copy(allergens)
        new_allergens.remove(allergen)
        new_ingredients = copy(ingredients)
        new_ingredients.remove(ingredient)
        for solution in search_allergen_ingredients(
            new_foods, new_ingredients, new_allergens, new_allergen_ingredients
        ):
            yield solution


def solve_part_one(foods):
    allergens = set()
    for food in foods:
        allergens = allergens.union(food.allergens)

    ingredients = set()
    for food in foods:
        ingredients = ingredients.union(food.ingredients)
    allergen_ingredients = tuple(
        islice(search_allergen_ingredients(foods, ingredients, allergens, {}), 1)
    )[0]
    solution = sum(
        len(food.ingredients - set(allergen_ingredients.values())) for food in foods
    )
    return allergen_ingredients, solution


ingredient_allergens, solution_1 = solve_part_one(foods)

assert solution_1 == 1945

print(f"The solution to part is '{solution_1}'.")
