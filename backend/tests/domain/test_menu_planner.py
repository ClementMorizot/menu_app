from backend.tests.test_objects import mealblocks
from backend.tests.test_objects import timeslots
from backend.domain.menu import Menu
from backend.domain.planner import MenuPlanner
import pytest


def test_plan_returns_stable_and_complete_menu_for_minimal_case():
    # Arrange
    timeslots_list = [timeslots.monday_lunch()]
    mealblocks_list = [mealblocks.length_1_mealblock()]
    planner = MenuPlanner()

    # Act
    menu = planner.plan(timeslots_list, mealblocks_list)

    # Assert
    assert menu.is_stable()
    assert menu.is_complete(len(timeslots_list))
    assert menu.get_unique_mealblocks() == mealblocks_list
    assert menu.planned_timeslots() == timeslots_list
    assert isinstance(menu, Menu)


def test_plan_schedules_mealblocks_sequentially():
    # Arrange
    block_1 = mealblocks.length_1_mealblock()
    block_3 = mealblocks.length_3_mealblock()
    timeslots_list = [
        timeslots.monday_lunch(),
        timeslots.monday_dinner(),
        timeslots.tuesday_lunch(),
        timeslots.tuesday_dinner(),
    ]
    mealblocks_list = [block_1, block_3]
    planner = MenuPlanner()

    # Act
    menu = planner.plan(timeslots_list, mealblocks_list)

    # Assert
    assert menu.is_stable()
    assert menu.get_mealblock(timeslots_list[0]) == block_1
    assert menu.get_mealblock(timeslots_list[1]) == block_3
    assert menu.get_mealblock(timeslots_list[2]) == block_3
    assert menu.get_mealblock(timeslots_list[3]) == block_3


def test_plan_raises_error_if_mealblocks_length_sum_is_lesser_than_timeslots_count():
    # Arrange
    timeslots_list = [timeslots.monday_lunch(), timeslots.monday_dinner()]
    mealblocks_list = [mealblocks.length_1_mealblock()]
    planner = MenuPlanner()

    # Act / Assert
    with pytest.raises(ValueError):
        planner.plan(timeslots_list, mealblocks_list)


def test_plan_raises_error_if_mealblocks_length_sum_is_greater_than_timeslots_count():
    # Arrange
    timeslots_list = [timeslots.monday_lunch()]
    mealblocks_list = [mealblocks.length_2_mealblock()]
    planner = MenuPlanner()

    # Act / Assert
    with pytest.raises(ValueError):
        planner.plan(timeslots_list, mealblocks_list)


def test_plan_raises_error_if_a_mealblock_has_zero_length():
    # Arrange
    timeslots_list = [timeslots.monday_lunch()]
    mealblocks_list = [mealblocks.zero_length_mealblock()]
    planner = MenuPlanner()

    # Act / Assert
    with pytest.raises(ValueError):
        planner.plan(timeslots_list, mealblocks_list)
