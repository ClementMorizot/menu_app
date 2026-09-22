from backend.domain.measured_ingredients import RecipeIngredient
from uuid import UUID

class FakeRecipeIngredientRepository:
    def __init__(self, recipe_ingredients : dict[UUID, tuple[RecipeIngredient,...]] | None = None ) -> None:
        self._data = {
            recipe_id : list(items)
            for recipe_id, items in (recipe_ingredients or {}).items()
        }

    def get_ingredients_of_recipe(self, recipe_id: UUID) -> list[RecipeIngredient]:
        return list(self._data.get(recipe_id,[]))

    def add_recipe_ingredient(self, recipe_id: UUID, recipe_ingredient: RecipeIngredient,) -> None:
        if recipe_id not in self._data:
            self._data[recipe_id] = list()
        for recipe_ingredient_data in self._data[recipe_id]:
            if recipe_ingredient_data.ingredient.id == recipe_ingredient.ingredient.id:
                raise ValueError(
                    f"Duplicate ingredient {recipe_ingredient.ingredient.id}"
                    f"in recipe {recipe_id}"
                    )
        self._data[recipe_id].append(recipe_ingredient)

    def update_recipe_ingredients(self, recipe_id: UUID, recipe_ingredients: list[RecipeIngredient]) -> None:
        self._data[recipe_id] = list(recipe_ingredients)

    def delete_recipe_ingredient(self, recipe_id: UUID, ingredient_id: UUID) -> None:
        if recipe_id not in self._data:
            raise ValueError(f"Ingredient {ingredient_id} not in recipe {recipe_id}")
        if ingredient_id not in [recipe_ingredient.ingredient.id for recipe_ingredient in self._data[recipe_id]]:
            raise ValueError(f"Ingredient {ingredient_id} not in recipe {recipe_id}")
        self._data[recipe_id] = [
            recipe_ingredient
            for recipe_ingredient in self._data[recipe_id]
            if recipe_ingredient.ingredient.id != ingredient_id
        ]

    def delete_all_recipe_ingredients_for_recipe(self, recipe_id: UUID) -> None:
        self._data.pop(recipe_id, None)

class FailingRecipeIngredientRepository(FakeRecipeIngredientRepository):
    def __init__(self, recipe_ingredients : dict[UUID, tuple[RecipeIngredient,...]] | None = None ) -> None:
        self._data = {
            recipe_id : list(items)
            for recipe_id, items in (recipe_ingredients or {}).items()
        }

    def get_ingredients_of_recipe(self, recipe_id: UUID) -> list[RecipeIngredient]:
        raise RuntimeError("Simulated repository failure")

    def add_recipe_ingredient(self, recipe_id: UUID, recipe_ingredient: RecipeIngredient,) -> None:
        raise RuntimeError("Simulated repository failure")

    def update_recipe_ingredients(self, recipe_id: UUID, recipe_ingredients: list[RecipeIngredient]) -> None:
        raise RuntimeError("Simulated repository failure")

    def delete_recipe_ingredient(self, recipe_id: UUID, ingredient_id: UUID) -> None:
        raise RuntimeError("Simulated repository failure")

    def delete_all_recipe_ingredients_for_recipe(self, recipe_id: UUID) -> None:
        raise RuntimeError("Simulated repository failure")