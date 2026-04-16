from backend.domain.mealblock import MealBlock
from backend.domain.timeslot import TimeSlot
from backend.domain.menu import Menu


class MenuEditor:
    def reroll(
        self, menu: Menu, target_timeslot: TimeSlot, new_mealblock: MealBlock
    ) -> None:
        if not menu.is_planned(target_timeslot):
            raise ValueError("Cannot reroll an unplanned timeslot")

        if new_mealblock.length < 1:
            raise ValueError("New mealblock length must be greater than 0.")

        old_mealblock = menu.get_mealblock(target_timeslot)

        if old_mealblock == new_mealblock:
            raise ValueError("New mealblock is identical to the current mealblock")

        if menu.has_mealblock(new_mealblock):
            raise ValueError("New mealblock is already present in the menu")

        if old_mealblock.length != new_mealblock.length:
            raise ValueError(
                "New mealblock must have the same length as the current mealblock"
            )

        affected_timeslots = menu.timeslots_for(old_mealblock)
        if len(affected_timeslots) != old_mealblock.length:
            raise ValueError("Mealblock length does not match its assigned timeslots")

        for timeslot in affected_timeslots:
            menu.delete_mealblock(timeslot)

        for timeslot in affected_timeslots:
            menu.add_mealblock(timeslot, new_mealblock)

        if not menu.is_stable():
            raise ValueError("Menu is not stable after reroll")
