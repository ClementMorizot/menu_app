from typing import Protocol
from backend.domain.repositories import RecipeRepository, IngredientRepository, RecipeIngredientRepository

class UnitOfWork(Protocol):
    recipes: RecipeRepository
    ingredients: IngredientRepository
    recipe_ingredients: RecipeIngredientRepository

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...