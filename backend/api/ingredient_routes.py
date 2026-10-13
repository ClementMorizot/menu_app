from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, StringConstraints
from uuid import UUID
from backend.domain.units import Unit
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.application.ingredient_service import IngredientApplicationService

def get_ingredient_service() -> IngredientApplicationService:
    raise NotImplementedError

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
)

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

@router.get("")
def read_ingredients(ias: IngredientApplicationService = Depends(get_ingredient_service)
                     ) -> list[IngredientResponse]:
    return [IngredientResponse(
        ingredient_name = ingredient.name,
        ingredient_unit = ingredient.standard_unit.value,
        ingredient_id = ingredient.id
    ) 
    for ingredient in ias.list_ingredients()]

@router.get("/{ingredient_id}",
    responses= {404: {"description":"Ingredient not found"}})
def find_ingredient_by_id(ingredient_id: UUID, 
                          ias: IngredientApplicationService = Depends(get_ingredient_service)
                          ) ->IngredientResponse:
    ingredient = ias.get_ingredient(ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return IngredientResponse(
        ingredient_name = ingredient.name,
        ingredient_unit = ingredient.standard_unit.value,
        ingredient_id = ingredient.id
    )

@router.post("", status_code=status.HTTP_201_CREATED)
def create_ingredient(input_ingredient: IngredientCreateRequest, 
                      ias: IngredientApplicationService = Depends(get_ingredient_service)
                      ) -> IngredientResponse:
    if input_ingredient.ingredient_name.strip() == "":
        raise HTTPException(status_code= 422, detail= "Ingredient name cannot be empty")

    new_ingredient = NewIngredient(
        name= input_ingredient.ingredient_name,
        standard_unit= input_ingredient.ingredient_unit
    )

    ingredient = ias.create_ingredient(new_ingredient)

    return IngredientResponse(
        ingredient_name= ingredient.name,
        ingredient_unit= ingredient.standard_unit.value,
        ingredient_id= ingredient.id
    )