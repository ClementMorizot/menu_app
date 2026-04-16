# domain/creneau.py

from dataclasses import dataclass


@dataclass(frozen=True)  # Immutable data class
class TimeSlot:
    day: str
    meal_time: str  # "lunch" or "dinner"
