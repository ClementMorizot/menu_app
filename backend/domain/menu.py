# domain/menu.py

from typing import Dict
from backend.domain.timeslot import TimeSlot
from backend.domain.mealblock import MealBlock


class Menu:
    def __init__(self):
        self._planning: Dict[TimeSlot, MealBlock] = {}

    @property
    def planning(self) -> Dict[TimeSlot, MealBlock]:
        return self._planning.copy()

    def add_mealblock(self, timeslot: TimeSlot, mealblock: MealBlock) -> None:
        if timeslot in self._planning:
            raise ValueError("Timeslot already planned.")
        self._planning[timeslot] = mealblock

    def replace_mealblock(self, timeslot: TimeSlot, new_mealblock: MealBlock) -> None:
        if timeslot not in self._planning:
            raise ValueError("Timeslot not planned")

        self._planning[timeslot] = new_mealblock

    def is_planned(self, timeslot: TimeSlot) -> bool:
        return timeslot in self._planning

    def delete_mealblock(self, timeslot: TimeSlot) -> None:
        if timeslot not in self._planning:
            raise ValueError("Timeslot not planned")
        del self._planning[timeslot]

    def get_mealblock(self, timeslot: TimeSlot) -> MealBlock:
        if timeslot not in self._planning:
            raise ValueError("Timeslot not planned")
        return self._planning[timeslot]

    def has_mealblock(self, mealblock: MealBlock) -> bool:
        return mealblock in self._planning.values()

    def timeslots_for(self, mealblock: MealBlock) -> list[TimeSlot]:
        timeslots = []
        for timeslot, b in self._planning.items():
            if b == mealblock:
                timeslots.append(timeslot)
        return timeslots

    def planned_timeslots(self) -> list[TimeSlot]:
        timeslots = []
        for c in self._planning.keys():
            timeslots.append(c)

        return timeslots

    def is_complete(self, expected_timeslots: int) -> bool:
        return len(self._planning) == expected_timeslots

    def can_replace(self, timeslot: TimeSlot, new_mealblock: MealBlock) -> bool:
        if not self.is_planned(timeslot):
            return False
        if self.has_mealblock(new_mealblock):
            return False
        return True

    def is_length_consistent(self) -> bool:
        for mealblock in self.get_unique_mealblocks():
            if len(self.timeslots_for(mealblock)) != mealblock.length:
                return False
        return True

    def get_unique_mealblocks(self) -> list[MealBlock]:
        unique_mealblocks = []
        for mealblock in self._planning.values():
            if mealblock not in unique_mealblocks:
                unique_mealblocks.append(mealblock)

        return unique_mealblocks

    def total_meals(self) -> int:
        return sum(mealblock.length for mealblock in self.get_unique_mealblocks())

    def is_stable(self) -> bool:
        return (
            len(self._planning) == self.total_meals()
        ) and self.is_length_consistent()
