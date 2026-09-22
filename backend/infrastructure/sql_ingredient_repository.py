from uuid import UUID

from psycopg import Connection
from backend.domain.repositories import IngredientRepository
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.domain.units import Unit


class SqlIngredientRepository(IngredientRepository):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def _get_unit_id(self, unit: Unit):
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM unites
                WHERE nom = %s;
                """,
                (unit.value,),
            )
            row = cur.fetchone()

        if row is None:
            raise ValueError(f"Unit not found in database: {unit.value}")

        return row[0]

    def list_ingredients(self) -> list[Ingredient]:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT i.id, i.nom, u.nom
                FROM ingredients AS i
                JOIN unites AS u
                    ON i.unite_standard_id = u.id
                ORDER BY i.nom;
                """
            )
            result = cur.fetchall()

        return [
            Ingredient(
                id=id_,
                name=name,
                standard_unit=Unit(standard_unit),
            )
            for id_, name, standard_unit in result
        ]

    def find_by_id(self, ingredient_id: UUID) -> Ingredient | None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT i.id, i.nom, u.nom
                FROM ingredients AS i
                JOIN unites AS u
                    ON i.unite_standard_id = u.id
                WHERE i.id = %s;
                """,
                (ingredient_id,),
            )
            result = cur.fetchone()

        if result is None:
            return None

        id_, name, standard_unit = result

        return Ingredient(
            id=id_,
            name=name,
            standard_unit=Unit(standard_unit),
        )

    def add_ingredient(self, new_ingredient: NewIngredient) -> Ingredient:
        unit_id = self._get_unit_id(new_ingredient.standard_unit)

        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ingredients (nom, unite_standard_id)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (
                    new_ingredient.name,
                    unit_id,
                ),
            )
            row = cur.fetchone()

        if row is None:
            raise RuntimeError("INSERT failed: no id returned")

        return Ingredient(
            id=row[0],
            name=new_ingredient.name,
            standard_unit=new_ingredient.standard_unit,
        )

    def update_ingredient(self, ingredient: Ingredient) -> None:
        unit_id = self._get_unit_id(ingredient.standard_unit)

        with self._conn.cursor() as cur:
            cur.execute(
                """
                UPDATE ingredients
                SET nom = %s,
                    unite_standard_id = %s
                WHERE id = %s;
                """,
                (
                    ingredient.name,
                    unit_id,
                    ingredient.id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Ingredient not found: {ingredient.id}")

    def delete_ingredient(self, ingredient_id: UUID) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM ingredients
                WHERE id = %s;
                """,
                (ingredient_id,),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Ingredient not found: {ingredient_id}")