# domain/recette.py

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)  # Immutable data class
class Recipe:
    id: UUID
    name: str
    description: str
    cooking_time: int
    number_meals: int

@dataclass(frozen=True)  # Immutable data class
class NewRecipe:
    name: str
    description: str
    cooking_time: int
    number_meals: int