from backend.domain.timeslot import TimeSlot


# General factory
def make_timeslot(day: str, meal_time: str) -> TimeSlot:
    return TimeSlot(day=day, meal_time=meal_time)


# Normal timeslots
def monday_lunch() -> TimeSlot:
    return TimeSlot(day="monday", meal_time="lunch")


def monday_dinner() -> TimeSlot:
    return TimeSlot(day="monday", meal_time="dinner")


def tuesday_lunch() -> TimeSlot:
    return TimeSlot(day="tuesday", meal_time="lunch")


def tuesday_dinner() -> TimeSlot:
    return TimeSlot(day="tuesday", meal_time="dinner")


def wednesday_lunch() -> TimeSlot:
    return TimeSlot(day="wednesday", meal_time="lunch")


def wednesday_dinner() -> TimeSlot:
    return TimeSlot(day="wednesday", meal_time="dinner")


def thursday_lunch() -> TimeSlot:
    return TimeSlot(day="thursday", meal_time="lunch")


def thursday_dinner() -> TimeSlot:
    return TimeSlot(day="thursday", meal_time="dinner")


def friday_lunch() -> TimeSlot:
    return TimeSlot(day="friday", meal_time="lunch")


def friday_dinner() -> TimeSlot:
    return TimeSlot(day="friday", meal_time="dinner")


def saturday_lunch() -> TimeSlot:
    return TimeSlot(day="saturday", meal_time="lunch")


def saturday_dinner() -> TimeSlot:
    return TimeSlot(day="saturday", meal_time="dinner")


def sunday_lunch() -> TimeSlot:
    return TimeSlot(day="sunday", meal_time="lunch")


def sunday_dinner() -> TimeSlot:
    return TimeSlot(day="sunday", meal_time="dinner")


# Unusable timeslots
def invalid_day_timeslot() -> TimeSlot:
    return TimeSlot(day="mondayy", meal_time="lunch")


def invalid_meal_time_timeslot() -> TimeSlot:
    return TimeSlot(day="monday", meal_time="morning")


def empty_day_timeslot() -> TimeSlot:
    return TimeSlot(day="", meal_time="lunch")


def empty_meal_time_timeslot() -> TimeSlot:
    return TimeSlot(day="monday", meal_time="")
