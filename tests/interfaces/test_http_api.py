from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from backend.domain.units import Unit
import backend.api.ingredient_routes as routes
import tests.test_objects.ingredients as ing
from unittest.mock import patch
import pytest

api = routes.api
client = TestClient(api)

@pytest.fixture(autouse=True)
def ingredients_data():
    ingredients_copy = routes._INGREDIENTS.copy()
    routes._INGREDIENTS[:] = [
        ing.cream(),
        ing.garlic(),
        ing.pasta(),
        ing.sugar()
    ]

    yield

    routes._INGREDIENTS[:] = ingredients_copy.copy()

def test_read_ingredients():
    response = client.get("/ingredients")

    assert response.status_code == 200
    assert len(response.json()) == len(routes._INGREDIENTS)
    for ingredient in routes._INGREDIENTS:
        expected = {"ingredient_name": ingredient.name,
                    "ingredient_unit": ingredient.standard_unit.value,
                    "ingredient_id": str(ingredient.id)}
        assert expected in response.json()

def test_read_ingredients_when_empty_returns_empty_list():
    routes._INGREDIENTS.clear()
    response = client.get("/ingredients")
    assert response.status_code == 200
    assert response.json() == []

def test_find_ingredient_by_id_nominal_case():
    ingredient = routes._INGREDIENTS[0]
    response = client.get(f"/ingredients/{ingredient.id}")

    assert response.status_code == 200
    assert response.json()["ingredient_name"] == ingredient.name
    assert response.json()["ingredient_unit"] == ingredient.standard_unit.value
    assert UUID(response.json()["ingredient_id"]) == ingredient.id

def test_read_ingredients_returns_500_on_unexpected_error():
    client = TestClient(api, raise_server_exceptions=False)
    with patch("backend.api.ingredient_routes._INGREDIENTS", None):
        response = client.get("/ingredients")
    assert response.status_code == 500

def test_find_ingredient_by_unknown_id():
    response = client.get(f"/ingredients/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"

def test_find_ingredient_by_id_with_non_id_input():
    response = client.get("/ingredients/garbage")

    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert response.json()["detail"] != []

def test_find_ingredient_by_id_returns_500_on_unexpected_error():
    client = TestClient(api, raise_server_exceptions=False)
    with patch("backend.api.ingredient_routes._INGREDIENTS", None):
        response = client.get(f"/ingredients/{uuid4()}")
    assert response.status_code == 500

def test_create_ingredient():
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
    UUID(response.json()["ingredient_id"])
    assert len(routes._INGREDIENTS) == 5

def test_created_ingredient_can_be_retrieved():
    post_response = client.post(
        "/ingredients",
        json= {
                "ingredient_name": "Farine",
                "ingredient_unit": "g"
            }
        )
    assert post_response.status_code == 201
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
    response = client.post("/ingredients", json= payload)
    assert response.status_code == expected_status
    assert len(routes._INGREDIENTS) == 4