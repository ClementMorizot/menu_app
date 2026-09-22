import pytest
from uuid import uuid4
from decimal import Decimal

from backend.application.recipe_service import RecipeApplicationService
from backend.domain.ingredient import Ingredient
from backend.domain.recipe import Recipe, NewRecipe
from backend.domain.measured_ingredients import RecipeIngredient
from backend.domain.units import Unit
from tests.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.fakes.fake_recipe_repository import FakeRecipeRepository, FailingRecipeRepository
from tests.fakes.fake_ingredient_repository import FakeIngredientRepository
from tests.fakes.fake_recipe_ingredient_repository import FakeRecipeIngredientRepository, FailingRecipeIngredientRepository

def test_list_recipes_returns_all_recipes():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="French pie",
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

    repository = FakeRecipeRepository([recipe1, recipe2])

    uow = FakeUnitOfWork(
        recipes=repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    result = service.list_recipes()

    # Assert
    assert result == [recipe1, recipe2]
    assert uow.committed is False

def test_get_recipe_returns_recipe():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="French pie",
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

    repository = FakeRecipeRepository([recipe1, recipe2])

    uow = FakeUnitOfWork(
        recipes=repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    result = service.get_recipe(recipe1.id)

    # Assert
    assert result == recipe1
    assert uow.committed is False

def test_get_unknown_recipe_returns_none():
    # Arrange
    recipe1 = Recipe(
        id=uuid4(),
        name="French pie",
        description="Description",
        cooking_time=45,
        number_meals=2,
    )

    repository = FakeRecipeRepository([recipe1])

    uow = FakeUnitOfWork(
        recipes=repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    result = service.get_recipe(uuid4())

    # Assert
    assert result is None
    assert uow.committed is False

def test_get_ingredients_of_recipe_returns_all_recipe_ingredients():
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
            recipe.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    result = service.get_ingredients_of_recipe(recipe.id)

    # Assert
    assert result == [pasta_ingredient, bolognaise_ingredient]
    assert uow.committed is False

def test_get_ingredients_of_unknown_recipe_returns_empty_list():
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
            recipe.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    result = service.get_ingredients_of_recipe(uuid4())

    # Assert
    assert result == []
    assert uow.committed is False

def test_create_recipe_adds_recipe_and_commits():
    # Arrange
    recipe_repository = FakeRecipeRepository([])
    recipe_ingredient_repository = FakeRecipeIngredientRepository()

    uow = FakeUnitOfWork(
        recipes = recipe_repository,
        ingredients = FakeIngredientRepository(),
        recipe_ingredients = recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    new_recipe = NewRecipe(
        name="Pizza",
        description="Test description",
        cooking_time=45,
        number_meals=2,
    )

    new_recipe_ingredient_list = [
        RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Pizza dough", Unit.unit),
            unit= Unit.unit,
            quantity= Decimal("1")
        ),
        RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Tomato sauce", Unit.mL),
            unit= Unit.mL,
            quantity= Decimal("180")
        )
    ]

    # Act
    created = service.create_recipe(new_recipe, new_recipe_ingredient_list)

    # Assert
    assert created.name == "Pizza"
    assert recipe_repository.find_by_id(created.id) == created
    assert recipe_ingredient_repository.get_ingredients_of_recipe(created.id) == new_recipe_ingredient_list
    assert uow.committed is True

def test_create_recipe_rolls_back_upons_repository_error():
    # Arrange
    recipe_repository = FakeRecipeRepository([])
    recipe_ingredient_repository = FailingRecipeIngredientRepository()

    uow = FakeUnitOfWork(
        recipes = recipe_repository,
        ingredients = FakeIngredientRepository(),
        recipe_ingredients = recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    new_recipe = NewRecipe(
        name="Pizza",
        description="Test description",
        cooking_time=45,
        number_meals=2,
    )

    new_recipe_ingredient_list = [
        RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Pizza dough", Unit.unit),
            unit= Unit.unit,
            quantity= Decimal("1")
        ),
        RecipeIngredient(
            ingredient= Ingredient(uuid4(),"Tomato sauce", Unit.mL),
            unit= Unit.mL,
            quantity= Decimal("180")
        )
    ]

    # Act
    with pytest.raises(RuntimeError):
        service.create_recipe(new_recipe, new_recipe_ingredient_list)

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True

def test_update_recipe_correctly_updates_the_correct_recipe():
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

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    updated_recipe = Recipe(
            id=recipe1.id,
            name="Update test",
            description="Test description",
            cooking_time=5,
            number_meals=25,
        )
    test_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"test",Unit.bunch),
            unit= Unit.bunch,
            quantity= Decimal("50")
        )

    # Act
    service.update_recipe(updated_recipe,[test_ingredient])

    # Assert
    assert recipe_repository.find_by_id(updated_recipe.id) == updated_recipe
    assert recipe_repository.find_by_id(recipe2.id) == recipe2
    assert recipe_ingredient_repository.get_ingredients_of_recipe(updated_recipe.id) == [test_ingredient]
    assert uow.committed is True

def test_update_unknown_recipe_raises_valueerror():
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

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    fake_recipe = Recipe(
            id=uuid4(),
            name="Update test",
            description="Test description",
            cooking_time=5,
            number_meals=25,
        )
    test_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"test",Unit.bunch),
            unit= Unit.bunch,
            quantity= Decimal("50")
        )

    # Act
    with pytest.raises(ValueError):
        service.update_recipe(fake_recipe, [test_ingredient])

    assert uow.committed is False
    assert uow.rolled_back is True
    assert recipe_repository.find_by_id(recipe1.id) == recipe1
    assert recipe_repository.find_by_id(recipe2.id) == recipe2

def test_update_recipe_rolls_back_upon_repository_error():
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

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FailingRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    updated_recipe = Recipe(
            id=recipe1.id,
            name="Update test",
            description="Test description",
            cooking_time=5,
            number_meals=25,
        )
    test_ingredient = RecipeIngredient(
            ingredient= Ingredient(uuid4(),"test",Unit.bunch),
            unit= Unit.bunch,
            quantity= Decimal("50")
        )

    # Act
    with pytest.raises(RuntimeError):
        service.update_recipe(updated_recipe,[test_ingredient])

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True

def test_delete_recipe_deletes_the_correct_recipe():
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

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    service.delete_recipe(recipe1.id)

    # Assert
    assert recipe_repository.find_by_id(recipe1.id) is None
    assert recipe_ingredient_repository.get_ingredients_of_recipe(recipe1.id) == []
    assert recipe_repository.find_by_id(recipe2.id) == recipe2
    assert uow.committed is True

def test_delete_unknown_recipe_raises_valueerror():
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

    recipe_repository = FakeRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    with pytest.raises(ValueError):
        service.delete_recipe(uuid4())

    assert uow.committed is False
    assert uow.rolled_back is True

def test_delete_recipe_rolls_back_upon_repository_error():
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

    recipe_repository = FailingRecipeRepository([recipe1, recipe2])
    recipe_ingredient_repository = FakeRecipeIngredientRepository(
        {
            recipe1.id : (pasta_ingredient, bolognaise_ingredient)
        }
    )

    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=recipe_ingredient_repository,
    )

    service = RecipeApplicationService(lambda: uow)

    # Act
    with pytest.raises(RuntimeError):
        service.delete_recipe(recipe1.id)

    # Assert
    assert uow.committed is False
    assert uow.rolled_back is True