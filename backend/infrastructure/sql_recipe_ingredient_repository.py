from backend.domain.measured_ingredients import RecipeIngredient
from backend.domain.ingredient import Ingredient
from backend.domain.repositories import RecipeIngredientRepository
from backend.domain.units import Unit
from decimal import Decimal
from psycopg import Connection
from uuid import UUID

class SqlRecipeIngredientRepository(RecipeIngredientRepository):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def get_ingredients_of_recipe(self, recipe_id: UUID) -> list[RecipeIngredient]:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    i.id,
                    i.nom,
                    standard_unit.nom,
                    recipe_unit.nom,
                    ri.quantite
                FROM recette_ingredients ri
                JOIN ingredients i
                    ON i.id = ri.ingredient_id
                JOIN unites recipe_unit
                    ON recipe_unit.id = ri.unite_id
                JOIN unites standard_unit
                    ON standard_unit.id = i.unite_standard_id
                WHERE ri.recette_id = %s
                ORDER BY i.nom;

                """,
                (recipe_id,),
            )
            rows = cur.fetchall()

        return [
            RecipeIngredient(
                ingredient=Ingredient(
                    id=ingredient_id,
                    name=ingredient_name,
                    standard_unit=Unit(standard_unit),
                ),
                unit=Unit(unit),
                quantity=Decimal(str(quantity)),
            )
            for ingredient_id, ingredient_name, standard_unit, unit, quantity in rows
        ]

    def add_recipe_ingredient(
        self,
        recipe_id: UUID,
        recipe_ingredient: RecipeIngredient,
    ) -> None:

        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO recette_ingredients (
                    recette_id,
                    ingredient_id,
                    unite_id,
                    quantite
                )
                VALUES (
                    %s,
                    %s,
                    (SELECT id FROM unites WHERE nom = %s),
                    %s
                );
                """,
                (
                    recipe_id,
                    recipe_ingredient.ingredient.id,
                    recipe_ingredient.unit.value,
                    recipe_ingredient.quantity,
                ),
            )

    def update_recipe_ingredients(
        self,
        recipe_id: UUID,
        recipe_ingredients: list[RecipeIngredient],
    ) -> None:

        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM recettes WHERE id = %s",
                (recipe_id,),
            )
            if cur.fetchone() is None:
                raise ValueError(f"Update failed. Recipe {recipe_id} not found")

        self.delete_all_recipe_ingredients_for_recipe(recipe_id)
        for recipe_ingredient in recipe_ingredients:
            self.add_recipe_ingredient(recipe_id, recipe_ingredient)

    def delete_recipe_ingredient(
        self,
        recipe_id: UUID,
        ingredient_id: UUID,
    ) -> None:

        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM recette_ingredients
                WHERE
                    recette_id = %s
                    AND ingredient_id = %s;
                """,
                (
                    recipe_id,
                    ingredient_id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(
                    f"Recipe ingredient not found: "
                    f"recipe={recipe_id}, ingredient={ingredient_id}"
                )

    def delete_all_recipe_ingredients_for_recipe(
        self,
        recipe_id: UUID,
    ) -> None:

        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM recette_ingredients
                WHERE
                    recette_id = %s;
                """,
                (
                    recipe_id,
                ),
            )