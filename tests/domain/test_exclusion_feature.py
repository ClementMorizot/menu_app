import pytest
from uuid import uuid4
from backend.domain.user_exclusions import UserExclusions
from backend.domain.system_exclusions import SystemExclusions
from backend.domain.recipe_exclusions import RecipeExclusions
from backend.domain.available_recipe_list import AvailableRecipeList
from backend.domain.recipe import Recipe
from tests.fakes.fake_recipe_repository import FakeRecipeRepository

# UserExclusions tests

def test_add_user_exclusion():
    exclusions = UserExclusions()
    recipe_id = uuid4()

    exclusions.add_user_exclusion(recipe_id)

    assert exclusions.contains_recipe(recipe_id)
    assert exclusions.list_all_user_exclusions() == {recipe_id}

def test_add_duplicate_user_exclusions():
    exclusions = UserExclusions()
    recipe_id = uuid4()

    exclusions.add_user_exclusion(recipe_id)
    exclusions.add_user_exclusion(recipe_id)

    assert exclusions.contains_recipe(recipe_id)
    assert exclusions.list_all_user_exclusions() == {recipe_id}

def test_remove_user_exclusion():
    exclusions = UserExclusions()
    recipe1_id = uuid4()
    recipe2_id = uuid4()
    exclusions.add_user_exclusion(recipe1_id)
    exclusions.add_user_exclusion(recipe2_id)

    exclusions.remove_user_exclusion(recipe1_id)

    assert not exclusions.contains_recipe(recipe1_id)
    assert exclusions.contains_recipe(recipe2_id)

def test_remove_unknown_user_exclusion_raises_error():
    exclusions = UserExclusions()

    with pytest.raises(ValueError):
        exclusions.remove_user_exclusion(uuid4())

def test_list_user_exclusions_returns_copy():
    exclusions = UserExclusions()
    recipe_id = uuid4()
    exclusions.add_user_exclusion(recipe_id)

    returned_exclusions = exclusions.list_all_user_exclusions()
    returned_exclusions.clear()

    assert exclusions.contains_recipe(recipe_id)

# SystemExclusions tests

def test_add_system_exclusion():
    exclusions = SystemExclusions()
    recipe_id = uuid4()

    exclusions.add_system_exclusion(recipe_id)

    assert exclusions.contains_recipe(recipe_id)
    assert exclusions.list_all_system_exclusions() == {recipe_id}

def test_add_duplicate_system_exclusions():
    exclusions = SystemExclusions()
    recipe_id = uuid4()

    exclusions.add_system_exclusion(recipe_id)
    exclusions.add_system_exclusion(recipe_id)

    assert exclusions.contains_recipe(recipe_id)
    assert exclusions.list_all_system_exclusions() == {recipe_id}

def test_remove_system_exclusion():
    exclusions = SystemExclusions()
    recipe1_id = uuid4()
    recipe2_id = uuid4()
    exclusions.add_system_exclusion(recipe1_id)
    exclusions.add_system_exclusion(recipe2_id)

    exclusions.remove_system_exclusion(recipe1_id)

    assert not exclusions.contains_recipe(recipe1_id)
    assert exclusions.contains_recipe(recipe2_id)

def test_remove_unknown_system_exclusion_raises_error():
    exclusions = SystemExclusions()

    with pytest.raises(ValueError):
        exclusions.remove_system_exclusion(uuid4())

def test_list_system_exclusions_returns_copy():
    exclusions = SystemExclusions()
    recipe_id = uuid4()
    exclusions.add_system_exclusion(recipe_id)

    returned_exclusions = exclusions.list_all_system_exclusions()
    returned_exclusions.clear()

    assert exclusions.contains_recipe(recipe_id)

def test_clear_system_exclusions():
    exclusions = SystemExclusions()
    recipe1_id = uuid4()
    recipe2_id = uuid4()
    exclusions.add_system_exclusion(recipe1_id)
    exclusions.add_system_exclusion(recipe2_id)

    exclusions.clear()

    assert exclusions.list_all_system_exclusions() == set()

def test_clear_empty_system_exclusions():
    exclusions = SystemExclusions()

    exclusions.clear()

    assert exclusions.list_all_system_exclusions() == set()

# RecipeExclusions tests
@pytest.mark.parametrize(
    "is_user_excluded, is_system_excluded, expected_result",
    [
        (False, False, False),
        (True,  False, True),
        (False, True,  True),
        (True,  True,  True),
    ],
)
def test_exhaustive_is_excluded(
    is_user_excluded,
    is_system_excluded,
    expected_result,
):
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()
    test_id = uuid4()

    if is_user_excluded:
        user_exclusions.add_user_exclusion(test_id)

    if is_system_excluded:
        system_exclusions.add_system_exclusion(test_id)

    exclusion_list = RecipeExclusions(
        user_exclusions,
        system_exclusions,
    )

    assert exclusion_list.is_excluded(test_id) == expected_result

@pytest.mark.parametrize(
    "is_user_excluded, is_system_excluded, expected_result",
    [
        (False, False, set()),
        (True,  False, {"USER"}),
        (False, True,  {"SYSTEM"}),
        (True,  True,  {"USER", "SYSTEM"}),
    ],
)
def test_get_exhaustive_exclusion_reasons(
    is_user_excluded,
    is_system_excluded,
    expected_result,
):
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()
    test_id = uuid4()

    if is_user_excluded:
        user_exclusions.add_user_exclusion(test_id)

    if is_system_excluded:
        system_exclusions.add_system_exclusion(test_id)

    exclusion_list = RecipeExclusions(
        user_exclusions,
        system_exclusions,
    )

    assert exclusion_list.get_exclusion_reasons(test_id) == expected_result

# AvailableRecipeList tests

def test_generate_available_recipe_list_with_no_exclusions():
    recipe = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    repository = FakeRecipeRepository([recipe])
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusions)
    available_recipes = AvailableRecipeList(repository, recipe_exclusions)

    result = available_recipes.generate_available_recipe_list()

    assert result == [recipe]

def test_generate_available_recipe_list_with_exclusions_from_one_source():
    recipe1 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe2 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe3 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    repository = FakeRecipeRepository([recipe1, recipe2, recipe3])
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()

    user_exclusions.add_user_exclusion(recipe2.id)

    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusions)
    available_recipes = AvailableRecipeList(repository, recipe_exclusions)

    result = available_recipes.generate_available_recipe_list()

    assert result == [recipe1, recipe3]

def test_generate_available_recipe_list_with_exclusion_from_both_sources():
    recipe1 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe2 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe3 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe4 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    repository = FakeRecipeRepository([recipe1, recipe2, recipe3, recipe4])
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()

    user_exclusions.add_user_exclusion(recipe2.id)
    system_exclusions.add_system_exclusion(recipe3.id)

    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusions)
    available_recipes = AvailableRecipeList(repository, recipe_exclusions)

    result = available_recipes.generate_available_recipe_list()

    assert result == [recipe1, recipe4]

def test_generate_available_recipe_list_with_common_exclusion():
    recipe1 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe2 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe3 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    repository = FakeRecipeRepository([recipe1, recipe2, recipe3])
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()

    user_exclusions.add_user_exclusion(recipe2.id)
    system_exclusions.add_system_exclusion(recipe2.id)

    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusions)
    available_recipes = AvailableRecipeList(repository, recipe_exclusions)

    result = available_recipes.generate_available_recipe_list()

    assert result == [recipe1, recipe3]

def test_generate_available_recipe_list_with_all_recipes_excluded_returns_empty_list():
    recipe1 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    recipe2 = Recipe(uuid4(), "Test recipe", "Test description", 45, 1)
    repository = FakeRecipeRepository([recipe1, recipe2])
    user_exclusions = UserExclusions()
    system_exclusions = SystemExclusions()

    user_exclusions.add_user_exclusion(recipe1.id)
    system_exclusions.add_system_exclusion(recipe2.id)

    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusions)
    available_recipes = AvailableRecipeList(repository, recipe_exclusions)

    result = available_recipes.generate_available_recipe_list()

    assert result == []
