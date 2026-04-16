# domain/bloc.py

from dataclasses import dataclass
from backend.domain.recipe import Recipe


@dataclass(frozen=True)  # immutable data class
class MealBlock:
    recipe_snapshot: Recipe
    length: int  # number of timeslots covered
