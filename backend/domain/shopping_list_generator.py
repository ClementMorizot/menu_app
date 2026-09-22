from backend.domain.menu import Menu
from backend.domain.measured_ingredients import ShoppingListItem
from backend.domain.repositories import RecipeIngredientRepository
from backend.domain.unit_conversion import normalize_recipe_ingredient
from backend.domain.ingredient import Ingredient
from decimal import Decimal


class ShoppingListGenerator:

    def __init__(self, repository: RecipeIngredientRepository) -> None :
        self._repository = repository

    def generate_shopping_list(self, menu: Menu) -> list[ShoppingListItem]:

        if not menu.is_stable():
            raise ValueError("Menu is unstable")

        mealblocks = menu.get_unique_mealblocks()
        ingredient_quantities : dict[Ingredient, Decimal] = {}
        for block in mealblocks:
            block_ingredient_list = self._repository.get_ingredients_of_recipe(block.recipe_snapshot.id)

            if not block_ingredient_list:
                raise ValueError(f'Recipe has no ingredient: {block.recipe_snapshot.name}, id {block.recipe_snapshot.id}')

            for recipe_ingredient in block_ingredient_list:
                recipe_ingredient = normalize_recipe_ingredient(recipe_ingredient)
                if recipe_ingredient.ingredient in ingredient_quantities:
                    ingredient_quantities[recipe_ingredient.ingredient] += recipe_ingredient.quantity
                else:
                    ingredient_quantities[recipe_ingredient.ingredient] = recipe_ingredient.quantity

        shopping_list = [
            ShoppingListItem(ingredient, ingredient.standard_unit, quantity)
            for ingredient, quantity in ingredient_quantities.items()
            ]

        return shopping_list
