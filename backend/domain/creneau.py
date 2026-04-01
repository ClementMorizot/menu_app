# domain/creneau.py

from dataclasses import dataclass


@dataclass(frozen=True) # Immutable data class
class Creneau:
    jour: str
    moment: str  # "midi" ou "soir"