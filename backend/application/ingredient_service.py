from uuid import UUID
from collections.abc import Callable
from backend.application.unit_of_work import UnitOfWork
from backend.domain.ingredient import Ingredient, NewIngredient


class IngredientApplicationService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory


    def list_ingredients(self) -> list[Ingredient]:
        with self._uow_factory() as uow:
            return uow.ingredients.list_ingredients()

    def get_ingredient(self, ingredient_id: UUID) -> Ingredient | None:
        with self._uow_factory() as uow:
            return uow.ingredients.find_by_id(ingredient_id)

    def create_ingredient(self, new_ingredient: NewIngredient) -> Ingredient:
        with self._uow_factory() as uow:
            ingredient = uow.ingredients.add_ingredient(new_ingredient)
            uow.commit()
            return ingredient

    def update_ingredient(self, ingredient: Ingredient) -> None:
        with self._uow_factory() as uow:
            uow.ingredients.update_ingredient(ingredient)
            uow.commit()

    def delete_ingredient(self, ingredient_id: UUID) -> None:
        with self._uow_factory() as uow:
            uow.ingredients.delete_ingredient(ingredient_id)
            uow.commit()