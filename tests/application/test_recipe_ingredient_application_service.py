import pytest
from uuid import uuid4
from decimal import Decimal

from backend.application.recipe_ingredient_service import RecipeIngredientApplicationService
from backend.domain.ingredient import Ingredient
from backend.domain.recipe import Recipe
from backend.domain.measured_ingredients import RecipeIngredient
from backend.domain.units import Unit
from tests.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.fakes.fake_recipe_repository import FakeRecipeRepository
from tests.fakes.fake_ingredient_repository import FakeIngredientRepository
from tests.fakes.fake_recipe_ingredient_repository import FakeRecipeIngredientRepository, FailingRecipeIngredientRepository

def test_get_ingredients_of_recipe_returns_recipe_ingredients():
    # Arrange
    recipe_id = uuid4()

    measured = RecipeIngredient(
        ingredient=Ingredient(
            id=uuid4(),
            name="Flour",
            standard_unit=Unit.g,
        ),
        quantity=Decimal("250"),
        unit=Unit.g,
    )

    repository = FakeRecipeIngredientRepository(
        {
            recipe_id: (measured,),
        }
    )

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    result = service.get_ingredients_of_recipe(recipe_id)

    # Assert
    assert result == [measured]
    assert uow.committed is False

def test_get_ingredients_of_unknown_recipe_returns_empty_list():
    # Arrange
    recipe_id = uuid4()

    measured = RecipeIngredient(
        ingredient=Ingredient(
            id=uuid4(),
            name="Flour",
            standard_unit=Unit.g,
        ),
        quantity=Decimal("250"),
        unit=Unit.g,
    )

    repository = FakeRecipeIngredientRepository(
        {
            recipe_id: (measured,),
        }
    )

    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    result = service.get_ingredients_of_recipe(uuid4())

    # Assert
    assert result == []
    assert uow.committed is False

def test_add_recipe_ingredient_adds_recipe_ingredient_to_recipe():
    # Arrange
    recipe = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )

    recipe_repository = FakeRecipeRepository([recipe])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe.id : (pasta_ingredient,)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    service.add_recipe_ingredient(recipe.id, bolognaise_ingredient)

    # Assert
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe.id) == [pasta_ingredient, bolognaise_ingredient]
    assert uow.committed is True

def test_add_duplicate_recipe_ingredient_raises_error():
    # Arrange
    recipe = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )

    recipe_repository = FakeRecipeRepository([recipe])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe.id : (pasta_ingredient,)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    with pytest.raises(ValueError):
        service.add_recipe_ingredient(recipe.id, pasta_ingredient)

    # Assert
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe.id) == [pasta_ingredient]
    assert uow.committed is False
    assert uow.rolled_back is True

def test_add_recipe_ingredient_with_failing_repository_raises_error():
    # Arrange
    recipe = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )

    recipe_repository = FakeRecipeRepository([recipe])
    recipe_ingredient_repository = FailingRecipeIngredientRepository(
        {
            recipe.id : (pasta_ingredient,)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    with pytest.raises(RuntimeError):
        service.add_recipe_ingredient(recipe.id, bolognaise_ingredient)

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True

def test_update_recipe_ingredients_updates_correct_recipe():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    recipe2 = Recipe(
            id=uuid4(),
            name="Pizza",
            description="Description",
            cooking_time=25,
            number_meals=1,
        )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )
    dough_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(), "Dough", Unit.unit),
        unit= Unit.unit,
        quantity= Decimal("1")
    )

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient),
            recipe2.id : (dough_ingredient,)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    test_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(), "Test ingredient", Unit.unit),
            unit= Unit.unit,
            quantity= Decimal("1")
        )

    # Act
    service.update_recipe_ingredients(recipe1.id, [test_ingredient])

    # Assert
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe1.id) == [test_ingredient]
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe2.id) == [dough_ingredient]
    assert uow.committed is True

def test_update_recipe_ingredients_with_failing_repository_raises_error():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    recipe2 = Recipe(
            id=uuid4(),
            name="Pizza",
            description="Description",
            cooking_time=25,
            number_meals=1,
        )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )
    dough_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(), "Dough", Unit.unit),
        unit= Unit.unit,
        quantity= Decimal("1")
    )

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FailingRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient),
            recipe2.id : (dough_ingredient,)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    test_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(), "Test ingredient", Unit.unit),
            unit= Unit.unit,
            quantity= Decimal("1")
        )

    # Act
    with pytest.raises(RuntimeError):
        service.update_recipe_ingredients(recipe1.id, [test_ingredient])

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True

def test_delete_recipe_ingredient_correctly_deletes_target_recipe_ingredient():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )
    recipe2 = Recipe(
                id=uuid4(),
                name="Pizza",
                description="Description",
                cooking_time=25,
                number_meals=1,
            )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )
    dough_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(), "Dough", Unit.unit),
            unit= Unit.unit,
            quantity= Decimal("1")
        )
    test_recipe_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(), "Test ingredient", Unit.unit),
        unit = Unit.unit,
        quantity = Decimal("3")
    )
    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, test_recipe_ingredient, bolognaise_ingredient),
            recipe2.id : (dough_ingredient, test_recipe_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    service.delete_recipe_ingredient(recipe1.id, test_recipe_ingredient.ingredient.id)

    # Assert
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe1.id) == [pasta_ingredient, bolognaise_ingredient]
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe2.id) == [dough_ingredient, test_recipe_ingredient]
    assert uow.committed is True

def test_delete_recipe_ingredient_on_unknown_relation_raises_error():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )

    recipe_repository = FakeRecipeRepository([recipe1])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient),
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    with pytest.raises(ValueError):
        service.delete_recipe_ingredient(recipe1.id, uuid4())

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True

def test_delete_recipe_ingredient_with_failing_repository_raises_error():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="Pasta a la bolognaise",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )
    recipe2 = Recipe(
                id=uuid4(),
                name="Pizza",
                description="Description",
                cooking_time=25,
                number_meals=1,
            )

    pasta_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(),"Pasta",Unit.g),
        unit= Unit.g,
        quantity= Decimal("350")
    )
    bolognaise_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Bolognaise",Unit.pack),
            unit= Unit.pack,
            quantity= Decimal("2")
        )
    dough_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(), "Dough", Unit.unit),
            unit= Unit.unit,
            quantity= Decimal("1")
        )
    test_recipe_ingredient = RecipeIngredient(
        ingredient= Ingredient(uuid4(), "Test ingredient", Unit.unit),
        unit = Unit.unit,
        quantity = Decimal("3")
    )
    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FailingRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, test_recipe_ingredient, bolognaise_ingredient),
            recipe2.id : (dough_ingredient, test_recipe_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeIngredientApplicationService(lambda: uow)

    # Act
    with pytest.raises(RuntimeError):
        service.delete_recipe_ingredient(recipe1.id, test_recipe_ingredient.ingredient.id)

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True