from backend.domain.recipe import Recipe
from uuid import UUID


class FakeRecipeRepository:
    def __init__(self, recettes: list[Recipe] | None = None):
        self._data = {r.id: r for r in (recettes or [])}

    def list_recipes(self) -> list[Recipe]:
        return list(self._data.values())

    def find_by_id(self, recette_id: UUID) -> Recipe | None:
        return self._data.get(recette_id)

    def add_recipe(self, recette: Recipe) -> Recipe:
        if recette.id in self._data:
            raise ValueError("Recipe already exists")
        self._data[recette.id] = recette
        return recette

    def update_recipe(self, recette: Recipe) -> None:
        if recette.id not in self._data:
            raise KeyError("Recipe not found")
        self._data[recette.id] = recette

    def delete_recipe(self, recette_id: UUID) -> None:
        if recette_id not in self._data:
            raise KeyError("Recipe not found")
        del self._data[recette_id]
