from backend.application.ingredient_service import IngredientApplicationService
from fastapi import Request

def ingredient_service(request: Request) -> IngredientApplicationService:
    return IngredientApplicationService(request.app.state.uow_factory)