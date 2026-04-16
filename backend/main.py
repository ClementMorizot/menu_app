from backend.application.orchestrator import MenuOrchestrator
from backend.application.timeslotsgenerator import TimeSlotGenerator
from backend.domain.generator import MealBlockGenerator
from backend.domain.planner import MenuPlanner
from backend.domain.editor import MenuEditor
from backend.domain.menu import Menu
from backend.infrastructure.db_connection import get_connection
from backend.infrastructure.sql_recipe_repository import SqlRecipeRepository


def display_menu(menu: Menu) -> None:
    # Terminal diplay before v1
    timeslot = menu.planned_timeslots()
    print("Generated menu: ")
    for timeslot in timeslot:
        bloc = menu.get_mealblock(timeslot)
        print(f"{timeslot.day} {timeslot.meal_time} : {bloc.recipe_snapshot.name}")


def main() -> None:
    connection = None

    try:
        connection = get_connection()
        repository = SqlRecipeRepository(connection)

        mealblock_generator = MealBlockGenerator(repository)
        menu_planner = MenuPlanner()
        menu_editor = MenuEditor()
        timeslot_generator = TimeSlotGenerator()

        orchestrator = MenuOrchestrator(
            mealblock_generator, menu_planner, menu_editor, timeslot_generator
        )

        result = orchestrator.generate_menu()

        if not result.success:
            print(result.message)
            return

        print(result.message)
        print()

        if result.menu is not None:
            display_menu(result.menu)

    except Exception as e:
        print(f"Erreur technique : {e}")

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()
