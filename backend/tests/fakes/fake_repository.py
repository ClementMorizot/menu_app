from domain.recette import Recette
from uuid import UUID

class FakeRecipeRepository:

    def __init__(self, recettes: list[Recette] | None = None):
        self._data = {r.id: r for r in (recettes or [])}

    def list_recipes(self) -> list[Recette]:
        return list(self._data.values())

    def find_by_id(self, recette_id: UUID) -> Recette | None:
        return self._data.get(recette_id)

    def add_recipe(self, recette: Recette) -> None:
        if recette.id in self._data:
            raise ValueError("Recette already exists")
        self._data[recette.id] = recette

    def update_recipe(self, recette: Recette) -> None:
        if recette.id not in self._data:
            raise KeyError("Recette not found")
        self._data[recette.id] = recette

    def delete_recipe(self, recette_id: UUID) -> None:
        if recette_id not in self._data:
            raise KeyError("Recette not found")
        del self._data[recette_id]