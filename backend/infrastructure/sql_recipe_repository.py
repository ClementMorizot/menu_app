from domain.recette import Recette
from psycopg import Connection
from uuid import UUID

class SqlRecipeRepository:
    
    def __init__(self,conn : Connection) -> None:
        self._conn = conn

    def find_by_id(self, recette_id : UUID) -> Recette | None:

        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM recettes WHERE id = %s;", (recette_id,))
            result = cur.fetchone()

        if result is None:
            return None
        
        id_, nom, description, temps_preparation, nombre_repas = result
        return Recette(id=id_, nom=nom, description = description, temps_preparation = temps_preparation, nombre_repas=nombre_repas)
    
    def list_recipes(self) -> list[Recette]:

        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM recettes ORDER BY nom")
            result = cur.fetchall()

        return [
        Recette(id=id_, nom=nom, description = description, temps_preparation = temps_preparation, nombre_repas=nombre_repas)
        for id_, nom, description, temps_preparation, nombre_repas in result
        ]
    
    def add_recipe(self, recette: Recette) -> Recette:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO recettes (nom, description, temps_preparation, nombre_repas)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    recette.nom,
                    recette.description,
                    recette.temps_preparation,
                    recette.nombre_repas,
                ),
            )
            row = cur.fetchone()

            if row is None:
                raise RuntimeError("INSERT failed: no id returned")
            
            generated_id = row[0]

        self._conn.commit()

        return Recette(
            id=generated_id,
            nom=recette.nom,
            description=recette.description,
            temps_preparation=recette.temps_preparation,
            nombre_repas=recette.nombre_repas,
        )

    def update_recipe(self, recette: Recette) -> None:

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
                    recette.nom,
                    recette.description,
                    recette.temps_preparation,
                    recette.nombre_repas,
                    recette.id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Recette introuvable : {recette.id}")

        self._conn.commit()

    def delete_recipe(self, recette_id: UUID) -> None:

        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM recettes
                WHERE id = %s;
                """,
                (
                    recette_id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(f"Recette introuvable : {recette_id}")

        self._conn.commit()