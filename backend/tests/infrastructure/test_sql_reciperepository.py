from infrastructure.sql_recipe_repository import SqlRecipeRepository
import infrastructure.db_connection as db_connect
from domain.recette import Recette
from uuid import UUID, uuid4
import pytest

def test_sql_list_recipe():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    recette_test = Recette(
        id = UUID("1e676777-9b35-4e27-8432-2a0c1429ae85"),
        nom = "Quiche lorraine",
        description = "Une tarte salée garnie de lardons, d œufs et de crème fraîche.",
        temps_preparation = 45,
        nombre_repas = 2)
    
    # Act
    liste_recettes = sql_recipe_repo.list_recipes()

    conn.close()
    
    # Assert
    assert isinstance(liste_recettes, list)
    assert recette_test in liste_recettes

    for recette in liste_recettes:
        assert isinstance(recette, Recette)
        assert recette.id is not None
        assert isinstance(recette.nom, str)
        assert isinstance(recette.nombre_repas, int)

def test_sql_find_by_id_pour_id_existant():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    recette_test = Recette(
        id = UUID("1e676777-9b35-4e27-8432-2a0c1429ae85"),
        nom = "Quiche lorraine",
        description = "Une tarte salée garnie de lardons, d œufs et de crème fraîche.",
        temps_preparation = 45,
        nombre_repas = 2)
    
    # Act
    recette_cible = sql_recipe_repo.find_by_id(recette_test.id)

    conn.close()

    # Assert
    assert isinstance(recette_cible,Recette)
    assert recette_cible.id == recette_test.id
    assert recette_cible.nom == recette_test.nom
    assert recette_cible.nombre_repas == recette_test.nombre_repas
    assert recette_cible.temps_preparation == recette_test.temps_preparation

def test_sql_find_by_id_pour_id_non_trouve():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    
    # Act
    recette_cible = sql_recipe_repo.find_by_id(UUID("00000000-0000-0000-0000-000000000000"))

    conn.close()

    # Assert
    assert recette_cible is None

def test_sql_add_recipe_pour_nouvelle_recette():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    nouvelle_recette = Recette(
        id = uuid4(),
        nom = "Salade de fraises",
        description = "Des fraises coupées en morceaux avec du sucre.",
        temps_preparation = 15,
        nombre_repas = 1)
    
    # Act
    recette_inseree = sql_recipe_repo.add_recipe(nouvelle_recette)

    # Assert
    recette_extraite = sql_recipe_repo.find_by_id(recette_inseree.id)
    
    assert recette_extraite is not None
    assert recette_extraite.id == recette_inseree.id
    assert recette_extraite.nom == recette_inseree.nom
    assert recette_extraite.description == recette_inseree.description
    assert recette_extraite.temps_preparation == recette_inseree.temps_preparation
    assert recette_extraite.nombre_repas == recette_inseree.nombre_repas

    # Clean-up
    sql_recipe_repo.delete_recipe(recette_inseree.id)
    conn.close()

def test_sql_update_recipe_pour_recette_existante_dans_le_repository():

    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    recette_temoin = Recette(
        id= uuid4(),
        nom = "Test",
        description = "Ceci est une recette test.",
        temps_preparation = 1,
        nombre_repas = 1
    )
    recette_temoin = sql_recipe_repo.add_recipe(recette_temoin)

    recette_test = Recette(
        id= recette_temoin.id,
        nom = "Test",
        description = "Ceci est une recette test.",
        temps_preparation = 1,
        nombre_repas = 1
    )

    # Act
    sql_recipe_repo.update_recipe(recette_test)

    # Assert
    verification = sql_recipe_repo.find_by_id(recette_temoin.id)
    assert verification is not None
    assert verification.nom == recette_test.nom
    assert verification.description == recette_test.description
    assert verification.temps_preparation == recette_test.temps_preparation
    assert verification.nombre_repas == recette_test.nombre_repas

    # Clean-up
    sql_recipe_repo.delete_recipe(recette_temoin.id)
    conn.close()

def test_sql_update_recipe_pour_recette_absente_du_repository():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    nouvelle_recette = Recette(
        id = uuid4(),
        nom = "Salade de fraises",
        description = "Des fraises coupées en morceaux avec du sucre.",
        temps_preparation = 15,
        nombre_repas = 1)
    
    # Act / Assert
    with pytest.raises(ValueError):
        sql_recipe_repo.update_recipe(nouvelle_recette)

    conn.close()

def test_sql_delete_recipe_pour_recette_existante_dans_le_repository():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    recette_test = Recette(
        id= uuid4(),
        nom = "Test",
        description = "Ceci est une recette test.",
        temps_preparation = 1,
        nombre_repas = 1
    )
    recette_test = sql_recipe_repo.add_recipe(recette_test)

    # Act
    sql_recipe_repo.delete_recipe(recette_test.id)

    # Assert
    assert sql_recipe_repo.find_by_id(recette_test.id) is None

    conn.close()

def test_sql_delete_recipe_pour_recette_absente_du_repository():
    # Arrange
    conn = db_connect.get_connection()
    sql_recipe_repo = SqlRecipeRepository(conn)
    nouvelle_recette = Recette(
        id = uuid4(),
        nom = "Salade de fraises",
        description = "Des fraises coupées en morceaux avec du sucre.",
        temps_preparation = 15,
        nombre_repas = 1)
    
    # Act / Assert
    with pytest.raises(ValueError):
        sql_recipe_repo.delete_recipe(nouvelle_recette.id)

    conn.close()