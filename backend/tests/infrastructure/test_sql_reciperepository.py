from backend.infrastructure.sql_recipe_repository import SqlRecipeRepository
import backend.infrastructure.db_connection as db_connect
from backend.domain.recipe import Recipe
from uuid import UUID, uuid4
import pytest


def test_sql_list_recipes():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    test_recipe = Recipe(
        id=UUID("1e676777-9b35-4e27-8432-2a0c1429ae85"),
        name="Quiche lorraine",
        description="Une tarte salée garnie de lardons, d œufs et de crème fraîche.",
        cooking_time=45,
        number_meals=2,
    )

    # Act
    recipe_list = repository.list_recipes()

    conn.close()

    # Assert
    assert isinstance(recipe_list, list)
    assert test_recipe in recipe_list

    for recipe in recipe_list:
        assert isinstance(recipe, Recipe)
        assert recipe.id is not None
        assert isinstance(recipe.name, str)
        assert isinstance(recipe.number_meals, int)


def test_sql_find_by_id_for_existing_id():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    test_recipe = Recipe(
        id=UUID("1e676777-9b35-4e27-8432-2a0c1429ae85"),
        name="Quiche lorraine",
        description="Une tarte salée garnie de lardons, d œufs et de crème fraîche.",
        cooking_time=45,
        number_meals=2,
    )

    # Act
    target = repository.find_by_id(test_recipe.id)

    conn.close()

    # Assert
    assert isinstance(target, Recipe)
    assert target.id == test_recipe.id
    assert target.name == test_recipe.name
    assert target.number_meals == test_recipe.number_meals
    assert target.cooking_time == test_recipe.cooking_time


def test_sql_find_by_id_for_unknown_id():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)

    # Act
    target = repository.find_by_id(
        UUID("00000000-0000-0000-0000-000000000000")
    )

    conn.close()

    # Assert
    assert target is None


def test_sql_add_recipe_for_new_recipe():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    new_recipe = Recipe(
        id=uuid4(),
        name="Salade de fraises",
        description="Des fraises coupées en morceaux avec du sucre.",
        cooking_time=15,
        number_meals=1,
    )

    # Act
    added_recipe = repository.add_recipe(new_recipe)

    # Assert
    recipe_from_base = repository.find_by_id(added_recipe.id)

    assert recipe_from_base is not None
    assert recipe_from_base.id == added_recipe.id
    assert recipe_from_base.name == added_recipe.name
    assert recipe_from_base.description == added_recipe.description
    assert recipe_from_base.cooking_time == added_recipe.cooking_time
    assert recipe_from_base.number_meals == added_recipe.number_meals

    # Clean-up
    repository.delete_recipe(added_recipe.id)
    conn.close()


def test_sql_update_recipe_for_existing_id_in_repository():

    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    indicator = Recipe(
        id=uuid4(),
        name="Test",
        description="Ceci est une recette test.",
        cooking_time=1,
        number_meals=1,
    )
    indicator = repository.add_recipe(indicator)

    test_recipe = Recipe(
        id=indicator.id,
        name="Test update",
        description="Ceci est une recette test mise à jour.",
        cooking_time=15,
        number_meals=3,
    )

    # Act
    repository.update_recipe(test_recipe)

    # Assert
    check_recipe = repository.find_by_id(indicator.id)
    assert check_recipe is not None
    assert check_recipe.name == test_recipe.name
    assert check_recipe.description == test_recipe.description
    assert check_recipe.cooking_time == test_recipe.cooking_time
    assert check_recipe.number_meals == test_recipe.number_meals

    # Clean-up
    repository.delete_recipe(indicator.id)
    conn.close()


def test_sql_update_recipe_for_unknown_id_in_repository():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    new_recipe = Recipe(
        id=uuid4(),
        name="Salade de fraises",
        description="Des fraises coupées en morceaux avec du sucre.",
        cooking_time=15,
        number_meals=1,
    )

    # Act / Assert
    with pytest.raises(ValueError):
        repository.update_recipe(new_recipe)

    conn.close()


def test_sql_delete_recipe_for_existing_id():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    test_recipe = Recipe(
        id=uuid4(),
        name="Test",
        description="Ceci est une recette test.",
        cooking_time=1,
        number_meals=1,
    )
    test_recipe = repository.add_recipe(test_recipe)

    # Act
    repository.delete_recipe(test_recipe.id)

    # Assert
    assert repository.find_by_id(test_recipe.id) is None

    conn.close()


def test_sql_delete_recipe_for_unknown_id_in_repository():
    # Arrange
    conn = db_connect.get_connection()
    repository = SqlRecipeRepository(conn)
    new_recipe = Recipe(
        id=uuid4(),
        name="Salade de fraises",
        description="Des fraises coupées en morceaux avec du sucre.",
        cooking_time=15,
        number_meals=1,
    )

    # Act / Assert
    with pytest.raises(ValueError):
        repository.delete_recipe(new_recipe.id)

    conn.close()
