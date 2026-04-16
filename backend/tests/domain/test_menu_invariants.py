from backend.tests.test_objects import mealblocks
from backend.tests.test_objects import timeslots
from backend.domain.menu import Menu
import pytest


class TestMenuStability:
    def test_empty_menu_is_stable(self):
        # Arrange
        menu = Menu()

        # Assert
        assert menu.is_stable() is True

    def test_menu_can_be_stable_even_if_it_is_not_full_week(self):
        # Arrange
        timeslot_list = [
            timeslots.monday_lunch(),
            timeslots.monday_dinner(),
            timeslots.tuesday_lunch(),
        ]
        mealblock_1 = mealblocks.length_1_mealblock()
        mealblock_2 = mealblocks.length_2_mealblock()
        menu = Menu()

        # Act
        menu.add_mealblock(timeslot_list[0], mealblock_1)
        menu.add_mealblock(timeslot_list[1], mealblock_2)
        menu.add_mealblock(timeslot_list[2], mealblock_2)

        # Assert
        assert menu.is_stable() is True
        assert all(menu.is_planned(timeslot) is True for timeslot in timeslot_list)

        # Arrange
        timeslot_list = [
            timeslots.monday_lunch(),
            timeslots.monday_dinner(),
            timeslots.tuesday_lunch(),
        ]
        mealblock_1 = mealblocks.length_1_mealblock()
        mealblock_2 = mealblocks.length_2_mealblock()
        menu = Menu()

        # Act
        menu.add_mealblock(timeslot_list[0], mealblock_1)
        menu.add_mealblock(timeslot_list[1], mealblock_2)

        # Assert
        assert menu.is_stable() is False

    def test_menu_is_not_stable_if_mealblock_is_overrepresented(self):
        # Arrange
        timeslot_list = [timeslots.monday_lunch(), timeslots.monday_dinner()]
        mealblock_1 = mealblocks.length_1_mealblock()
        menu = Menu()

        # Act
        menu.add_mealblock(timeslot_list[0], mealblock_1)
        menu.add_mealblock(timeslot_list[1], mealblock_1)

        # Assert
        assert menu.is_stable() is False


class TestMenuCompleteness:
    def test_menu_with_missing_timeslot_is_not_complete(self):
        # Arrange
        timeslot_list = [
            timeslots.monday_lunch(),
            timeslots.monday_dinner(),
            timeslots.tuesday_lunch(),
            timeslots.wednesday_lunch(),
        ]
        mealblock_1 = mealblocks.length_1_mealblock()
        mealblock_2 = mealblocks.length_2_mealblock()
        menu = Menu()

        # Act
        menu.add_mealblock(timeslot_list[0], mealblock_1)
        menu.add_mealblock(timeslot_list[1], mealblock_2)
        menu.add_mealblock(timeslot_list[2], mealblock_2)

        # Assert
        assert menu.is_complete(len(timeslot_list)) is False


class TestMenuAddProtection:
    def test_add_mealblock_on_planned_timeslot_raises_error(self):
        # Arrange
        timeslot_list = [timeslots.monday_lunch()]
        mealblock_1 = mealblocks.length_1_mealblock()
        mealblock_2 = mealblocks.length_2_mealblock()
        menu = Menu()

        # Act
        menu.add_mealblock(timeslot_list[0], mealblock_1)

        # Assert
        with pytest.raises(ValueError):
            menu.add_mealblock(timeslot_list[0], mealblock_2)
