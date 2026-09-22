from . import ingredients
from backend.domain.units import Unit
from backend.domain.measured_ingredients import RecipeIngredient
from decimal import Decimal

def recipe_ingredient_with_standard_unit(unit: Unit, quantity: Decimal, name="Test ingredient") -> RecipeIngredient:
    ingredient = ingredients.ingredient_with_standard_unit(unit, name)
    return RecipeIngredient(
        ingredient= ingredient,
        unit= unit,
        quantity= quantity
    )

def recipe_ingredient_with_convertible_unit():
    return RecipeIngredient(
        ingredient= ingredients.pasta(),
        unit= Unit.kg,
        quantity = Decimal("1")
    )

def incompatible_unit_recipe_ingredient():
    return RecipeIngredient(
        ingredient= ingredients.cream(),
        unit= Unit.g,
        quantity = Decimal("150")
    )

def zero_quantity_recipe_ingredient():
    return RecipeIngredient(
        ingredient= ingredients.garlic(),
        unit= Unit.unit,
        quantity = Decimal("0")
    )

def pasta_in_kg(quantity: Decimal):
    return RecipeIngredient(
        ingredients.pasta(),
        Unit.kg,
        quantity
    )

def pasta_in_mg(quantity: Decimal):
    return RecipeIngredient(
        ingredients.pasta(),
        Unit.mg,
        quantity
    )

def cream_in_cL(quantity: Decimal):
    return RecipeIngredient(
        ingredients.cream(),
        Unit.cL,
        quantity
    )

def cream_in_L(quantity: Decimal):
    return RecipeIngredient(
        ingredients.cream(),
        Unit.L,
        quantity
    )

def sugar_in_tablespoon(quantity: Decimal):
    return RecipeIngredient(
        ingredients.sugar(),
        Unit.tablespoon,
        quantity
    )