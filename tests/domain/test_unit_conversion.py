import pytest
from tests.test_objects import recipe_ingredients, ingredients
from backend.domain.units import Unit
from backend.domain.measured_ingredients import RecipeIngredient
from backend.domain import unit_conversion
from decimal import Decimal


@pytest.mark.parametrize("unit, quantity, expected_unit, expected_quantity",
[
    (Unit.g, Decimal("1"), Unit.g, Decimal("1")),
    (Unit.mL, Decimal("1"), Unit.mL, Decimal("1")),
    (Unit.teaspoon, Decimal("1"), Unit.teaspoon, Decimal("1")),
    (Unit.bunch, Decimal("1"), Unit.bunch, Decimal("1")),
    (Unit.pack, Decimal("1"), Unit.pack, Decimal("1")),
    (Unit.unit, Decimal("1"), Unit.unit, Decimal("1"))
])
def test_normalize_recipe_ingredient_with_standard_units(unit, quantity, expected_unit, expected_quantity):
    recipe_ingredient = recipe_ingredients.recipe_ingredient_with_standard_unit(unit, quantity)

    normalized_recipe_ingredient = unit_conversion.normalize_recipe_ingredient(recipe_ingredient)

    assert isinstance(normalized_recipe_ingredient, RecipeIngredient)
    assert normalized_recipe_ingredient.unit == expected_unit
    assert normalized_recipe_ingredient.quantity == expected_quantity

@pytest.mark.parametrize(
    "recipe_ingredient, expected_unit, expected_quantity",
    [
        (recipe_ingredients.pasta_in_kg(Decimal("1")), Unit.g, Decimal("1000")),
        (recipe_ingredients.pasta_in_mg(Decimal("500")), Unit.g, Decimal("0.5")),
        (recipe_ingredients.cream_in_cL(Decimal("50")), Unit.mL, Decimal("500")),
        (recipe_ingredients.cream_in_L(Decimal("1")), Unit.mL, Decimal("1000")),
        (recipe_ingredients.sugar_in_tablespoon(Decimal("2")), Unit.teaspoon, Decimal("6")),
    ],
)
def test_normalize_recipe_ingredient_converts_compatible_units(recipe_ingredient, expected_unit, expected_quantity):
    normalized = unit_conversion.normalize_recipe_ingredient(recipe_ingredient)

    assert normalized.unit == expected_unit
    assert normalized.quantity == expected_quantity

def test_normalize_incompatible_unit_recipe_ingredient():
    recipe_ingredient = recipe_ingredients.incompatible_unit_recipe_ingredient()

    with pytest.raises(ValueError):
        unit_conversion.normalize_recipe_ingredient(recipe_ingredient)


def test_normalize_recipe_ingredient_raises_error_for_ingredient_with_non_standard_unit():
    recipe_ingredient = RecipeIngredient(
         ingredients.ingredient_with_standard_unit(Unit.kg),
         Unit.kg,
         Decimal("1")
    )

    with pytest.raises(ValueError):
        unit_conversion.normalize_recipe_ingredient(recipe_ingredient)