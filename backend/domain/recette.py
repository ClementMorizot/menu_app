# domain/recette.py

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True) # Immutable data class
class Recette:
    id: UUID
    nom: str
    description : str
    temps_preparation : int
    nombre_repas: int