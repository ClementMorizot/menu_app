from backend.domain.ingredient import Ingredient
from backend.domain.units import Unit
from uuid import uuid4,UUID

def ingredient(name: str, unit: Unit) -> Ingredient:
    return Ingredient(
        id=uuid4(),
        name=name,
        standard_unit=unit
    )

def ingredient_with_standard_unit(unit: Unit, name: str = "Test ingredient") -> Ingredient:
    return ingredient(name, unit)

def pasta():
    return Ingredient(
        id= UUID("00000000-0000-0000-0001-000000000001"),
        name= "Pates",
        standard_unit= Unit.g)

def cream():
    return Ingredient(
        id= UUID("00000000-0000-0000-0001-000000000002"),
        name= "Crème fraiche",
        standard_unit= Unit.mL)

def garlic():
    return ingredient("Ail", Unit.unit)

def sugar():
    return ingredient("Sucre", Unit.teaspoon)