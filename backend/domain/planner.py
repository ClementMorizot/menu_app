from backend.domain.mealblock import MealBlock
from backend.domain.timeslot import TimeSlot
from backend.domain.menu import Menu


class MenuPlanner:
    def plan(self, timeslots: list[TimeSlot], mealblocks: list[MealBlock]) -> Menu:
        timeslots_count = len(timeslots)
        meals_count = sum(mealblock.length for mealblock in mealblocks)

        if meals_count != timeslots_count:
            raise ValueError(
                f"Mealblock lengths sum to {meals_count}, but {timeslots_count} timeslots were provided."
            )

        for mealblock in mealblocks:
            if mealblock.length <= 0:
                raise ValueError(
                    f"Invalid mealblock length: {mealblock.length}. Length must be greater than 0."
                )

        menu = Menu()
        i = 0

        for mealblock in mealblocks:
            for _ in range(mealblock.length):
                # i is validated by checking meals_count == timeslots_count
                menu.add_mealblock(timeslots[i], mealblock)
                i += 1

        if not menu.is_stable():
            raise ValueError("Menu is not stable after planning.")

        return menu
