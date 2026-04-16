from backend.application.orchestrator import MenuOrchestrator
from backend.application.timeslotsgenerator import TimeSlotGenerator
from backend.tests.test_objects import timeslots
from backend.domain.generator import MealBlockGenerator
from backend.domain.planner import MenuPlanner
from backend.domain.menu import Menu
from backend.tests.fakes.fake_repository import FakeRecipeRepository
from backend.tests.test_objects import recipes
from backend.domain.editor import MenuEditor
from backend.tests.test_objects import menus


def test_orchestrator_in_nominal_case():
    # Arrange
    recipes_list = [
        recipes.one_meal_recipe(),
        recipes.one_meal_recipe_2(),
        recipes.one_meal_recipe_3(),
        recipes.one_meal_recipe_4(),
        recipes.two_meals_recipe(),
        recipes.two_meals_recipe_2(),
        recipes.three_meals_recipe(),
        recipes.three_meals_recipe_2(),
    ]
    repository = FakeRecipeRepository(recipes_list)
    mealblock_generator = MealBlockGenerator(repository)
    menu_planner = MenuPlanner()
    menu_editor = MenuEditor()
    timeslot_generator = TimeSlotGenerator()
    orchestrator = MenuOrchestrator(
        mealblock_generator, menu_planner, menu_editor, timeslot_generator
    )

    # Act
    result = orchestrator.generate_menu()

    # Assert
    assert result.success is True
    assert isinstance(result.menu, Menu)
    assert result.menu.is_stable() is True
    assert result.menu.is_complete(14) is True
    assert result.message == "Menu successfully created"


def test_orchestrator_with_insufficient_repository():
    # Arrange
    recipes_list = [
        recipes.one_meal_recipe(),
        recipes.one_meal_recipe_2(),
        recipes.one_meal_recipe_3(),
        recipes.one_meal_recipe_4(),
        recipes.two_meals_recipe(),
    ]
    repository = FakeRecipeRepository(recipes_list)
    mealblock_generator = MealBlockGenerator(repository)
    menu_planner = MenuPlanner()
    menu_editor = MenuEditor()
    timeslot_generator = TimeSlotGenerator()
    orchestrator = MenuOrchestrator(
        mealblock_generator, menu_planner, menu_editor, timeslot_generator
    )

    # Act
    result = orchestrator.generate_menu()

    # Assert
    assert result.success is False
    assert result.menu is None
    assert result.message == "Unable to create menu with the available recipes"


def test_reroll_by_orchestrator_in_nominal_case_for_length_one_mealblock():
    # Arrange
    menu = menus.menu_for_reroll()
    target_timeslot = timeslots.monday_lunch()
    recipes_list = [recipes.one_meal_recipe_3()]
    repository = FakeRecipeRepository(recipes_list)
    generator = MealBlockGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    timeslot_generator = TimeSlotGenerator()
    orchestrator = MenuOrchestrator(generator, planner, editor, timeslot_generator)

    # Act
    result = orchestrator.reroll_timeslot(menu, target_timeslot)

    # Assert
    assert menu.is_stable() is True
    assert menu.get_mealblock(target_timeslot).recipe_snapshot == recipes_list[0]
    assert result.success is True
    assert isinstance(result.menu, Menu)
    assert result.message == "Meal replaced successfully"


def test_reroll_by_orchestrator_in_nominal_case_for_mealblock_length_greater_than_one():
    # Arrange
    menu = menus.menu_for_reroll()
    target_timeslot = timeslots.tuesday_lunch()
    affected_timeslots = menu.timeslots_for(menu.get_mealblock(target_timeslot))
    recipes_list = [recipes.two_meals_recipe_2()]
    repository = FakeRecipeRepository(recipes_list)
    generator = MealBlockGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    timeslot_generator = TimeSlotGenerator()
    orchestrator = MenuOrchestrator(generator, planner, editor, timeslot_generator)

    # Act
    result = orchestrator.reroll_timeslot(menu, target_timeslot)

    # Assert
    assert menu.is_stable() is True
    assert all(
        menu.get_mealblock(timeslot).recipe_snapshot == recipes_list[0]
        for timeslot in affected_timeslots
    )
    assert result.success is True
    assert isinstance(result.menu, Menu)
    assert result.message == "Meal replaced successfully"


def test_reroll_by_orchestrator_on_unplanned_timeslot():
    # Arrange
    menu = menus.menu_for_reroll()
    initial_menu_timeslots = menu.planned_timeslots()
    initial_menu_representation = dict()
    for timeslot in initial_menu_timeslots:
        initial_menu_representation[timeslot] = menu.get_mealblock(timeslot)
    target_timeslot = timeslots.friday_lunch()
    recipes_list = [recipes.one_meal_recipe_3()]
    repository = FakeRecipeRepository(recipes_list)
    generator = MealBlockGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    timeslot_generator = TimeSlotGenerator()
    orchestrator = MenuOrchestrator(generator, planner, editor, timeslot_generator)

    # Act
    result = orchestrator.reroll_timeslot(menu, target_timeslot)

    # Assert
    assert result.success is False
    assert isinstance(result.menu, Menu)
    assert result.message == "Unable to replace meal with available recipes"
    assert menu.is_stable() is True
    assert menu.is_complete(len(initial_menu_timeslots)) is True
    assert all(
        menu.get_mealblock(timeslot) == initial_menu_representation[timeslot]
        for timeslot in menu.planned_timeslots()
    )


def test_reroll_by_orchestrator_with_insufficient_repository_under_reroll_constraints():
    # Arrange
    menu = menus.menu_for_reroll()
    initial_menu_timeslots = menu.planned_timeslots()
    initial_menu_representation = dict()
    for timeslot in initial_menu_timeslots:
        initial_menu_representation[timeslot] = menu.get_mealblock(timeslot)
    target_timeslot = timeslots.monday_lunch()
    recipes_list = [
        menu.get_mealblock(target_timeslot).recipe_snapshot,
        recipes.two_meals_recipe_2(),
    ]
    repository = FakeRecipeRepository(recipes_list)
    generator = MealBlockGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    timeslot_generator = TimeSlotGenerator()
    orchestrator = MenuOrchestrator(generator, planner, editor, timeslot_generator)

    # Act
    result = orchestrator.reroll_timeslot(menu, target_timeslot)

    # Assert
    assert result.success is False
    assert isinstance(result.menu, Menu)
    assert (
        result.message
        == "Unable to replace meal with available recipes"
    )
    assert menu.is_stable() is True
    assert menu.is_complete(len(initial_menu_timeslots)) is True
    assert all(
        menu.get_mealblock(timeslot) == initial_menu_representation[timeslot]
        for timeslot in menu.planned_timeslots()
    )
