from uuid import UUID
from collections.abc import Callable
from backend.application.unit_of_work import UnitOfWork
from backend.domain.recipe import Recipe, NewRecipe
from backend.domain.measured_ingredients import RecipeIngredient


class RecipeApplicationService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def list_recipes(self) -> list[Recipe]:
        with self._uow_factory() as uow:
            return uow.recipes.list_recipes()

    def get_recipe(self, recipe_id: UUID) -> Recipe | None:
        with self._uow_factory() as uow:
            return uow.recipes.find_by_id(recipe_id)

    def get_ingredients_of_recipe(self, recipe_id: UUID) -> list[RecipeIngredient]:
        with self._uow_factory() as uow:
            return uow.recipe_ingredients.get_ingredients_of_recipe(recipe_id)

    def create_recipe(self, new_recipe: NewRecipe, recipe_ingredients: list[RecipeIngredient]) -> Recipe:
        with self._uow_factory() as uow:
            recipe = uow.recipes.add_recipe(new_recipe)

            for recipe_ingredient in recipe_ingredients:
                uow.recipe_ingredients.add_recipe_ingredient(recipe.id, recipe_ingredient)

            uow.commit()
            return recipe

    def update_recipe(self, recipe: Recipe, recipe_ingredients: list[RecipeIngredient]) -> None:
        with self._uow_factory() as uow:
            uow.recipes.update_recipe(recipe)
            uow.recipe_ingredients.update_recipe_ingredients(recipe.id, recipe_ingredients)
            uow.commit()

    def delete_recipe(self, recipe_id: UUID) -> None:
        with self._uow_factory() as uow:
            uow.recipe_ingredients.delete_all_recipe_ingredients_for_recipe(recipe_id)
            uow.recipes.delete_recipe(recipe_id)
            uow.commit()