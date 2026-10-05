from tests.fakes.fake_ingredient_repository import FakeIngredientRepository
import tests.test_objects.ingredients as ing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from uuid import UUID

api = FastAPI()

class IngredientResponse(BaseModel):
    ingredient_name: str
    ingredient_unit: str
    ingredient_id: UUID

@api.get("/ingredients")
def read_ingredients() -> list[IngredientResponse]:
    output = []
    ingredients = [
            ing.cream(),
            ing.garlic(),
            ing.pasta(),
            ing.sugar()
        ]
    for ingredient in ingredients:
        output.append({
            "ingredient_name": ingredient.name,
            "ingredient_unit": ingredient.standard_unit.value,
            "ingredient_id": ingredient.id
        })

    return output

@api.get("/ingredients/{ingredient_id}")
def find_ingredient_by_id(ingredient_id: UUID)->IngredientResponse:
    ingredients = [
                ing.cream(),
                ing.garlic(),
                ing.pasta(),
                ing.sugar()
            ]

    for ingredient in ingredients:
        if ingredient.id == ingredient_id:
            return IngredientResponse(
            ingredient_name= ingredient.name,
            ingredient_unit= ingredient.standard_unit.value,
            ingredient_id= ingredient.id
            )
    raise HTTPException(status_code=404, detail="Ingredient not found")
