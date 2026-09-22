from dataclasses import dataclass
from backend.domain.ingredient import Ingredient
from backend.domain.units import Unit
from decimal import Decimal

@dataclass(frozen=True)
class ShoppingListItem:
    ingredient : Ingredient
    unit : Unit
    quantity : Decimal

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(
                f"Recipe ingredient quantity must be positive: {self.quantity}"
            )

@dataclass(frozen=True)
class RecipeIngredient:
    ingredient : Ingredient
    unit : Unit
    quantity : Decimal

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(
                f"Recipe ingredient quantity must be positive: {self.quantity}"
            )