import pytest
from tests.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.fakes.fake_recipe_repository import FakeRecipeRepository
from tests.fakes.fake_ingredient_repository import FakeIngredientRepository
from tests.fakes.fake_recipe_ingredient_repository import FakeRecipeIngredientRepository


# ============================================================================
# Injection des repositories
# ============================================================================

def test_fake_unit_of_work_exposes_injected_repositories():
    # Arrange
    recipe_repository = FakeRecipeRepository()
    ingredient_repository = FakeIngredientRepository()
    recipe_ingredient_repository = FakeRecipeIngredientRepository()

    # Act
    uow = FakeUnitOfWork(
        recipes=recipe_repository,
        ingredients=ingredient_repository,
        recipe_ingredients=recipe_ingredient_repository,
    )

    # Assert
    assert uow.recipes is recipe_repository
    assert uow.ingredients is ingredient_repository
    assert uow.recipe_ingredients is recipe_ingredient_repository


# ============================================================================
# Context manager
# ============================================================================

def test_fake_unit_of_work_context_manager_returns_itself():
    # Arrange
    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    # Act
    with uow as active_uow:
        result = active_uow

    # Assert
    assert result is uow


# ============================================================================
# Commit
# ============================================================================

def test_fake_unit_of_work_commit_marks_uow_as_committed():
    # Arrange
    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    # Act
    uow.commit()

    # Assert
    assert uow.committed is True


# ============================================================================
# Rollback manuel
# ============================================================================

def test_fake_unit_of_work_rollback_marks_uow_as_rolled_back():
    # Arrange
    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    # Act
    uow.rollback()

    # Assert
    assert uow.rolled_back is True


# ============================================================================
# Rollback automatique sur exception
# ============================================================================

def test_fake_unit_of_work_rolls_back_when_exception_occurs():
    # Arrange
    uow = FakeUnitOfWork(
        recipes=FakeRecipeRepository(),
        ingredients=FakeIngredientRepository(),
        recipe_ingredients=FakeRecipeIngredientRepository(),
    )

    # Act / Assert
    with pytest.raises(RuntimeError):
        with uow:
            raise RuntimeError("RuntimeError")

    # Assert
    assert uow.rolled_back is True
    assert uow.committed is False