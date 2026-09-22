from backend.domain.user_exclusions import UserExclusions
from backend.domain.system_exclusions import SystemExclusions
from uuid import UUID

class RecipeExclusions:
    def __init__(
        self,
        user_exclusions: UserExclusions,
        system_exclusions: SystemExclusions,
    ):
        self._user_exclusions = user_exclusions
        self._system_exclusions = system_exclusions

    def is_excluded(self, recipe_id: UUID) -> bool:
        return (
            self._user_exclusions.contains_recipe(recipe_id)
            or self._system_exclusions.contains_recipe(recipe_id)
        )

    def get_exclusion_reasons(self, recipe_id: UUID) -> set[str]:
        reasons = set()

        if self._user_exclusions.contains_recipe(recipe_id):
            reasons.add("USER")

        if self._system_exclusions.contains_recipe(recipe_id):
            reasons.add("SYSTEM")

        return reasons