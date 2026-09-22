from uuid import UUID
from collections.abc import Callable
from backend.application.unit_of_work import UnitOfWork
from backend.domain.measured_ingredients import RecipeIngredient

class RecipeIngredientApplicationService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def get_ingredients_of_recipe(self, recipe_id: UUID) -> list[RecipeIngredient]:
        with self._uow_factory() as uow:
            return uow.recipe_ingredients.get_ingredients_of_recipe(recipe_id)

    def add_recipe_ingredient(self, recipe_id: UUID, recipe_ingredient: RecipeIngredient) -> None:
        with self._uow_factory() as uow:
            uow.recipe_ingredients.add_recipe_ingredient(recipe_id, recipe_ingredient)
            uow.commit()

    def update_recipe_ingredients(self, recipe_id: UUID, recipe_ingredients: list[RecipeIngredient]) -> None:
        with self._uow_factory() as uow:
            uow.recipe_ingredients.update_recipe_ingredients(recipe_id, recipe_ingredients)
            uow.commit()

    def delete_recipe_ingredient(self, recipe_id: UUID, ingredient_id: UUID) -> None:
        with self._uow_factory() as uow:
            uow.recipe_ingredients.delete_recipe_ingredient(recipe_id, ingredient_id)
            uow.commit()
