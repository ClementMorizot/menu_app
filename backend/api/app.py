from fastapi import FastAPI
from backend.infrastructure.db_connection import get_connection
from backend.infrastructure.sql_unit_of_work import SqlUnitOfWork
from backend.application.ingredient_service import IngredientApplicationService
import backend.api.ingredient_routes as ingredient_routes
from backend.api.ingredient_routes import get_ingredient_service

def default_uow_factory() -> SqlUnitOfWork:
    return SqlUnitOfWork(get_connection())

def create_app(uow_factory = default_uow_factory) -> FastAPI:
    def ingredient_service() -> IngredientApplicationService:
        return IngredientApplicationService(uow_factory)
    app = FastAPI()
    app.include_router(ingredient_routes.router)
    app.dependency_overrides[get_ingredient_service] = ingredient_service
    return app
    
