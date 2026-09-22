from backend.domain.ingredient import Ingredient, NewIngredient
from uuid import UUID, uuid4


class FakeIngredientRepository:
    def __init__(self, ingredients: list[Ingredient] | None = None):
        self._data = {i.id: i for i in (ingredients or [])}

    def list_ingredients(self) -> list[Ingredient]:
        return list(self._data.values())

    def find_by_id(self, ingredient_id: UUID) -> Ingredient | None:
        return self._data.get(ingredient_id)

    def add_ingredient(self, new_ingredient: NewIngredient) -> Ingredient:
        if new_ingredient in self._data.values():
            raise ValueError("Ingredient already exists")
        ingredient = Ingredient(
            id= uuid4(),
            name= new_ingredient.name,
            standard_unit= new_ingredient.standard_unit
        )
        self._data[ingredient.id] = ingredient
        return ingredient

    def update_ingredient(self, ingredient: Ingredient) -> None:
        if ingredient.id not in self._data:
            raise ValueError("Ingredient not found")
        self._data[ingredient.id] = ingredient

    def delete_ingredient(self, ingredient_id: UUID) -> None:
        if ingredient_id not in self._data:
            raise ValueError("Ingredient not found")
        del self._data[ingredient_id]