from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, StringConstraints
from uuid import UUID
from backend.domain.units import Unit
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.application.ingredient_service import IngredientApplicationService
from backend.api.dependencies import ingredient_service
from backend.domain.errors import IngredientNotFound, IngredientDuplicationError

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
)

class IngredientResponse(BaseModel):
    ingredient_name: str
    ingredient_unit: str
    ingredient_id: UUID

class IngredientPayload(BaseModel):
    ingredient_name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    ingredient_unit: Unit

@router.get("")
def read_ingredients(ias: IngredientApplicationService = Depends(ingredient_service)
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
                          ias: IngredientApplicationService = Depends(ingredient_service)
                          ) ->IngredientResponse:
    
    try :
        ingredient = ias.get_ingredient(ingredient_id)
        return IngredientResponse(
                ingredient_name = ingredient.name,
                ingredient_unit = ingredient.standard_unit.value,
                ingredient_id = ingredient.id)
    except IngredientNotFound:
        raise HTTPException(status_code=404, detail="Ingredient not found")

@router.post("", status_code=status.HTTP_201_CREATED)
def create_ingredient(input_ingredient: IngredientPayload, 
                      ias: IngredientApplicationService = Depends(ingredient_service)
                      ) -> IngredientResponse:

    new_ingredient = NewIngredient(
        name= input_ingredient.ingredient_name,
        standard_unit= input_ingredient.ingredient_unit
    )
    try:
        ingredient = ias.create_ingredient(new_ingredient)

        return IngredientResponse(
            ingredient_name= ingredient.name,
            ingredient_unit= ingredient.standard_unit.value,
            ingredient_id= ingredient.id
        )

    except IngredientDuplicationError:
        raise HTTPException(status_code= 409, detail="Ingredient name already used")

@router.put("/{ingredient_id}")
def update_ingredient(ingredient_id: UUID, 
                      input_ingredient: IngredientPayload,
                      ias: IngredientApplicationService = Depends(ingredient_service)
                    ) -> IngredientResponse:

    updated_ingredient = Ingredient(
        id= ingredient_id,
        name= input_ingredient.ingredient_name,
        standard_unit= input_ingredient.ingredient_unit
    )

    try : 
        ias.update_ingredient(updated_ingredient)
        return IngredientResponse(
            ingredient_name= updated_ingredient.name,
            ingredient_unit= updated_ingredient.standard_unit.value,
            ingredient_id = updated_ingredient.id
        )
    except IngredientNotFound:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    except IngredientDuplicationError:
        raise HTTPException(status_code=409, detail="Ingredient name already used")

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: UUID, 
                      ias: IngredientApplicationService = Depends(ingredient_service)
                    ) :
    try : 
        ias.delete_ingredient(ingredient_id)
    except IngredientNotFound:
        raise HTTPException(status_code=404, detail="Ingredient not found")