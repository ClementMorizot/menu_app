from backend.domain.timeslot import TimeSlot

_TIMESLOTS = [
    ["sunday", "lunch"],
    ["sunday", "dinner"],
    ["monday", "lunch"],
    ["monday", "dinner"],
    ["tuesday", "lunch"],
    ["tuesday", "dinner"],
    ["wednesday", "lunch"],
    ["wednesday", "dinner"],
    ["thursday", "lunch"],
    ["thursday", "dinner"],
    ["friday", "lunch"],
    ["friday", "dinner"],
    ["saturday", "lunch"],
    ["saturday", "dinner"],
]


class TimeSlotGenerator:
    def generate_timeslots(self, meal_count: int) -> list[TimeSlot]:
        if meal_count < 1 or meal_count > len(_TIMESLOTS):
            raise ValueError(
                f"Meal count must be bewteen 1 and {len(_TIMESLOTS)}. Got: {meal_count}"
            )

        return [TimeSlot(day, meal_time) for day, meal_time in _TIMESLOTS[:meal_count]]
