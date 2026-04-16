from backend.domain.recipe import Recipe
from psycopg import Connection
from uuid import UUID


class SqlRecipeRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def find_by_id(self, recette_id: UUID) -> Recipe | None:

        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM recettes WHERE id = %s;", (recette_id,))
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
            cur.execute("SELECT * FROM recettes ORDER BY nom")
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

    def add_recipe(self, recette: Recipe) -> Recipe:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO recettes (nom, description, temps_preparation, nombre_repas)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    recette.name,
                    recette.description,
                    recette.cooking_time,
                    recette.number_meals,
                ),
            )
            row = cur.fetchone()

            if row is None:
                raise RuntimeError("INSERT failed: no id returned")

            generated_id = row[0]

        self._conn.commit()

        return Recipe(
            id=generated_id,
            name=recette.name,
            description=recette.description,
            cooking_time=recette.cooking_time,
            number_meals=recette.number_meals,
        )

    def update_recipe(self, recette: Recipe) -> None:

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
                    recette.name,
                    recette.description,
                    recette.cooking_time,
                    recette.number_meals,
                    recette.id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Recipe not found : {recette.id}")

        self._conn.commit()

    def delete_recipe(self, recette_id: UUID) -> None:

        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM recettes
                WHERE id = %s;
                """,
                (recette_id,),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Recipe not found : {recette_id}")

        self._conn.commit()
