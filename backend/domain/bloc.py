# domain/bloc.py

from dataclasses import dataclass
from .recette import Recette


@dataclass(frozen=True) # immutable data class
class Bloc:
    recette_snapshot: Recette
    longueur: int  # nombre de créneaux couverts