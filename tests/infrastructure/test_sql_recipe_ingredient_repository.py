import pytest
import psycopg
from decimal import Decimal
from uuid import uuid4
import backend.infrastructure.db_connection as db_connect
from backend.domain.ingredient import Ingredient
from backend.domain.measured_ingredients import RecipeIngredient
from backend.domain.units import Unit
from backend.infrastructure.sql_recipe_ingredient_repository import SqlRecipeIngredientRepository


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
def insert_recipe(conn):
    def _insert_recipe(
        *,
        name: str = "Test recipe",
        description: str = "Test description",
        cooking_time: int = 30,
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
                VALUES (%s, %s, %s, %s, %s)
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

    return _insert_recipe

@pytest.fixture
def get_or_insert_unit(conn):
    def _get_or_insert_unit(unit: Unit):
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM unites
                WHERE nom = %s
                """,
                (unit.value,),
            )
            row = cur.fetchone()

            if row is not None:
                return row[0]

            cur.execute(
                """
                INSERT INTO unites (nom)
                VALUES (%s)
                RETURNING id
                """,
                (unit.value,),
            )
            return cur.fetchone()[0]

    return _get_or_insert_unit

@pytest.fixture
def insert_ingredient(conn):
    def _insert_ingredient(
        *,
        name: str = "Test ingredient",
        standard_unit_id,
    ):
        ingredient_id = uuid4()

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ingredients (
                    id,
                    nom,
                    unite_standard_id
                )
                VALUES (%s, %s, %s)
                """,
                (
                    ingredient_id,
                    name,
                    standard_unit_id,
                ),
            )

        return ingredient_id

    return _insert_ingredient

@pytest.fixture
def insert_recipe_ingredient(conn):
    def _insert_recipe_ingredient(
        *,
        recipe_id,
        ingredient_id,
        quantity: Decimal = Decimal("100"),
        unit_id,
    ):
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO recette_ingredients (
                    recette_id,
                    ingredient_id,
                    quantite,
                    unite_id
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    recipe_id,
                    ingredient_id,
                    quantity,
                    unit_id,
                ),
            )

    return _insert_recipe_ingredient

def test_get_ingredients_of_recipe_returns_recipe_ingredients_for_existing_recipe(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    insert_recipe_ingredient,
    ):

    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    insert_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_id=flour_id,
        quantity=Decimal("250"),
        unit_id=gram_unit_id,
        )

    # Act
    result = repository.get_ingredients_of_recipe(recipe_id)

    # Assert
    assert len(result) == 1
    assert result[0].ingredient.id == flour_id
    assert result[0].ingredient.name == "Flour"
    assert result[0].ingredient.standard_unit == Unit.g
    assert result[0].unit == Unit.g
    assert result[0].quantity == Decimal("250")

def test_get_ingredients_of_unknown_recipe_returns_empty_list(conn):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)
    unknown_recipe_id = uuid4()

    # Act
    result = repository.get_ingredients_of_recipe(unknown_recipe_id)

    # Assert
    assert result == []

def test_add_recipe_ingredient_inserts_correctly_ingredient_with_recipe_in_base(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")

    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
    )

    flour = Ingredient(
        id=flour_id,
        name="Flour",
        standard_unit=Unit.g,
    )

    recipe_ingredient = RecipeIngredient(
        ingredient=flour,
        unit=Unit.g,
        quantity=Decimal("250"),
    )

    # Act
    repository.add_recipe_ingredient(recipe_id, recipe_ingredient)

    # Assert
    result = repository.get_ingredients_of_recipe(recipe_id)
    assert result == [recipe_ingredient]

def test_add_duplicate_recipe_ingredient_raises_unique_violation(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    insert_recipe_ingredient,
    ):

    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    insert_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_id=flour_id,
        quantity=Decimal("250"),
        unit_id=gram_unit_id,
        )

    flour_recipe_ingredient = RecipeIngredient(
        ingredient= Ingredient(flour_id, "Flour", Unit.g),
        unit= Unit.g,
        quantity = Decimal("250")
    )

    # Act
    with pytest.raises(psycopg.errors.UniqueViolation):
        repository.add_recipe_ingredient(recipe_id, flour_recipe_ingredient)

def test_add_recipe_ingredient_to_unknown_recipe_raises_error(
    conn,
    get_or_insert_unit,
    insert_ingredient,
    ):

    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    gram_unit_id = get_or_insert_unit(Unit.g)
    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )
    flour_recipe_ingredient = RecipeIngredient(
        ingredient= Ingredient(flour_id, "Flour", Unit.g),
        unit= Unit.g,
        quantity = Decimal("250")
    )

    # Act
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        repository.add_recipe_ingredient(uuid4(), flour_recipe_ingredient)

def test_add_unknown_ingredient_to_recipe_raises_error(
    conn,
    get_or_insert_unit,
    insert_recipe,
    ):

    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)

    flour = Ingredient(
        id=uuid4(),
        name="Flour",
        standard_unit=Unit.g,
    )

    flour_recipe_ingredient = RecipeIngredient(
        ingredient=flour,
        unit=Unit.g,
        quantity=Decimal("250"),
    )

    # Act
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        repository.add_recipe_ingredient(recipe_id, flour_recipe_ingredient)

def test_update_recipe_ingredients_replaces_old_ingredient_list_with_new_list(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    insert_recipe_ingredient,
    ):

    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)
    unit_unit_id = get_or_insert_unit(Unit.unit)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    egg_id = insert_ingredient(
        name="Egg",
        standard_unit_id=unit_unit_id
    )

    insert_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_id=flour_id,
        quantity=Decimal("250"),
        unit_id=gram_unit_id,
        )

    egg_recipe_ingredient = RecipeIngredient(
        ingredient= Ingredient(egg_id, "Egg", Unit.unit),
        unit= Unit.unit,
        quantity= Decimal("4")
    )

    # Act
    repository.update_recipe_ingredients(recipe_id, [egg_recipe_ingredient])

    # Assert
    result = repository.get_ingredients_of_recipe(recipe_id)
    assert len(result) == 1
    assert result[0].ingredient.id == egg_id
    assert result[0].ingredient.name == "Egg"
    assert result[0].ingredient.standard_unit == Unit.unit
    assert result[0].unit == Unit.unit
    assert result[0].quantity == Decimal("4")

def test_update_recipe_ingredients_replaces_old_ingredient_with_empty_list_to_get_no_associated_ingredients_with_recipe(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    insert_recipe_ingredient,
    ):

    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    insert_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_id=flour_id,
        quantity=Decimal("250"),
        unit_id=gram_unit_id,
        )

    # Act
    repository.update_recipe_ingredients(recipe_id, [])

    # Assert
    assert repository.get_ingredients_of_recipe(recipe_id) == []

def test_update_recipe_ingredients_with_no_ingredient_for_unknown_recipe_raises_error(conn):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    # Act / assert
    with pytest.raises(ValueError):
        repository.update_recipe_ingredients(uuid4(), [])

def test_update_recipe_ingredients_with_ingredients_for_unknown_recipe_raises_error(
    conn,
    get_or_insert_unit,
    insert_ingredient,
):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)
    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=get_or_insert_unit(Unit.g),
        )

    flour_recipe_ingredient = RecipeIngredient(
        ingredient= Ingredient(flour_id, "Flour", Unit.g),
        unit= Unit.g,
        quantity= Decimal("150")
    )

    # Act / assert
    with pytest.raises(ValueError):
        repository.update_recipe_ingredients(uuid4(), [flour_recipe_ingredient])

def test_delete_recipe_ingredient_removes_ingredient_from_recipe_in_base(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    insert_recipe_ingredient,
    ):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)
    unit_unit_id = get_or_insert_unit(Unit.unit)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    egg_id = insert_ingredient(
        name="Egg",
        standard_unit_id=unit_unit_id
    )

    insert_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_id=flour_id,
        quantity=Decimal("250"),
        unit_id=gram_unit_id,
        )

    insert_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_id= egg_id,
        unit_id= unit_unit_id,
        quantity= Decimal("4")
    )

    # Act
    repository.delete_recipe_ingredient(recipe_id, flour_id)

    # Assert
    result = repository.get_ingredients_of_recipe(recipe_id)
    assert len(result) == 1
    assert result[0].ingredient.id == egg_id
    assert result[0].ingredient.name == "Egg"
    assert result[0].ingredient.standard_unit == Unit.unit
    assert result[0].unit == Unit.unit
    assert result[0].quantity == Decimal("4")

def test_delete_recipe_ingredient_not_in_recipe_raises_error(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    ):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")
    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    # Act
    with pytest.raises(ValueError):
        repository.delete_recipe_ingredient(recipe_id, flour_id)

def test_delete_recipe_ingredient_for_unknown_recipe_raises_error(
    conn,
    get_or_insert_unit,
    insert_ingredient,
    ):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    gram_unit_id = get_or_insert_unit(Unit.g)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    # Act
    with pytest.raises(ValueError):
        repository.delete_recipe_ingredient(uuid4(), flour_id)

def test_delete_unknown_recipe_ingredient_in_recipe_raises_error(
    conn,
    insert_recipe,
    ):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    recipe_id = insert_recipe(name="Pancakes")

    # Act / assert
    with pytest.raises(ValueError):
        repository.delete_recipe_ingredient(recipe_id, uuid4())

def test_delete_all_recipe_ingredient_removes_all_ingredient_from_recipe_in_base(
    conn,
    insert_recipe,
    get_or_insert_unit,
    insert_ingredient,
    insert_recipe_ingredient,
    ):
    # Arrange
    repository = SqlRecipeIngredientRepository(conn)

    pancakes_id = insert_recipe(name="Pancakes")
    dough_id= insert_recipe(name="Dough")
    omelette_id= insert_recipe(name="Omelette")
    gram_unit_id = get_or_insert_unit(Unit.g)
    unit_unit_id = get_or_insert_unit(Unit.unit)

    flour_id = insert_ingredient(
        name="Flour",
        standard_unit_id=gram_unit_id,
        )

    egg_id = insert_ingredient(
        name="Egg",
        standard_unit_id=unit_unit_id
    )

    insert_recipe_ingredient(
        recipe_id=pancakes_id,
        ingredient_id=flour_id,
        quantity=Decimal("250"),
        unit_id=gram_unit_id,
        )

    insert_recipe_ingredient(
        recipe_id=pancakes_id,
        ingredient_id= egg_id,
        unit_id= unit_unit_id,
        quantity= Decimal("4")
    )

    insert_recipe_ingredient(
        recipe_id=dough_id,
        ingredient_id=flour_id,
        quantity=Decimal("450"),
        unit_id=gram_unit_id,
        )

    insert_recipe_ingredient(
        recipe_id=omelette_id,
        ingredient_id= egg_id,
        unit_id= unit_unit_id,
        quantity= Decimal("1")
    )

    # Act
    repository.delete_all_recipe_ingredients_for_recipe(pancakes_id)

    # Assert
    assert repository.get_ingredients_of_recipe(pancakes_id) == []
    assert repository.get_ingredients_of_recipe(dough_id) == [RecipeIngredient(
        ingredient= Ingredient(flour_id, "Flour", Unit.g),
        unit= Unit.g,
        quantity = Decimal("450")
    )]
    assert repository.get_ingredients_of_recipe(omelette_id) == [RecipeIngredient(
        ingredient= Ingredient(egg_id, "Egg", Unit.unit),
        unit= Unit.unit,
        quantity = Decimal("1")
    )]
