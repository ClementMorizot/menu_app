# domain/generator.py

from __future__ import annotations
from uuid import UUID
import random
from typing import List
from .repositories import RecipeRepository
from .bloc import Bloc
from .recette import Recette
from .creneau import Creneau
from .menu import Menu


class MenuGenerator:
    def __init__(self, recipe_repository: RecipeRepository):
        self._recipe_repository = recipe_repository

    def creer_bloc(self, recette: Recette) -> Bloc:
        # bloc snapshot (V1) : on stocke la recette telle quelle
        return Bloc(recette_snapshot=recette, longueur=recette.nombre_repas)

    def creer_liste_blocs(self, nombre_repas: int) -> List[Bloc]:
        recettes = self._recipe_repository.list_recipes()
        if not recettes:
            raise ValueError("Aucune recette disponible")

        blocs: List[Bloc] = []
        total = 0

        # Pour éviter les boucles infinies, on limite les essais.
        # (V1 simple : on tente, et si on n'y arrive pas, on échoue clairement.)
        max_essais = 5000
        essais = 0

        # Option: éviter de reprendre la même recette
        recette_ids_utilises = set()

        while total < nombre_repas:
            essais += 1
            if essais > max_essais:
                raise ValueError(
                    "Impossible de générer des blocs couvrant exactement "
                    f"{nombre_repas} repas avec les recettes disponibles."
                )

            recette = random.choice(recettes)

            # évite doublon de recette (adaptable selon tes règles)
            if recette.id in recette_ids_utilises:
                continue

            longueur = recette.nombre_repas
            if total + longueur > nombre_repas:
                continue

            bloc = self.creer_bloc(recette)
            blocs.append(bloc)
            recette_ids_utilises.add(recette.id)
            total += longueur

        return blocs

    def creer_bloc_pour_reroll(
        self,
        longueur_bloc: int,
        recettes_exclues: list[Recette]
    ) -> Bloc:
        if longueur_bloc < 1:
            raise ValueError("La longueur du bloc doit être supérieure ou égale à 1.")

        recettes_disponibles = self._recipe_repository.list_recipes()

        recettes_candidates = [
            recette
            for recette in recettes_disponibles
            if recette.nombre_repas == longueur_bloc
            and recette not in recettes_exclues
        ]

        if not recettes_candidates:
            raise ValueError(
                f"Aucune recette disponible ne permet de créer un bloc de longueur {longueur_bloc}."
            )

        recette_choisie = random.choice(recettes_candidates)
        return self.creer_bloc(recette_choisie)