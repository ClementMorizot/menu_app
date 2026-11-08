from uuid import UUID

class ResourceNotFound(Exception):
    def __init__(self, resource_id: UUID, message: str) -> None:
        self.resource_id = resource_id
        super().__init__(message)


class IngredientNotFound(ResourceNotFound):
    def __init__(self, ingredient_id: UUID) -> None:
        super().__init__(
            resource_id=ingredient_id,
            message=f"Ingredient not found: {ingredient_id}",
        )


class RecipeNotFound(ResourceNotFound):
    def __init__(self, recipe_id: UUID) -> None:
        super().__init__(
            resource_id=recipe_id,
            message=f"Recipe not found: {recipe_id}",
        )

class ResourceDuplicationError(Exception):
    def __init__(self, resource_name: str, message: str) -> None:
        self.resource_name = resource_name
        super().__init__(message)

class IngredientDuplicationError(ResourceDuplicationError):
    def __init__(self, ingredient_name: str) -> None:
        super().__init__(
            resource_name = ingredient_name,
            message= f"Ingredient duplication: {ingredient_name}"
        )

class RecipeDuplicationError(ResourceDuplicationError):
    def __init__(self, recipe_name: str) -> None:
        super().__init__(
            resource_name = recipe_name,
            message = f"Recipe duplication: {recipe_name}"
        )