from dataclasses import dataclass
from backend.domain.menu import Menu
from backend.domain.generator import MealBlockGenerator
from backend.domain.planner import MenuPlanner
from backend.domain.editor import MenuEditor
from backend.domain.timeslot import TimeSlot
from backend.application.timeslotsgenerator import TimeSlotGenerator
from backend.domain.shopping_list_generator import ShoppingListGenerator
from backend.domain.measured_ingredients import ShoppingListItem
from backend.domain.system_exclusions import SystemExclusions

@dataclass
class MenuOrchestratorResult:
    success: bool
    menu: Menu | None
    message: str

@dataclass
class ShoppingListResult:
    success: bool
    shopping_list: list[ShoppingListItem] | None
    message: str

class MenuOrchestrator:
    def __init__(
        self,
        menu_generator: MealBlockGenerator,
        menu_planner: MenuPlanner,
        menu_editor: MenuEditor,
        timeslots_generator: TimeSlotGenerator,
        system_exclusions : SystemExclusions
    ) -> None:
        self._menu_generator = menu_generator
        self._menu_planner = menu_planner
        self._menu_editor = menu_editor
        self._timeslots_generator = timeslots_generator
        self._system_exclusions = system_exclusions

    def _sync_system_exclusions(self, menu: Menu) -> None:
        self._system_exclusions.clear()

        for block in menu.get_unique_mealblocks():
            self._system_exclusions.add_system_exclusion(
                block.recipe_snapshot.id
            )

    def generate_menu(self) -> MenuOrchestratorResult:
        meal_count = 14
        self._system_exclusions.clear()
        try:
            timeslots = self._timeslots_generator.generate_timeslots(meal_count)
            mealblocks = self._menu_generator.generate_mealblocks(meal_count)
            menu = self._menu_planner.plan(timeslots, mealblocks)
            self._sync_system_exclusions(menu)

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
            current_block = menu.get_mealblock(target_timeslot)
            new_mealblock = self._menu_generator.generate_replacement_mealblock(
                current_block.length
            )
            self._menu_editor.reroll(menu, target_timeslot, new_mealblock)
            self._sync_system_exclusions(menu)
            return MenuOrchestratorResult(
                success=True,
                menu=menu,
                message="Meal replaced successfully"
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

class ShoppingListOrchestrator:

    def __init__(self, generator: ShoppingListGenerator):
        self._generator = generator

    def generate(self, menu: Menu) -> ShoppingListResult:
        try:
            shopping_list = self._generator.generate_shopping_list(menu)

            return ShoppingListResult(
                success=True,
                message="Shopping list successfully generated.",
                shopping_list=shopping_list,
            )

        except ValueError as exc:
            return ShoppingListResult(
                success=False,
                message=str(exc),
                shopping_list=None,
            )