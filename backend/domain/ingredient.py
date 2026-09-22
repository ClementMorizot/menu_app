from dataclasses import dataclass
from uuid import UUID
from backend.domain.units import Unit

@dataclass(frozen=True)
class Ingredient:
    id: UUID
    name: str
    standard_unit: Unit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

@dataclass(frozen=True)
class NewIngredient:
    name: str
    standard_unit: Unit