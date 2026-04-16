from uuid import uuid4
from backend.domain.recipe import Recipe


def make_recipe(
    id, name: str, description: str, cooking_time: int, number_meals: int
) -> Recipe:
    return Recipe(id, name, description, cooking_time, number_meals)


def one_meal_recipe(name="Omelette") -> Recipe:
    return Recipe(
        id=uuid4(),
        name=name,
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def one_meal_recipe_2() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Poelee",
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def two_meals_recipe(name="Lasagnes") -> Recipe:
    return Recipe(
        id=uuid4(),
        name=name,
        description="General description",
        cooking_time=1,
        number_meals=2,
    )


def three_meals_recipe(name="Risotto") -> Recipe:
    return Recipe(
        id=uuid4(),
        name=name,
        description="General description",
        cooking_time=1,
        number_meals=3,
    )


def one_meal_recipe_3() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Croque-monsieur",
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def one_meal_recipe_4() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Salade composee",
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def two_meals_recipe_2() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Chili con carne",
        description="General description",
        cooking_time=1,
        number_meals=2,
    )


def two_meals_recipe_3() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Hachis parmentier",
        description="General description",
        cooking_time=1,
        number_meals=2,
    )


def two_meals_recipe_4() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Curry de poulet",
        description="General description",
        cooking_time=1,
        number_meals=2,
    )


def three_meals_recipe_2() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Couscous",
        description="General description",
        cooking_time=1,
        number_meals=3,
    )


def three_meals_recipe_3() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Paella",
        description="General description",
        cooking_time=1,
        number_meals=3,
    )


def minimum_length_name_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="A",
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def maximum_meals_recipe(name="Plat familial XXL") -> Recipe:
    return Recipe(
        id=uuid4(),
        name=name,
        description="General description",
        cooking_time=1,
        number_meals=14,
    )


def long_name_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Gratin de pommes de terre au reblochon, oignons fondants et lardons fumes",
        description="General description",
        cooking_time=1,
        number_meals=2,
    )


def empty_name_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="",
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def blanc_name_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="   ",
        description="General description",
        cooking_time=1,
        number_meals=1,
    )


def zero_meal_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Soupe",
        description="General description",
        cooking_time=1,
        number_meals=0,
    )


def negative_meal_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Salade",
        description="General description",
        cooking_time=1,
        number_meals=-1,
    )


def too_many_meals_recipe(name="Grand banquet") -> Recipe:
    return Recipe(
        id=uuid4(),
        name=name,
        description="General description",
        cooking_time=1,
        number_meals=15,
    )
