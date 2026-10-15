from fastapi import FastAPI
from backend.infrastructure.db_connection import get_connection
from backend.infrastructure.sql_unit_of_work import SqlUnitOfWork
import backend.api.ingredient_routes as ingredient_routes

def default_uow_factory() -> SqlUnitOfWork:
    return SqlUnitOfWork(get_connection())

def create_app(uow_factory = default_uow_factory) -> FastAPI:
    app = FastAPI()
    app.state.uow_factory = uow_factory
    app.include_router(ingredient_routes.router)
    return app
    
