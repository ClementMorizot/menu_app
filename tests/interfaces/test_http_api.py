from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from backend.domain.units import Unit
from backend.domain.ingredient import Ingredient
from backend.api.app import create_app
from tests.fakes.test_fake_unit_of_work import FakeUnitOfWork
from tests.fakes.fake_ingredient_repository import FakeIngredientRepository, FailingIngredientRepository
from tests.fakes.fake_recipe_repository import FakeRecipeRepository, FailingRecipeRepository
from tests.fakes.fake_recipe_ingredient_repository import FakeRecipeIngredientRepository, FailingRecipeIngredientRepository
import tests.test_objects.ingredients as ing
import pytest

def test_read_ingredients():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)

    response = client.get("/ingredients")

    list_ingredient = ing_repo.list_ingredients()
    assert response.status_code == 200
    assert len(response.json()) == len(list_ingredient)
    for ingredient in list_ingredient:
        expected = {"ingredient_name": ingredient.name,
                    "ingredient_unit": ingredient.standard_unit.value,
                    "ingredient_id": str(ingredient.id)}
        assert expected in response.json()

def test_read_ingredients_when_empty_returns_empty_list():
    uow = FakeUnitOfWork(
            recipes = FakeRecipeRepository(),
            ingredients = FakeIngredientRepository(),
            recipe_ingredients = FakeRecipeIngredientRepository()
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    response = client.get("/ingredients")
    assert response.status_code == 200
    assert response.json() == []

def test_find_ingredient_by_id_nominal_case():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)    
    ingredient = ing.cream()
    response = client.get(f"/ingredients/{ingredient.id}")

    assert response.status_code == 200
    assert response.json()["ingredient_name"] == ingredient.name
    assert response.json()["ingredient_unit"] == ingredient.standard_unit.value
    assert UUID(response.json()["ingredient_id"]) == ingredient.id

def test_read_ingredients_returns_500_on_unexpected_error():
    ing_repo = FailingIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/ingredients")
    assert response.status_code == 500

def test_find_ingredient_by_unknown_id():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)    
    response = client.get(f"/ingredients/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"

def test_find_ingredient_by_id_with_non_id_input():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)    
    response = client.get("/ingredients/garbage")

    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert response.json()["detail"] != []

def test_find_ingredient_by_id_returns_500_on_unexpected_error():
    ing_repo = FailingIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get(f"/ingredients/{uuid4()}")
    assert response.status_code == 500

def test_create_ingredient():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    response = client.post(
        "/ingredients",
        json= {
                "ingredient_name": "Farine",
                "ingredient_unit": "g"
            }
        )

    assert response.status_code == 201
    assert response.json()["ingredient_name"] == "Farine"
    assert response.json()["ingredient_unit"] == Unit.g.value
    ingredient_id = UUID(response.json()["ingredient_id"])
    assert ingredient_id in [ingredient.id for ingredient in ing_repo.list_ingredients()]
    assert len(ing_repo.list_ingredients()) == 5
    assert uow.committed is True

def test_created_ingredient_can_be_retrieved():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    post_response = client.post(
        "/ingredients",
        json= {
                "ingredient_name": "Farine",
                "ingredient_unit": "g"
            }
        )
    assert post_response.status_code == 201
    assert uow.committed is True

    ingredient_id = UUID(post_response.json()["ingredient_id"])
    get_response = client.get(f"/ingredients/{ingredient_id}")
    assert get_response.status_code == 200
    assert get_response.json()["ingredient_name"] == "Farine"
    assert get_response.json()["ingredient_unit"] == Unit.g.value
    assert UUID(get_response.json()["ingredient_id"]) == ingredient_id

testdata = [
    ({"ingredient_name": "", "ingredient_unit": "g"}, 422),
    ({"ingredient_name": "   ", "ingredient_unit": "g"}, 422),
    ({"ingredient_name": "Valid test name", "ingredient_unit": "litres"}, 422),
    ({"ingredient_unit": "g"}, 422),
    ({"ingredient_name": "Valid test name"}, 422),
    ({"ingredient_name": None, "ingredient_unit": "g"}, 422),
    ({"ingredient_name": "Valid test name", "ingredient_unit": None}, 422),
]

@pytest.mark.parametrize("payload, expected_status", testdata)
def test_create_ingredient_with_invalid_user_inputs(payload, expected_status):
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    response = client.post("/ingredients", json= payload)
    assert response.status_code == expected_status
    assert len(ing_repo.list_ingredients()) == 4
    assert uow.committed is False

def test_create_ingredient_with_failing_repository_returns_error_500():
    ing_repo = FailingIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post(
        "/ingredients",
        json= {
                "ingredient_name": "Farine",
                "ingredient_unit": "g"
            }
        )

    assert response.status_code == 500
    assert uow.committed is False

def test_update_ingredient():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    test_id = ing.cream().id
    response = client.put(f"/ingredients/{test_id}",
                          json= {
                            "ingredient_name": "Test ingredient",
                            "ingredient_unit": "unit"
                          })

    assert response.status_code == 200
    assert response.json()["ingredient_name"] == "Test ingredient"
    assert response.json()["ingredient_unit"] == Unit.unit.value
    assert UUID(response.json()["ingredient_id"]) == test_id
    updated = ing_repo.find_by_id(test_id)
    assert updated is not None
    assert updated.name == "Test ingredient"
    assert updated.standard_unit == Unit.unit
    assert uow.committed is True

def test_update_unknown_ingredient_id_returns_error_404():
    ing_repo = FakeIngredientRepository()
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    response = client.put(f"/ingredients/{uuid4()}",
                          json= {
                            "ingredient_name": "Test ingredient",
                            "ingredient_unit": "unit"
                          })

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"
    assert uow.committed is False

def test_update_ingredient_with_invalid_id_type_returns_error_422():
    ing_repo = FakeIngredientRepository()
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    test_id = "garbage"
    response = client.put(f"/ingredients/{test_id}",
                          json= {
                            "ingredient_name": "Test ingredient",
                            "ingredient_unit": "unit"
                          })

    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert response.json()["detail"] != []
    assert uow.committed is False

@pytest.mark.parametrize("payload, expected_output", testdata)
def test_update_ingredient_with_invalid_user_inputs(payload, expected_output):
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)

    response = client.put(f"/ingredients/{ing.cream().id}",
                          json= payload)

    assert response.status_code == expected_output
    assert uow.committed is False

def test_update_ingredient_with_failing_repository_returns_error_500():
    ing_repo = FailingIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app, raise_server_exceptions=False)
    test_id = ing.cream().id
    response = client.put(f"/ingredients/{test_id}",
                          json= {
                            "ingredient_name": "Test ingredient",
                            "ingredient_unit": "unit"
                          })

    assert response.status_code == 500
    assert uow.committed is False

def test_delete_ingredien():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)

    response = client.delete(f"/ingredients/{ing.cream().id}")

    assert response.status_code == 204
    assert len(ing_repo.list_ingredients()) == 3
    assert ing.cream() not in ing_repo.list_ingredients()
    assert response.content == b""
    assert uow.committed is True

def test_delete_unknown_ingredient_returns_error_404():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    response = client.delete(f"/ingredients/{uuid4()}")    

    assert response.status_code == 404
    assert len(ing_repo.list_ingredients()) == 4
    assert response.json()["detail"] == "Ingredient not found"
    assert uow.committed is False

def test_delete_ingredient_with_invalid_id_type_returns_error_422():
    ing_repo = FakeIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app)
    response = client.delete("/ingredients/garbage")    

    assert response.status_code == 422
    assert len(ing_repo.list_ingredients()) == 4
    assert isinstance(response.json()["detail"], list)
    assert response.json()["detail"] != []
    assert uow.committed is False

def test_delete_ingredient_with_failing_repository_returns_error_500():
    ing_repo = FailingIngredientRepository([
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ])
    rec_repo = FakeRecipeRepository()
    rec_ing_repo = FakeRecipeIngredientRepository()
    uow = FakeUnitOfWork(
            recipes = rec_repo,
            ingredients = ing_repo,
            recipe_ingredients = rec_ing_repo
        )
    app = create_app(lambda: uow)
    client = TestClient(app, raise_server_exceptions=False)

    response = client.delete(f"/ingredients/{ing.cream().id}")

    assert response.status_code == 500
    assert uow.committed is False