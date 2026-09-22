from backend.application.unit_of_work import UnitOfWork
from backend.domain.repositories import (
    RecipeRepository,
    IngredientRepository,
    RecipeIngredientRepository,
)


class FakeUnitOfWork(UnitOfWork):
    def __init__(
        self,
        recipes: RecipeRepository,
        ingredients: IngredientRepository,
        recipe_ingredients: RecipeIngredientRepository,
    ) -> None:
        self.recipes: RecipeRepository = recipes
        self.ingredients: IngredientRepository = ingredients
        self.recipe_ingredients: RecipeIngredientRepository = recipe_ingredients

        self.committed = False
        self.rolled_back = False

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None or not self.committed:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True