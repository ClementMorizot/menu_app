from backend.domain.units import Unit
from decimal import Decimal
from backend.domain.measured_ingredients import RecipeIngredient

UNIT_CONVERSION_TO_STANDARD  = {
    Unit.g: {
        Unit.mg: Decimal("0.001"),
        Unit.g: Decimal("1"),
        Unit.kg: Decimal("1000")
    },
    Unit.mL: {
        Unit.mL: Decimal("1"),
        Unit.cL: Decimal("10"),
        Unit.L: Decimal("1000")
    },
    Unit.teaspoon: {
        Unit.teaspoon: Decimal("1"),
        Unit.tablespoon: Decimal("3")
    },
    Unit.bunch: {
        Unit.bunch: Decimal("1")
    },
    Unit.pack: {
        Unit.pack: Decimal("1")
    },
    Unit.unit: {
        Unit.unit: Decimal("1")
    }
}

STANDARD_UNITS = [
    Unit.g,
    Unit.mL,
    Unit.teaspoon,
    Unit.bunch,
    Unit.pack,
    Unit.unit,
]

def normalize_recipe_ingredient(recipe_ingredient : RecipeIngredient) -> RecipeIngredient:

    standard_unit = recipe_ingredient.ingredient.standard_unit
    compatible_units = UNIT_CONVERSION_TO_STANDARD.get(standard_unit)

    if compatible_units is None:
        raise ValueError(
    f"Unit {recipe_ingredient.unit} is not compatible with "
    f"standard unit {standard_unit} for ingredient {recipe_ingredient.ingredient.id}"
)

    factor = compatible_units.get(recipe_ingredient.unit)

    if factor is None:
        raise ValueError("Unexpected unit in recipe")

    quantity = recipe_ingredient.quantity * factor

    return RecipeIngredient(
        ingredient= recipe_ingredient.ingredient,
        unit= recipe_ingredient.ingredient.standard_unit,
        quantity= quantity)
