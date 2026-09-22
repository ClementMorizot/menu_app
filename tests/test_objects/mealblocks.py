from . import recipes
from backend.domain.recipe import Recipe
from backend.domain.mealblock import MealBlock


# Mealblock factory
def mealblock_from_recipe(recipe: Recipe) -> MealBlock:
    return MealBlock(recipe, recipe.number_meals)


# Standard mealblocks
def length_1_mealblock() -> MealBlock:
    recipe = recipes.one_meal_recipe()
    return mealblock_from_recipe(recipe)


def length_2_mealblock() -> MealBlock:
    recipe = recipes.two_meals_recipe()
    return mealblock_from_recipe(recipe)


def length_3_mealblock() -> MealBlock:
    recipe = recipes.three_meals_recipe()
    return mealblock_from_recipe(recipe)


def length_1_mealblock_2() -> MealBlock:
    recipe = recipes.one_meal_recipe_2()
    return mealblock_from_recipe(recipe)


def length_1_mealblock_3() -> MealBlock:
    recipe = recipes.one_meal_recipe_3()
    return mealblock_from_recipe(recipe)


def length_1_mealblock_4() -> MealBlock:
    recipe = recipes.one_meal_recipe_4()
    return mealblock_from_recipe(recipe)


def length_2_mealblock_2() -> MealBlock:
    recipe = recipes.two_meals_recipe_2()
    return mealblock_from_recipe(recipe)


def length_2_mealblock_3() -> MealBlock:
    recipe = recipes.two_meals_recipe_3()
    return mealblock_from_recipe(recipe)


def length_2_mealblock_4() -> MealBlock:
    recipe = recipes.two_meals_recipe_4()
    return mealblock_from_recipe(recipe)


def length_3_mealblock_2() -> MealBlock:
    recipe = recipes.three_meals_recipe_2()
    return mealblock_from_recipe(recipe)


# Limit testing mealblocks
def minimum_length_mealblock() -> MealBlock:
    recipe = recipes.one_meal_recipe_2()
    return mealblock_from_recipe(recipe)


def maximum_length_mealblock() -> MealBlock:
    recipe = recipes.maximum_meals_recipe()
    return mealblock_from_recipe(recipe)


# Unusable mealblocks
def too_long_mealblock() -> MealBlock:
    recipe = recipes.too_many_meals_recipe()
    return mealblock_from_recipe(recipe)


def zero_length_mealblock() -> MealBlock:
    recipe = recipes.zero_meal_recipe()
    return mealblock_from_recipe(recipe)


def negative_length_mealblock() -> MealBlock:
    recipe = recipes.negative_meal_recipe()
    return mealblock_from_recipe(recipe)
