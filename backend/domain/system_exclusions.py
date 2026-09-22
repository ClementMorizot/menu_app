from uuid import UUID

class SystemExclusions:
    def __init__(self):
        self._data: set[UUID] = set()

    def add_system_exclusion(self, recipe_id: UUID) -> None:
        self._data.add(recipe_id)

    def remove_system_exclusion(self, recipe_id: UUID) -> None:
        if recipe_id not in self._data:
            raise ValueError("Recipe not in system exclusions")
        self._data.remove(recipe_id)

    def contains_recipe(self, recipe_id: UUID) -> bool:
        return recipe_id in self._data

    def list_all_system_exclusions(self) -> set[UUID]:
        return self._data.copy()

    def clear(self) -> None:
        self._data.clear()