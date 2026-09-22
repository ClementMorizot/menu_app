from backend.domain.recipe import Recipe, NewRecipe
from backend.domain.repositories import RecipeRepository
from psycopg import Connection
from uuid import UUID


class SqlRecipeRepository(RecipeRepository):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def find_by_id(self, recipe_id: UUID) -> Recipe | None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nom, description, temps_preparation, nombre_repas
                FROM recettes
                WHERE id = %s;
                """,
                (recipe_id,),
            )
            result = cur.fetchone()

        if result is None:
            return None

        id_, name, description, cooking_time, number_meals = result
        return Recipe(
            id=id_,
            name=name,
            description=description,
            cooking_time=cooking_time,
            number_meals=number_meals,
        )

    def list_recipes(self) -> list[Recipe]:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nom, description, temps_preparation, nombre_repas
                FROM recettes
                ORDER BY nom;
                """
            )
            result = cur.fetchall()

        return [
            Recipe(
                id=id_,
                name=name,
                description=description,
                cooking_time=cooking_time,
                number_meals=number_meals,
            )
            for id_, name, description, cooking_time, number_meals in result
        ]

    def add_recipe(self, new_recipe: NewRecipe) -> Recipe:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO recettes (nom, description, temps_preparation, nombre_repas)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    new_recipe.name,
                    new_recipe.description,
                    new_recipe.cooking_time,
                    new_recipe.number_meals,
                ),
            )
            row = cur.fetchone()

        if row is None:
            raise RuntimeError("INSERT failed: no id returned")

        return Recipe(
            id=row[0],
            name=new_recipe.name,
            description=new_recipe.description,
            cooking_time=new_recipe.cooking_time,
            number_meals=new_recipe.number_meals,
        )

    def update_recipe(self, recipe: Recipe) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                UPDATE recettes
                SET nom = %s,
                    description = %s,
                    temps_preparation = %s,
                    nombre_repas = %s
                WHERE id = %s;
                """,
                (
                    recipe.name,
                    recipe.description,
                    recipe.cooking_time,
                    recipe.number_meals,
                    recipe.id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Recipe not found: {recipe.id}")

    def delete_recipe(self, recipe_id: UUID) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM recettes
                WHERE id = %s;
                """,
                (recipe_id,),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Recipe not found: {recipe_id}")