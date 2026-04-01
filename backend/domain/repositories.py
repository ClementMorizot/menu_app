from typing import Protocol
from uuid import UUID

from .recette import Recette


class RecipeRepository(Protocol):

    def list_recipes(self) -> list[Recette]:
        ...

    def find_by_id(self, recette_id: UUID) -> Recette | None:
        ...

    def add_recipe(self, recette : Recette) -> Recette:
        ...

    def update_recipe(self, recette : Recette) -> None:
        ...

    def delete_recipe(self, recette_id: UUID) -> None:
        ...
