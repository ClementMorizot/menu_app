import pytest
import backend.infrastructure.db_connection as db_connect
from backend.infrastructure.sql_recipe_repository import SqlRecipeRepository
from backend.domain.recipe import Recipe, NewRecipe
from uuid import uuid4


@pytest.fixture
def conn():
    connection = db_connect.get_connection()
    connection.autocommit = False

    try:
        yield connection
    finally:
        connection.rollback()
        connection.close()


@pytest.fixture
def repository(conn):
    return SqlRecipeRepository(conn)


def insert_recipe(
    conn,
    *,
    name: str = "Test recipe",
    description: str = "Test description",
    cooking_time: int = 10,
    number_meals: int = 1,
):
    recipe_id = uuid4()

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO recettes (
                id,
                nom,
                description,
                temps_preparation,
                nombre_repas
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                recipe_id,
                name,
                description,
                cooking_time,
                number_meals,
            ),
        )

    return recipe_id

def test_list_recipes_returns_inserted_recipes(repository, conn):
    # Arrange
    suffix = uuid4().hex

    recipe_1_id = insert_recipe(
        conn,
        name=f"AAA Test recipe {suffix}",
        description="First test recipe",
        cooking_time=10,
        number_meals=1,
    )
    recipe_2_id = insert_recipe(
        conn,
        name=f"BBB Test recipe {suffix}",
        description="Second test recipe",
        cooking_time=20,
        number_meals=2,
    )

    expected_recipe_1 = Recipe(
        id=recipe_1_id,
        name=f"AAA Test recipe {suffix}",
        description="First test recipe",
        cooking_time=10,
        number_meals=1,
    )
    expected_recipe_2 = Recipe(
        id=recipe_2_id,
        name=f"BBB Test recipe {suffix}",
        description="Second test recipe",
        cooking_time=20,
        number_meals=2,
    )

    # Act
    recipes = repository.list_recipes()

    # Assert
    assert expected_recipe_1 in recipes
    assert expected_recipe_2 in recipes

def test_list_recipes_returns_recipes_ordered_by_name(repository, conn):
    # Arrange
    suffix = uuid4().hex

    insert_recipe(
        conn,
        name=f"CCC Test recipe {suffix}",
        description="Third recipe",
        cooking_time=30,
        number_meals=3,
    )
    insert_recipe(
        conn,
        name=f"AAA Test recipe {suffix}",
        description="First recipe",
        cooking_time=10,
        number_meals=1,
    )
    insert_recipe(
        conn,
        name=f"BBB Test recipe {suffix}",
        description="Second recipe",
        cooking_time=20,
        number_meals=2,
    )

    # Act
    recipes = repository.list_recipes()

    # Assert
    test_recipe_names = [
        recipe.name
        for recipe in recipes
        if recipe.name.endswith(suffix)
    ]

    assert test_recipe_names == [
        f"AAA Test recipe {suffix}",
        f"BBB Test recipe {suffix}",
        f"CCC Test recipe {suffix}",
    ]

def test_find_by_id_returns_correct_recipe(repository, conn):
    # Arrange
    recipe_id = insert_recipe(
        conn,
        name="Quiche test",
        description="Test description",
        cooking_time=45,
        number_meals=2,
    )

    # Act
    recipe = repository.find_by_id(recipe_id)

    # Assert
    assert recipe == Recipe(
        id=recipe_id,
        name="Quiche test",
        description="Test description",
        cooking_time=45,
        number_meals=2,
    )

def test_find_by_id_returns_none_when_id_not_found(repository):
    # Arrange
    unknown_id = uuid4()

    # Act
    recipe = repository.find_by_id(unknown_id)

    # Assert
    assert recipe is None

def test_add_recipe_correctly_adds_recipe_to_base(repository, conn):
    # Arrange
    new_recipe = NewRecipe(
        name="Salade de fraises",
        description="Des fraises coupées en morceaux avec du sucre.",
        cooking_time=15,
        number_meals=1,
    )

    # Act
    added_recipe = repository.add_recipe(new_recipe)

    # Assert
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, nom, description, temps_preparation, nombre_repas
            FROM recettes
            WHERE id = %s;
            """,
            (added_recipe.id,),
        )
        row = cur.fetchone()

    assert row == (
        added_recipe.id,
        "Salade de fraises",
        "Des fraises coupées en morceaux avec du sucre.",
        15,
        1,
    )

    assert added_recipe.name == new_recipe.name
    assert added_recipe.description == new_recipe.description
    assert added_recipe.cooking_time == new_recipe.cooking_time
    assert added_recipe.number_meals == new_recipe.number_meals

def test_update_recipe_correctly_updates_recipe_in_base(repository, conn):
    # Arrange
    recipe_id = insert_recipe(
        conn,
        name="Test recipe",
        description="Initial description",
        cooking_time=10,
        number_meals=1,
    )

    updated_recipe = Recipe(
        id=recipe_id,
        name="Updated test recipe",
        description="Updated description",
        cooking_time=25,
        number_meals=3,
    )

    # Act
    repository.update_recipe(updated_recipe)

    # Assert
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, nom, description, temps_preparation, nombre_repas
            FROM recettes
            WHERE id = %s;
            """,
            (recipe_id,),
        )
        row = cur.fetchone()

    assert row == (
        recipe_id,
        "Updated test recipe",
        "Updated description",
        25,
        3,
    )

def test_update_recipe_raises_error_when_id_not_found(repository):
    # Arrange
    unknown_recipe = Recipe(
        id=uuid4(),
        name="Unknown recipe",
        description="Unknown description",
        cooking_time=15,
        number_meals=1,
    )

    # Act / Assert
    with pytest.raises(ValueError, match="Recipe not found"):
        repository.update_recipe(unknown_recipe)

def test_delete_recipe_correctly_deletes_recipe_from_base(repository, conn):
    # Arrange
    recipe_id = insert_recipe(
        conn,
        name="Recipe to delete",
        description="This recipe should be deleted",
        cooking_time=5,
        number_meals=1,
    )

    # Act
    repository.delete_recipe(recipe_id)

    # Assert
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM recettes
            WHERE id = %s;
            """,
            (recipe_id,),
        )
        row = cur.fetchone()

    assert row is None

def test_delete_recipe_raises_error_when_id_not_found(repository):
    # Arrange
    unknown_id = uuid4()

    # Act / Assert
    with pytest.raises(ValueError, match="Recipe not found"):
        repository.delete_recipe(unknown_id)