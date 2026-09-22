from tests.test_objects import mealblocks, timeslots
from tests.test_objects import menus
from backend.domain.editor import MenuEditor
import pytest


def test_reroll_replaces_all_current_block_occurrences():
    # Arrange
    menu = menus.menu_with_two_length_2_mealblock()
    target_timeslot = timeslots.monday_lunch()
    new_mealblock = mealblocks.length_2_mealblock_3()
    unaffected_mealblock = menu.get_mealblock(timeslots.tuesday_lunch())
    editor = MenuEditor()

    # Act
    editor.reroll(menu, target_timeslot, new_mealblock)

    # Assert
    assert menu.is_stable() is True
    assert menu.get_mealblock(timeslots.monday_lunch()) == new_mealblock
    assert menu.get_mealblock(timeslots.monday_dinner()) == new_mealblock
    assert menu.get_mealblock(timeslots.tuesday_lunch()) == unaffected_mealblock
    assert menu.get_mealblock(timeslots.tuesday_dinner()) == unaffected_mealblock


def test_reroll_raises_error_if_timeslot_is_not_planned():
    # Arrange
    menu = menus.menu_with_two_length_2_mealblock()
    target_timeslot = timeslots.friday_lunch()
    new_mealblock = mealblocks.length_2_mealblock_3()
    editor = MenuEditor()

    # Act / Assert
    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)


def test_reroll_raises_error_for_mealblock_length_smaller_than_1():
    # Arrange
    menu = menus.menu_with_two_length_2_mealblock()
    target_timeslot = timeslots.monday_lunch()
    new_mealblock = mealblocks.zero_length_mealblock()
    editor = MenuEditor()

    # Act / Assert
    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)


def test_reroll_raises_error_if_new_mealblock_is_current_mealblock():
    # Arrange
    menu = menus.menu_with_two_length_2_mealblock()
    target_timeslot = timeslots.monday_lunch()
    current_mealblock = menu.get_mealblock(target_timeslot)
    new_mealblock = current_mealblock
    editor = MenuEditor()

    # Act / Assert
    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)


def test_reroll_raises_error_if_new_mealblock_is_already_in_menu():
    # Arrange
    menu = menus.menu_for_reroll()
    target_timeslot = timeslots.tuesday_dinner()
    new_mealblock = menu.get_mealblock(timeslots.monday_lunch())
    editor = MenuEditor()

    # Act / Assert
    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)


def test_reroll_raises_error_for_different_lengths_between_new_and_current_mealblocks():
    # Arrange
    menu = menus.menu_with_two_length_2_mealblock()
    target_timeslot = timeslots.monday_lunch()
    new_mealblock = mealblocks.length_1_mealblock()
    editor = MenuEditor()

    # Act / Assert
    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)


def test_reroll_raises_error_if_current_mealblock_is_incomplete_in_menu():
    # Arrange
    menu = menus.unstable_menu_with_incomplete_mealblock()
    target_timeslot = timeslots.monday_dinner()
    new_mealblock = mealblocks.length_2_mealblock_3()
    editor = MenuEditor()

    # Act / Assert
    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)


def snapshot_menu(menu):
    return {
        timeslot: menu.get_mealblock(timeslot) for timeslot in menu.planned_timeslots()
    }


def test_reroll_does_not_modify_menu_if_timeslot_is_not_planned():
    menu = menus.menu_with_two_length_2_mealblock()
    initial_snapshot = snapshot_menu(menu)
    target_timeslot = timeslots.friday_lunch()
    new_mealblock = mealblocks.length_2_mealblock_3()
    editor = MenuEditor()

    with pytest.raises(ValueError):
        editor.reroll(menu, target_timeslot, new_mealblock)

    assert snapshot_menu(menu) == initial_snapshot
