from tests.test_objects import recipes
from backend.domain.mealblock import MealBlock
from backend.domain.generator import MealBlockGenerator
from tests.fakes.fake_recipe_repository import FakeRecipeRepository
from backend.domain.user_exclusions import UserExclusions
from backend.domain.system_exclusions import SystemExclusions
from backend.domain.recipe_exclusions import RecipeExclusions
from backend.domain.available_recipe_list import AvailableRecipeList
import pytest

# _create_mealblock(recipe) tests

def test_create_mealblock_returns_same_length_mealblock_as_recipe_meal_count():
    # Arrange
    recipe = recipes.two_meals_recipe()
    repository = FakeRecipeRepository([recipe])
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act
    mealblock = generator._create_mealblock(recipe)

    # Assert
    assert mealblock.recipe_snapshot == recipe
    assert mealblock.length == recipe.number_meals

@pytest.mark.parametrize(
    "recipe_factory, expected_length",
    [
        (recipes.one_meal_recipe, 1),
        (recipes.two_meals_recipe, 2),
        (recipes.maximum_meals_recipe, 14),
        (recipes.zero_meal_recipe, 0),
        (recipes.negative_meal_recipe, -1),
    ],
)
def test_create_mealblock_returns_correct_mealblock_length_for_multiple_meal_counts(
    recipe_factory, expected_length
):
    recipe = recipe_factory()
    repository = FakeRecipeRepository([recipe])
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    mealblock = generator._create_mealblock(recipe)

    assert mealblock.length == expected_length

# generate_mealblocks(meal_count) tests

def test_generate_mealblocks_when_repository_provides_the_exact_amount_of_recipes():
    # Arrange
    meal_count = 3
    recipe_1 = recipes.one_meal_recipe()
    recipe_2 = recipes.two_meals_recipe()
    repository = FakeRecipeRepository([recipe_1, recipe_2])
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act
    mealblocks_list = generator.generate_mealblocks(meal_count)

    # Assert

    # 1. sum is correct
    assert sum(mb.length for mb in mealblocks_list) == meal_count

    # 2. only one use per recipe
    ids = [mb.recipe_snapshot.id for mb in mealblocks_list]
    assert len(ids) == len(set(ids))

    # 3. check instances
    assert all(isinstance(mb, MealBlock) for mb in mealblocks_list)

    # 4. mealblocks created from recipe pool
    recipes_ids = {recipe_1.id, recipe_2.id}
    assert all(mb.recipe_snapshot.id in recipes_ids for mb in mealblocks_list)

def test_generate_mealblocks_when_repository_is_empty():
    # Arrange
    meal_count = 1
    repository = FakeRecipeRepository([])
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act / Assert
    with pytest.raises(ValueError):
        generator.generate_mealblocks(meal_count)

def test_generate_mealblocks_when_repository_is_insufficient():
    # Arrange
    meal_count = 14
    recipe_1 = recipes.one_meal_recipe()
    recipe_2 = recipes.two_meals_recipe()
    repository = FakeRecipeRepository([recipe_1, recipe_2])
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act / Assert
    with pytest.raises(ValueError):
        generator.generate_mealblocks(meal_count)

def test_generate_mealblocks_for_a_full_week():
    # Arrange
    meal_count = 14
    recipe_1 = recipes.one_meal_recipe()
    recipe_1_bis = recipes.one_meal_recipe_2()
    recipe_1_ter = recipes.one_meal_recipe_3()
    recipe_1_quater = recipes.one_meal_recipe_4()
    recipe_2 = recipes.two_meals_recipe()
    recipe_2_bis = recipes.two_meals_recipe_2()
    recipe_3 = recipes.three_meals_recipe()
    recipe_3_bis = recipes.three_meals_recipe_2()
    recipes_list = [
        recipe_1,
        recipe_1_bis,
        recipe_1_ter,
        recipe_1_quater,
        recipe_2,
        recipe_2_bis,
        recipe_3,
        recipe_3_bis,
    ]
    repository = FakeRecipeRepository(recipes_list)
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act
    mealblocks_list = generator.generate_mealblocks(meal_count)

    # Assert

    # 1. check sum
    assert sum(mb.length for mb in mealblocks_list) == meal_count

    # 2. only one use per recipe
    ids = [mb.recipe_snapshot.id for mb in mealblocks_list]
    assert len(ids) == len(set(ids))

    # 3. check instances
    assert all(isinstance(mb, MealBlock) for mb in mealblocks_list)

    # 4. mealblocks created from recipe pool
    recipes_ids = {recipe.id for recipe in recipes_list}
    assert all(mb.recipe_snapshot.id in recipes_ids for mb in mealblocks_list)

def test_generate_mealblocks_for_only_one_block():
    # Arrange
    meal_count = 3
    recipe = recipes.three_meals_recipe()
    repository = FakeRecipeRepository([recipe])
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act
    mealblocks_list = generator.generate_mealblocks(meal_count)

    # Assert

    # 1. check sum
    assert mealblocks_list[0].length == meal_count

    # 2. check recipe
    assert mealblocks_list[0].recipe_snapshot == recipe

    # 3. check instances
    assert all(isinstance(mb, MealBlock) for mb in mealblocks_list)

    # 4. count mealblock = 1
    assert len(mealblocks_list) == 1

def test_generate_mealblocks_ignores_excluded_recipes():
    # Arrange
    meal_count = 2
    recipe_1 = recipes.one_meal_recipe()
    recipe_2 = recipes.one_meal_recipe_2()
    recipe_3 = recipes.one_meal_recipe_3()
    repository = FakeRecipeRepository([recipe_1, recipe_2, recipe_3])
    user_exclusions = UserExclusions()
    user_exclusions.add_user_exclusion(recipe_1.id)
    system_exclusion = SystemExclusions()
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act
    mealblocks_list = generator.generate_mealblocks(meal_count)

    # Assert
    generated_recipe_ids = {
        block.recipe_snapshot.id
        for block in mealblocks_list
    }

    assert recipe_1.id not in generated_recipe_ids
    assert generated_recipe_ids == {recipe_2.id, recipe_3.id}

# generate_replacement_mealblock tests

def test_generate_replacement_mealblock_with_minimum_viable_repository():
    # Arrange
    recipe_1 = recipes.one_meal_recipe()
    recipe_1_bis = recipes.one_meal_recipe_2()
    recipe_2 = recipes.two_meals_recipe()
    recipes_list = [recipe_1, recipe_1_bis, recipe_2]
    repository = FakeRecipeRepository(recipes_list)
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    system_exclusion.add_system_exclusion(recipe_1.id)
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)
    mealblock_length = 1

    # Act
    new_mealblock = generator.generate_replacement_mealblock(
        mealblock_length
    )

    # Assert
    assert isinstance(new_mealblock, MealBlock)
    assert new_mealblock.length == mealblock_length
    assert new_mealblock.recipe_snapshot == recipe_1_bis


def test_generate_replacement_mealblock_chooses_allowed_recipe_between_many_in_repository():
    # Arrange
    recipe_1 = recipes.one_meal_recipe()
    recipe_1_bis = recipes.one_meal_recipe_2()
    recipe_1_ter = recipes.one_meal_recipe_3()
    recipes_list = [recipe_1, recipe_1_bis, recipe_1_ter]
    repository = FakeRecipeRepository(recipes_list)
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    system_exclusion.add_system_exclusion(recipe_1.id)
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)

    # Act
    new_mealblock = generator.generate_replacement_mealblock(1)

    # Assert
    assert new_mealblock.length == 1
    assert new_mealblock.recipe_snapshot in [recipe_1_bis, recipe_1_ter]
    assert new_mealblock.recipe_snapshot not in [recipe_1]


def test_generate_replacement_mealblock_with_length_less_than_1():
    # Arrange
    recipe_1 = recipes.one_meal_recipe()
    recipe_1_bis = recipes.one_meal_recipe_2()
    recipe_2 = recipes.one_meal_recipe_3()
    recipes_list = [recipe_1, recipe_1_bis, recipe_2]
    repository = FakeRecipeRepository(recipes_list)
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    system_exclusion.add_system_exclusion(recipe_1.id)
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)
    mealblock_length = 0

    # Act / assert
    with pytest.raises(ValueError):
        generator.generate_replacement_mealblock(mealblock_length)


def test_generate_replacement_mealblock_without_allowed_recipes_in_repository():
    # Arrange
    recipe_1 = recipes.one_meal_recipe()
    recipe_1_bis = recipes.one_meal_recipe_2()
    recipe_2 = recipes.two_meals_recipe()
    recipes_list = [recipe_1, recipe_1_bis, recipe_2]
    repository = FakeRecipeRepository(recipes_list)
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    system_exclusion.add_system_exclusion(recipe_1.id)
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)
    mealblock_length = max(recipe.number_meals for recipe in recipes_list) + 1

    # Act / assert
    with pytest.raises(ValueError):
        generator.generate_replacement_mealblock(mealblock_length)


def test_generate_replacement_mealblock_raises_when_matching_recipe_is_excluded():
    # Arrange
    recipe_1 = recipes.one_meal_recipe()
    recipe_1_bis = recipes.one_meal_recipe_2()
    recipe_2 = recipes.two_meals_recipe()
    recipes_list = [recipe_1, recipe_1_bis, recipe_2]
    repository = FakeRecipeRepository(recipes_list)
    user_exclusions = UserExclusions()
    system_exclusion = SystemExclusions()
    system_exclusion.add_system_exclusion(recipe_2.id)
    recipe_exclusions = RecipeExclusions(user_exclusions, system_exclusion)
    recipe_list = AvailableRecipeList(repository, recipe_exclusions)
    generator = MealBlockGenerator(recipe_list)
    mealblock_length = 2

    # Act / assert
    with pytest.raises(ValueError):
        generator.generate_replacement_mealblock(mealblock_length)
