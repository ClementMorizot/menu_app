from dataclasses import dataclass
from backend.domain.menu import Menu
from backend.domain.generator import MealBlockGenerator
from backend.domain.planner import MenuPlanner
from backend.domain.editor import MenuEditor
from backend.domain.timeslot import TimeSlot
from backend.application.timeslotsgenerator import TimeSlotGenerator


@dataclass
class MenuOrchestratorResult:
    success: bool
    menu: Menu | None
    message: str


class MenuOrchestrator:
    def __init__(
        self,
        menu_generator: MealBlockGenerator,
        menu_planner: MenuPlanner,
        menu_editor: MenuEditor,
        timeslots_generator: TimeSlotGenerator,
    ) -> None:
        self._menu_generator = menu_generator
        self._menu_planner = menu_planner
        self._menu_editor = menu_editor
        self._timeslots_generator = timeslots_generator

    def generate_menu(self) -> MenuOrchestratorResult:
        meal_count = 14

        try:
            timeslots = self._timeslots_generator.generate_timeslots(meal_count)
            mealblocks = self._menu_generator.generate_mealblocks(meal_count)
            menu = self._menu_planner.plan(timeslots, mealblocks)

            return MenuOrchestratorResult(
                success=True, menu=menu, message="Menu successfully created"
            )

        except ValueError:
            return MenuOrchestratorResult(
                success=False,
                menu=None,
                message="Unable to create menu with the available recipes",
            )

        except Exception:
            return MenuOrchestratorResult(
                success=False,
                menu=None,
                message="Technical error occurred during menu generation",
            )

    def reroll_timeslot(
        self,
        menu: Menu,
        target_timeslot: TimeSlot,
    ) -> MenuOrchestratorResult:

        try:
            current_bloc = menu.get_mealblock(target_timeslot)
            excluded_recipes = [
                bloc.recipe_snapshot for bloc in menu.get_unique_mealblocks()
            ]
            new_mealblock = self._menu_generator.generate_replacement_mealblock(
                current_bloc.length, excluded_recipes
            )
            self._menu_editor.reroll(menu, target_timeslot, new_mealblock)

            return MenuOrchestratorResult(
                success=True, menu=menu, message="Meal replaced successfully"
            )

        except ValueError:
            return MenuOrchestratorResult(
                success=False,
                menu=menu,
                message="Unable to replace meal with available recipes",
            )

        except Exception:
            return MenuOrchestratorResult(
                success=False,
                menu=menu,
                message="Technical error occurred during meal replacement",
            )
