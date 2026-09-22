from backend.domain.menu import Menu
from backend.domain.mealblock import MealBlock
from backend.domain.timeslot import TimeSlot

from . import mealblocks, timeslots


def empty_menu() -> Menu:
    return Menu()


def menu_from_mapping(entries: list[tuple[TimeSlot, MealBlock]]) -> Menu:
    menu = Menu()
    for timeslot, mealblock in entries:
        menu.add_mealblock(timeslot, mealblock)
    return menu


def minimal_menu() -> Menu:
    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), mealblocks.length_1_mealblock()),
        ]
    )


def incomplete_stable_menu() -> Menu:
    block_1 = mealblocks.length_1_mealblock()
    block_2 = mealblocks.length_2_mealblock()
    block_3 = mealblocks.length_3_mealblock()

    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block_1),
            (timeslots.monday_dinner(), block_2),
            (timeslots.tuesday_lunch(), block_2),
            (timeslots.tuesday_dinner(), block_3),
            (timeslots.wednesday_lunch(), block_3),
            (timeslots.wednesday_dinner(), block_3),
        ]
    )


def complete_stable_menu() -> Menu:
    block_1 = mealblocks.length_1_mealblock()
    block_2 = mealblocks.length_2_mealblock()
    block_3 = mealblocks.length_3_mealblock()
    block_1_bis = mealblocks.length_1_mealblock_2()
    block_2_bis = mealblocks.length_2_mealblock_2()
    block_3_bis = mealblocks.length_3_mealblock_2()
    block_1_ter = mealblocks.length_1_mealblock_3()
    block_2_ter = mealblocks.length_2_mealblock_3()
    block_1_quater = mealblocks.length_1_mealblock_4()

    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block_1),
            (timeslots.monday_dinner(), block_2),
            (timeslots.tuesday_lunch(), block_2),
            (timeslots.tuesday_dinner(), block_3),
            (timeslots.wednesday_lunch(), block_3),
            (timeslots.wednesday_dinner(), block_3),
            (timeslots.thursday_lunch(), block_1_bis),
            (timeslots.thursday_dinner(), block_2_bis),
            (timeslots.friday_lunch(), block_2_bis),
            (timeslots.friday_dinner(), block_3_bis),
            (timeslots.saturday_lunch(), block_1_ter),
            (timeslots.saturday_dinner(), block_2_ter),
            (timeslots.sunday_lunch(), block_2_ter),
            (timeslots.sunday_dinner(), block_1_quater),
        ]
    )


def unstable_menu_with_repeated_mealblock() -> Menu:
    block_1 = mealblocks.length_1_mealblock()
    block_2 = mealblocks.length_2_mealblock()
    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block_1),
            (timeslots.monday_dinner(), block_2),
            (timeslots.tuesday_lunch(), block_2),
            (timeslots.tuesday_dinner(), block_1),
        ]
    )


def unstable_menu_with_incomplete_mealblock() -> Menu:
    block_1 = mealblocks.length_1_mealblock()
    block_2 = mealblocks.length_2_mealblock()
    block_3 = mealblocks.length_3_mealblock()

    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block_1),
            (timeslots.monday_dinner(), block_2),
            (timeslots.tuesday_lunch(), block_2),
            (timeslots.tuesday_dinner(), block_3),
            (timeslots.wednesday_lunch(), block_3),
        ]
    )


def menu_for_reroll() -> Menu:
    block_1 = mealblocks.length_1_mealblock()
    block_2 = mealblocks.length_2_mealblock()
    block_1_bis = mealblocks.length_1_mealblock_2()

    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block_1),
            (timeslots.monday_dinner(), block_2),
            (timeslots.tuesday_lunch(), block_2),
            (timeslots.tuesday_dinner(), block_1_bis),
        ]
    )


def menu_with_one_length_3_mealblock() -> Menu:
    mealblock = mealblocks.length_3_mealblock_2()

    return menu_from_mapping(
        [
            (timeslots.tuesday_dinner(), mealblock),
            (timeslots.wednesday_lunch(), mealblock),
            (timeslots.wednesday_dinner(), mealblock),
        ]
    )


def menu_with_two_length_2_mealblock() -> Menu:
    block_1 = mealblocks.length_2_mealblock()
    block_2 = mealblocks.length_2_mealblock_2()

    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block_1),
            (timeslots.monday_dinner(), block_1),
            (timeslots.tuesday_lunch(), block_2),
            (timeslots.tuesday_dinner(), block_2),
        ]
    )

def menu_with_no_associated_ingredients():
    block = mealblocks.length_1_mealblock_4()

    return menu_from_mapping(
        [
            (timeslots.monday_lunch(), block)
        ]
    )