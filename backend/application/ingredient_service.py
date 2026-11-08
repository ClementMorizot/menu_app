from uuid import UUID
from collections.abc import Callable
from backend.application.unit_of_work import UnitOfWork
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.domain.errors import IngredientNotFound, IngredientDuplicationError

class IngredientApplicationService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def list_ingredients(self) -> list[Ingredient]:
        with self._uow_factory() as uow:
            return uow.ingredients.list_ingredients()

    def get_ingredient(self, ingredient_id: UUID) -> Ingredient:
        with self._uow_factory() as uow:
            ingredient = uow.ingredients.find_by_id(ingredient_id)
            if ingredient is None:
                raise IngredientNotFound(ingredient_id)
            return ingredient

    def create_ingredient(self, new_ingredient: NewIngredient) -> Ingredient:
        with self._uow_factory() as uow:
            for ingredient in uow.ingredients.list_ingredients():
                if ingredient.name == new_ingredient.name:
                    raise IngredientDuplicationError(new_ingredient.name)
            created_ingredient = uow.ingredients.add_ingredient(new_ingredient)
            uow.commit()
            return created_ingredient

    def update_ingredient(self, updated_ingredient: Ingredient) -> None:
        with self._uow_factory() as uow:
            for ingredient in uow.ingredients.list_ingredients():
                if ingredient.name == updated_ingredient.name and ingredient.id != updated_ingredient.id:
                    raise IngredientDuplicationError(updated_ingredient.name)
            uow.ingredients.update_ingredient(updated_ingredient)
            uow.commit()

    def delete_ingredient(self, ingredient_id: UUID) -> None:
        with self._uow_factory() as uow:
            uow.ingredients.delete_ingredient(ingredient_id)
            uow.commit()