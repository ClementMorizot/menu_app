from backend.application.orchestrator import MenuOrchestrator, ShoppingListOrchestrator
from backend.application.timeslotsgenerator import TimeSlotGenerator
from backend.domain.generator import MealBlockGenerator
from backend.domain.planner import MenuPlanner
from backend.domain.editor import MenuEditor
from backend.infrastructure.db_connection import get_connection
from backend.infrastructure.sql_recipe_repository import SqlRecipeRepository
from backend.infrastructure.sql_recipe_ingredient_repository import SqlRecipeIngredientRepository
from backend.domain.user_exclusions import UserExclusions
from backend.domain.system_exclusions import SystemExclusions
from backend.domain.recipe_exclusions import RecipeExclusions
from backend.domain.available_recipe_list import AvailableRecipeList
from backend.domain.shopping_list_generator import ShoppingListGenerator
from backend.application.ingredient_service import IngredientApplicationService
from backend.application.recipe_service import RecipeApplicationService
from backend.infrastructure.sql_unit_of_work import SqlUnitOfWork
import backend.ui.cli as cli

def uow_factory() -> SqlUnitOfWork:
    return SqlUnitOfWork(get_connection())

def main() -> None:
    connection = None

    try:
        connection = get_connection()

        recipe_repository = SqlRecipeRepository(connection)
        recipe_ingredient_repository = SqlRecipeIngredientRepository(connection)
        user_exclusions = UserExclusions()
        system_exclusions = SystemExclusions()
        recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusions)
        available_recipe_list = AvailableRecipeList(recipe_repository, recipe_exclusions)
        mealblock_generator = MealBlockGenerator(available_recipe_list)
        menu_planner = MenuPlanner()
        menu_editor = MenuEditor()
        timeslot_generator = TimeSlotGenerator()

        orchestrator = MenuOrchestrator(
            mealblock_generator,
            menu_planner,
            menu_editor,
            timeslot_generator,
            system_exclusions
        )

        shopping_list_generator = ShoppingListGenerator(recipe_ingredient_repository)
        shopping_list_orchestrator = ShoppingListOrchestrator(shopping_list_generator)

        recipe_service = RecipeApplicationService(uow_factory)
        ingredient_service = IngredientApplicationService(uow_factory)

        cli.run(
            orchestrator= orchestrator,
            shopping_orchestrator= shopping_list_orchestrator,
            recipe_service= recipe_service,
            ingredient_service= ingredient_service,
            user_exclusions= user_exclusions
        )

    except Exception as e:
        print(f"Technical error: {e}")

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()