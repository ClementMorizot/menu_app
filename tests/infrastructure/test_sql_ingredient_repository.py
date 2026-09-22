from uuid import uuid4

import pytest

import backend.infrastructure.db_connection as db_connect
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.domain.units import Unit
from backend.infrastructure.sql_ingredient_repository import SqlIngredientRepository


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
    return SqlIngredientRepository(conn)


def unique_name(prefix: str) -> str:
    return f"{prefix}_{uuid4()}"


def insert_ingredient(conn, name: str, unit: Unit) :
    ingredient_id = uuid4()

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ingredients (id, nom, unite_standard_id)
            SELECT %s, %s, u.id
            FROM unites AS u
            WHERE u.nom = %s
            RETURNING id;
            """,
            (
                ingredient_id,
                name,
                unit.value,
            ),
        )
        row = cur.fetchone()

    if row is None:
        raise RuntimeError(f"Unit not found in database: {unit.value}")

    return row[0]


def test_list_ingredients_returns_inserted_ingredients(repository, conn):
    # Arrange
    tomato_name = unique_name("Tomate")
    milk_name = unique_name("Lait")

    tomato_id = insert_ingredient(conn, name=tomato_name, unit=Unit.g)
    milk_id = insert_ingredient(conn, name=milk_name, unit=Unit.mL)

    # Act
    ingredients = repository.list_ingredients()

    # Assert
    assert Ingredient(
        id=tomato_id,
        name=tomato_name,
        standard_unit=Unit.g,
    ) in ingredients

    assert Ingredient(
        id=milk_id,
        name=milk_name,
        standard_unit=Unit.mL,
    ) in ingredients


def test_find_by_id_returns_correct_ingredient(repository, conn):
    # Arrange
    name = unique_name("Farine")
    ingredient_id = insert_ingredient(conn, name=name, unit=Unit.g)

    # Act
    ingredient = repository.find_by_id(ingredient_id)

    # Assert
    assert ingredient == Ingredient(
        id=ingredient_id,
        name=name,
        standard_unit=Unit.g,
    )


def test_find_by_id_returns_none_when_id_not_found(repository):
    # Arrange
    unknown_id = uuid4()

    # Act
    ingredient = repository.find_by_id(unknown_id)

    # Assert
    assert ingredient is None


def test_add_ingredient_correctly_adds_ingredient_to_base(repository, conn):
    # Arrange
    name = unique_name("Riz")

    new_ingredient = NewIngredient(
        name=name,
        standard_unit=Unit.g,
    )

    # Act
    created_ingredient = repository.add_ingredient(new_ingredient)

    # Assert
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT i.id, i.nom, u.nom
            FROM ingredients AS i
            JOIN unites AS u
                ON i.unite_standard_id = u.id
            WHERE i.id = %s;
            """,
            (created_ingredient.id,),
        )
        row = cur.fetchone()

    assert row == (
        created_ingredient.id,
        name,
        Unit.g.value,
    )

    assert created_ingredient.name == name
    assert created_ingredient.standard_unit == Unit.g


def test_update_ingredient_correctly_updates_ingredient_in_base(repository, conn):
    # Arrange
    original_name = unique_name("Sucre")
    updated_name = unique_name("Sucre_blanc")

    ingredient_id = insert_ingredient(conn, name=original_name, unit=Unit.g)

    updated_ingredient = Ingredient(
        id=ingredient_id,
        name=updated_name,
        standard_unit=Unit.kg,
    )

    # Act
    repository.update_ingredient(updated_ingredient)

    # Assert
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT i.id, i.nom, u.nom
            FROM ingredients AS i
            JOIN unites AS u
                ON i.unite_standard_id = u.id
            WHERE i.id = %s;
            """,
            (ingredient_id,),
        )
        row = cur.fetchone()

    assert row == (
        ingredient_id,
        updated_name,
        Unit.kg.value,
    )


def test_update_ingredient_raises_error_when_id_not_found(repository):
    # Arrange
    unknown_ingredient = Ingredient(
        id=uuid4(),
        name=unique_name("Unknown"),
        standard_unit=Unit.g,
    )

    # Act / Assert
    with pytest.raises(ValueError, match="Ingredient not found"):
        repository.update_ingredient(unknown_ingredient)


def test_delete_ingredient_correctly_deletes_ingredient_in_base(repository, conn):
    # Arrange
    name = unique_name("Beurre")
    ingredient_id = insert_ingredient(conn, name=name, unit=Unit.g)

    # Act
    repository.delete_ingredient(ingredient_id)

    # Assert
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM ingredients
            WHERE id = %s;
            """,
            (ingredient_id,),
        )
        row = cur.fetchone()

    assert row is None


def test_delete_ingredient_raises_error_when_id_not_found(repository):
    # Arrange
    unknown_id = uuid4()

    # Act / Assert
    with pytest.raises(ValueError, match="Ingredient not found"):
        repository.delete_ingredient(unknown_id)