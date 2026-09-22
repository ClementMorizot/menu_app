from backend.application.unit_of_work import UnitOfWork
from backend.infrastructure.sql_ingredient_repository import SqlIngredientRepository
from backend.infrastructure.sql_recipe_repository import SqlRecipeRepository
from backend.infrastructure.sql_recipe_ingredient_repository import SqlRecipeIngredientRepository

class SqlUnitOfWork(UnitOfWork):
    def __init__(self, conn):
        self._conn = conn
        self.recipes = SqlRecipeRepository(conn)
        self.ingredients = SqlIngredientRepository(conn)
        self.recipe_ingredients = SqlRecipeIngredientRepository(conn)

        self._committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is not None:
                self.rollback()
            elif not self._committed:
                self.rollback()
        finally:
            self._conn.close()

    def commit(self) -> None:
        self._conn.commit()
        self._committed = True

    def rollback(self) -> None:
        self._conn.rollback()