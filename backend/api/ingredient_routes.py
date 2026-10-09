from tests.fakes.fake_ingredient_repository import FakeIngredientRepository
from typing import Annotated
import tests.test_objects.ingredients as ing
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, StringConstraints
from uuid import UUID, uuid4
from backend.domain.units import Unit
from backend.domain.ingredient import Ingredient

_INGREDIENTS = [
                ing.cream(),
                ing.garlic(),
                ing.pasta(),
                ing.sugar()
            ]

api = FastAPI()

class IngredientResponse(BaseModel):
    ingredient_name: str
    ingredient_unit: str
    ingredient_id: UUID

class IngredientCreateRequest(BaseModel):
    ingredient_name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    ingredient_unit: Unit

@api.get("/ingredients")
def read_ingredients() -> list[IngredientResponse]:
    output = []
    for ingredient in _INGREDIENTS:
        output.append({
            "ingredient_name": ingredient.name,
            "ingredient_unit": ingredient.standard_unit.value,
            "ingredient_id": ingredient.id
        })

    return output

@api.get("/ingredients/{ingredient_id}",
    responses= {404: {"description":"Ingredient not found"}})
def find_ingredient_by_id(ingredient_id: UUID)->IngredientResponse:
    for ingredient in _INGREDIENTS:
        if ingredient.id == ingredient_id:
            return IngredientResponse(
            ingredient_name= ingredient.name,
            ingredient_unit= ingredient.standard_unit.value,
            ingredient_id= ingredient.id
            )
    raise HTTPException(status_code=404, detail="Ingredient not found")

@api.post("/ingredients", status_code=status.HTTP_201_CREATED)
def create_ingredient(new_ingredient: IngredientCreateRequest) -> IngredientResponse:
    if new_ingredient.ingredient_name.strip() == "":
        raise HTTPException(status_code= 422, detail= "Ingredient name cannot be empty")

    #ingredient_service create_ingredient() simulation
    ingredient = Ingredient(
        id= uuid4(),
        name= new_ingredient.ingredient_name,
        standard_unit= new_ingredient.ingredient_unit
    )
    _INGREDIENTS.append(ingredient)

    return IngredientResponse(
        ingredient_name= ingredient.name,
        ingredient_unit= ingredient.standard_unit.value,
        ingredient_id= ingredient.id
    )