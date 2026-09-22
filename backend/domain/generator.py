# domain/generator.py
import random
from backend.domain.available_recipe_list import AvailableRecipeList
from backend.domain.mealblock import MealBlock
from backend.domain.recipe import Recipe


class MealBlockGenerator:
    def __init__(self, available_recipe_list: AvailableRecipeList):
        self._available_recipe_list = available_recipe_list

    def _create_mealblock(self, recipe: Recipe) -> MealBlock:
        # block snapshot (V1) : recipe is stored as it is
        return MealBlock(recipe_snapshot=recipe, length=recipe.number_meals)

    def generate_mealblocks(self, number_meals: int) -> list[MealBlock]:
        recipes = self._available_recipe_list.generate_available_recipe_list()
        if not recipes:
            raise ValueError("No recipe available")

        blocks: list[MealBlock] = []
        total = 0

        max_tries = 5000
        tries = 0

        used_recipe_ids = set()

        while total < number_meals:
            tries += 1
            if tries > max_tries:
                raise ValueError(
                    f"Unable to generate mealblocks list covering exactly {number_meals} meals."
                )

            recipe = random.choice(recipes)

            if recipe.id in used_recipe_ids:
                continue

            block_length = recipe.number_meals
            if total + block_length > number_meals:
                continue

            mealblock = self._create_mealblock(recipe)
            blocks.append(mealblock)
            used_recipe_ids.add(recipe.id)
            total += block_length

        return blocks

    def generate_replacement_mealblock(
        self, block_length: int
    ) -> MealBlock:
        if block_length < 1:
            raise ValueError("Mealblock length must be greater than 0.")

        available_recipes = self._available_recipe_list.generate_available_recipe_list()
        recipes_candidates = [
            recipe
            for recipe in available_recipes
            if recipe.number_meals == block_length
        ]

        if not recipes_candidates:
            raise ValueError(
                f"No available recipe allows creating a {block_length} long block."
            )

        selected_recipe = random.choice(recipes_candidates)
        return self._create_mealblock(selected_recipe)
