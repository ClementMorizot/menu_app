import pytest
from uuid import UUID
from backend.domain.shopping_list_generator import ShoppingListGenerator
from backend.domain.units import Unit
from tests.test_objects import menus, recipe_ingredients, ingredients
from tests.fakes.fake_recipe_ingredient_repository import FakeRecipeIngredientRepository
from backend.domain.measured_ingredients import RecipeIngredient, ShoppingListItem
from decimal import Decimal

_DATASET = {
    UUID("00000000-0000-0000-0000-000000000001"): ( #one_meal_recipe(name="Omelette")
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.unit,
            Decimal("2")
        ),
    ),
    UUID("00000000-0000-0000-0000-000000000003"): ( #two_meals_recipe(name="Lasagnes")
        recipe_ingredients.recipe_ingredient_with_convertible_unit(),
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.unit,
            Decimal("2")
        ),
        RecipeIngredient(
            ingredients.cream(),
            Unit.cL,
            Decimal("50")
        ),
    ),
    UUID("00000000-0000-0000-0000-000000000004"): ( #three_meals_recipe(name="Risotto")
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.g,
            Decimal("500")
        ),
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.g,
            Decimal("200")
        ),
    ),
    UUID("00000000-0000-0000-0000-000000000007"): ( #two_meals_recipe_2(name="Chilli con carne")
        RecipeIngredient(
            ingredients.cream(),
            Unit.mL,
            Decimal("250")
        ),
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.g,
            Decimal("300")
        ),
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.pack,
            Decimal("2")
        ),
        recipe_ingredients.recipe_ingredient_with_standard_unit(
            Unit.g,
            Decimal("500")
        ),
    ),
    UUID("00000000-0000-0000-0000-000000000010"): ( #three_meals_recipe_2(name="Couscous")
        RecipeIngredient(
            ingredients.cream(),
            Unit.mL,
            Decimal("250")
        ),
        RecipeIngredient(
            ingredients.pasta(),
            Unit.g,
            Decimal("500")
        ),
    )
}

def find_item_by_ingredient_id(
    shopping_list: list[ShoppingListItem],
    ingredient_id: UUID,
) -> ShoppingListItem:
    return next(
        item for item in shopping_list
        if item.ingredient.id == ingredient_id
    )

def test_generate_shopping_list_nominal_case():
    menu = menus.minimal_menu()
    repository = FakeRecipeIngredientRepository(_DATASET)
    generator = ShoppingListGenerator(repository)

    shopping_list = generator.generate_shopping_list(menu)

    target_item = ShoppingListItem(
        _DATASET[UUID("00000000-0000-0000-0000-000000000001")][0].ingredient,
        Unit.unit,
        Decimal("2")
    )
    assert all(isinstance(shopping_list_item, ShoppingListItem) for shopping_list_item in shopping_list)
    assert len(shopping_list) == 1
    assert target_item in shopping_list

def test_generate_shopping_list_with_multiple_recipes_and_recipe_ingredients_with_conversion():
    menu = menus.incomplete_stable_menu()
    repository = FakeRecipeIngredientRepository(_DATASET)
    generator = ShoppingListGenerator(repository)

    shopping_list = generator.generate_shopping_list(menu)

    pasta_item = find_item_by_ingredient_id(shopping_list, ingredients.pasta().id)
    cream_item = find_item_by_ingredient_id(shopping_list, ingredients.cream().id)
    assert all(isinstance(shopping_list_item, ShoppingListItem) for shopping_list_item in shopping_list)
    assert len(shopping_list) == 6
    assert pasta_item.unit == Unit.g
    assert pasta_item.quantity == Decimal("1000")
    assert cream_item.unit == Unit.mL
    assert cream_item.quantity == Decimal("500")

def test_generate_shopping_list_using_same_ingredient_multiple_times():
    menu = menus.menu_with_two_length_2_mealblock()
    repository = FakeRecipeIngredientRepository(_DATASET)
    generator = ShoppingListGenerator(repository)

    shopping_list = generator.generate_shopping_list(menu)

    cream_item = find_item_by_ingredient_id(shopping_list, ingredients.cream().id)
    assert all(isinstance(shopping_list_item, ShoppingListItem) for shopping_list_item in shopping_list)
    assert len(shopping_list) == 6 # 7 recipe_ingredients entries but 2 instances of cream()
    assert cream_item.unit == Unit.mL
    assert cream_item.quantity == Decimal("750")

def test_generate_shopping_list_for_unstable_menu():
    menu = menus.unstable_menu_with_incomplete_mealblock()
    repository = FakeRecipeIngredientRepository(_DATASET)
    generator = ShoppingListGenerator(repository)

    with pytest.raises(ValueError):
        generator.generate_shopping_list(menu)

def test_generate_shopping_list_with_recipe_having_no_declared_ingredients_raises_error():
    menu = menus.menu_with_no_associated_ingredients()
    repository = FakeRecipeIngredientRepository(_DATASET)
    generator = ShoppingListGenerator(repository)

    with pytest.raises(ValueError):
        generator.generate_shopping_list(menu)


def test_generate_shopping_list_generates_shopping_items_once_for_a_multiple_meals_mealblock_menu():
    menu = menus.menu_with_one_length_3_mealblock()
    repository = FakeRecipeIngredientRepository(_DATASET)
    generator = ShoppingListGenerator(repository)

    shopping_list = generator.generate_shopping_list(menu)

    cream_item = find_item_by_ingredient_id(shopping_list, ingredients.cream().id)
    pasta_item = find_item_by_ingredient_id(shopping_list, ingredients.pasta().id)

    assert cream_item.quantity == Decimal("250")
    assert pasta_item.quantity == Decimal("500")