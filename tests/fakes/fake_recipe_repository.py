from backend.domain.recipe import Recipe, NewRecipe
from uuid import UUID, uuid4


class FakeRecipeRepository:
    def __init__(self, recipes: list[Recipe] | None = None):
        self._data = {r.id: r for r in (recipes or [])}

    def list_recipes(self) -> list[Recipe]:
        return list(self._data.values())

    def find_by_id(self, recipe_id: UUID) -> Recipe | None:
        return self._data.get(recipe_id)

    def add_recipe(self, new_recipe: NewRecipe) -> Recipe:
        if new_recipe in self._data.values():
            raise ValueError("Recipe already exists")
        recipe = Recipe(
            id= uuid4(),
            name= new_recipe.name,
            description= new_recipe.description,
            cooking_time= new_recipe.cooking_time,
            number_meals= new_recipe.number_meals
        )
        self._data[recipe.id] = recipe
        return recipe

    def update_recipe(self, recipe: Recipe) -> None:
        if recipe.id not in self._data:
            raise ValueError("Recipe not found")
        self._data[recipe.id] = recipe

    def delete_recipe(self, recipe_id: UUID) -> None:
        if recipe_id not in self._data:
            raise ValueError("Recipe not found")
        del self._data[recipe_id]

class FailingRecipeRepository(FakeRecipeRepository):
    def __init__(self, recipes: list[Recipe] | None = None):
        self._data = {r.id: r for r in (recipes or [])}

    def list_recipes(self) -> list[Recipe]:
        raise RuntimeError("Simulated repository failure")

    def find_by_id(self, recipe_id: UUID) -> Recipe | None:
        raise RuntimeError("Simulated repository failure")

    def add_recipe(self, new_recipe: NewRecipe) -> Recipe:
        raise RuntimeError("Simulated repository failure")

    def update_recipe(self, recipe: Recipe) -> None:
        raise RuntimeError("Simulated repository failure")

    def delete_recipe(self, recipe_id: UUID) -> None:
        raise RuntimeError("Simulated repository failure")
