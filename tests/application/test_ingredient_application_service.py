import pytest
from uuid import uuid4
from backend.application.ingredient_service import IngredientApplicationService
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.domain.units import Unit
from tests.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.fakes.fake_recipe_repository import FakeRecipeRepository
from tests.fakes.fake_ingredient_repository import FakeIngredientRepository
from tests.fakes.fake_recipe_ingredient_repository import FakeRecipeIngredientRepository

def test_list_ingredients_returns_all_ingredients():
    # Arrange
    tomato = Ingredient(
        id=uuid4(),
        name="Tomate",
        standard_unit=Unit.g,
    )

    flour = Ingredient(
        id=uuid4(),
        name="Farine",
        standard_unit=Unit.g,
    )

    ingredient_repository = FakeIngredientRepository([tomato, flour])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    # Act
    result = service.list_ingredients()

    # Assert
    assert result == [tomato, flour]
    assert uow.committed is False


def test_get_existing_ingredient_returns_ingredient():
    # Arrange
    ingredient = Ingredient(
        id=uuid4(),
        name="Tomato",
        standard_unit=Unit.g,
    )

    flour = Ingredient(
            id=uuid4(),
            name="Farine",
            standard_unit=Unit.g,
        )

    ingredient_repository = FakeIngredientRepository([ingredient, flour])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    # Act
    result = service.get_ingredient(ingredient.id)

    # Assert
    assert result == ingredient
    assert uow.committed is False

def test_get_unknown_ingredient_returns_none():
    # Arrange
    ingredient = Ingredient(
        id=uuid4(),
        name="Tomato",
        standard_unit=Unit.g,
    )

    ingredient_repository = FakeIngredientRepository([ingredient])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    # Act
    result = service.get_ingredient(uuid4())

    # Assert
    assert result is None
    assert uow.committed is False

def test_create_ingredient_adds_ingredient_and_commits():
    # Arrange
    ingredient_repository = FakeIngredientRepository([])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    new_ingredient = NewIngredient(
        name="Tomato",
        standard_unit=Unit.g,
    )

    # Act
    created = service.create_ingredient(new_ingredient)

    # Assert
    assert created.name == "Tomato"
    assert created.standard_unit == Unit.g
    assert ingredient_repository.find_by_id(created.id) == created
    assert uow.committed is True

def test_update_ingredient_modifies_ingredient_and_commits():
    # Arrange
    ingredient1 = Ingredient(
                id=uuid4(),
                name="Tomato",
                standard_unit=Unit.g,
            )
    ingredient2 = Ingredient(
                id=uuid4(),
                name="Shrimp",
                standard_unit=Unit.g,
            )

    ingredient_repository = FakeIngredientRepository([ingredient1, ingredient2])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    # Act
    updated_ingredient = Ingredient(
                        id=ingredient1.id,
                        name="Milk",
                        standard_unit=Unit.pack,
                    )
    service.update_ingredient(updated_ingredient)

    # Assert
    assert ingredient_repository.find_by_id(ingredient1.id) == updated_ingredient
    assert ingredient_repository.find_by_id(ingredient2.id) == ingredient2
    assert uow.committed is True

def test_update_unknown_ingredient_raises_valueerror():
    # Arrange
    ingredient1 = Ingredient(
                id=uuid4(),
                name="Tomato",
                standard_unit=Unit.g,
            )
    ingredient2 = Ingredient(
                id=uuid4(),
                name="Shrimp",
                standard_unit=Unit.g,
            )

    ingredient_repository = FakeIngredientRepository([ingredient1, ingredient2])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    fake_ingredient = Ingredient(uuid4(),"Fake",Unit.unit)
    # Act
    with pytest.raises(ValueError):
            service.update_ingredient(fake_ingredient)

    assert uow.committed is False
    assert uow.rolled_back is True

def test_delete_ingredient_deletes_ingredient_and_commits():
    # Arrange
    ingredient = Ingredient(
        id=uuid4(),
        name="Tomato",
        standard_unit=Unit.g,
    )

    ingredient_repository = FakeIngredientRepository([ingredient])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    # Act
    service.delete_ingredient(ingredient.id)

    # Assert
    assert ingredient_repository.find_by_id(ingredient.id) is None
    assert uow.committed is True

def test_delete_unknown_ingredient_raises_valueerror():
    # Arrange
    ingredient1 = Ingredient(
                id=uuid4(),
                name="Tomato",
                standard_unit=Unit.g,
            )
    ingredient2 = Ingredient(
                id=uuid4(),
                name="Shrimp",
                standard_unit=Unit.g,
            )

    ingredient_repository = FakeIngredientRepository([ingredient1, ingredient2])

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=ingredient_repository,
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = IngredientApplicationService(lambda: uow)

    # Act
    with pytest.raises(ValueError):
            service.delete_ingredient(uuid4())

    assert uow.committed is False
    assert uow.rolled_back is True
