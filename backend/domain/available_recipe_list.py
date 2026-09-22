from backend.domain.recipe import Recipe
from backend.domain.repositories import RecipeRepository
from backend.domain.recipe_exclusions import RecipeExclusions

class AvailableRecipeList:

    def __init__(self, recipe_repository: RecipeRepository, recipe_exclusions: RecipeExclusions):
        self._recipe_repository = recipe_repository
        self._recipe_exclusions = recipe_exclusions

    def generate_available_recipe_list(self) -> list[Recipe]:
        return [
            recipe
            for recipe in self._recipe_repository.list_recipes()
            if not self._recipe_exclusions.is_excluded(recipe.id)
        ]