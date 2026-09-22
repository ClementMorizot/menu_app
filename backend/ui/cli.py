
import backend.ui.cli_helpers as helpers
from backend.application.orchestrator import MenuOrchestrator, ShoppingListOrchestrator
from backend.domain.timeslot import TimeSlot
from backend.domain.menu import Menu
from backend.domain.unit_conversion import STANDARD_UNITS
from backend.domain.recipe import Recipe, NewRecipe
from backend.domain.ingredient import Ingredient, NewIngredient
from backend.application.ingredient_service import IngredientApplicationService
from backend.application.recipe_service import RecipeApplicationService
from backend.ui.cli_exclusion_list import cli_exclusion_list
from backend.domain.user_exclusions import UserExclusions


def run(
        orchestrator: MenuOrchestrator,
        shopping_orchestrator: ShoppingListOrchestrator,
        ingredient_service: IngredientApplicationService,
        recipe_service: RecipeApplicationService,
        user_exclusions: UserExclusions
        ):

    while True:
        print("\n================\n")
        print("Welcome, you currently are in the main menu.\n")
        print("1 - Generate menu\n")
        print("2 - Recipes\n")
        print("3 - Ingredients\n")
        print("4 - Exit application\n")

        state = input("> ")
        print("\n")
        if state == "1":
            cli_menu(orchestrator, shopping_orchestrator, user_exclusions, recipe_service)

        elif state == "2":
            cli_recipes(recipe_service, ingredient_service)

        elif state == "3":
            cli_ingredients(ingredient_service)

        elif state == "4":
            break

        else:
            print("Invalid input.\n")

def cli_menu(orchestrator: MenuOrchestrator, shopping_orchestrator: ShoppingListOrchestrator, user_exclusions: UserExclusions, recipe_service: RecipeApplicationService):

    current_menu: Menu | None = None

    while True:
        print("\n================\n")
        print("This is the menu service. Please choose your service.\n")
        print("1 - Manage recipe exclusion")
        print("2 - Generate weekly menu")
        print("3 - Reroll one recipe")
        print("4 - Display related grocery list")
        print("5 - Exit to main menu\n")

        state = input("> ")
        print("\n")

        if state == "1":
            cli_exclusion_list(user_exclusions, recipe_service)

        elif state == "2":
            result = orchestrator.generate_menu()
            if not result.success:
                print(result.message)
                continue
            print(result.message)
            current_menu = result.menu

            helpers.display_menu(result.menu)

        elif state == "3":

            if current_menu is None:
                print('Menu has not been generated yet. Please use service "generate menu" first.\n')
                continue

            print("Please select (one of) the associated meal of the recipe to reroll.\n")
            day_to_reroll = input("Day > ")
            meal_to_reroll = input("Meal > ")
            selected_timeslot = TimeSlot(day_to_reroll, meal_to_reroll)

            reroll_result = orchestrator.reroll_timeslot(current_menu, selected_timeslot)

            print(reroll_result.message)
            if not reroll_result.success:
                continue

            current_menu = reroll_result.menu
            helpers.display_menu(current_menu)

        elif state == "4":

            if current_menu is None:
                print('Menu has not been generated yet. Please use service "generate menu" first.\n')
                continue

            shopping_list_result = shopping_orchestrator.generate(current_menu)
            print(shopping_list_result.message)

            if shopping_list_result.success:
                helpers.display_shopping_list(shopping_list_result.shopping_list)

        elif state == "5":

            break

        else:
            print("Invalid input")

def cli_recipes(recipe_service: RecipeApplicationService, ingredient_service: IngredientApplicationService):

    while True :
        print("\n===========\n")
        print("Recipe management")
        print("1 - Display recipes")
        print("2 - Create recipe")
        print("3 - Update recipe")
        print("4 - Delete recipe")
        print("5 - Exit to main menu\n")

        state = input("> ").strip()

        if state == "1":
            list_recipes = recipe_service.list_recipes()
            helpers.display_all_recipes(list_recipes)

        elif state == "2":
            new_name = input("Recipe name > ").strip()

            if not new_name:
                print("Recipe name cannot be empty")
                continue

            new_description = input("Description > ").strip()

            try:
                new_cooking_time = int(input("Cooking time in minutes > ").strip())
                new_number_meals = int(input("Number of meals > ").strip())
            except ValueError:
                print("Invalid input")
                continue

            new_recipe = NewRecipe(
                name=new_name,
                description=new_description,
                cooking_time=new_cooking_time,
                number_meals=new_number_meals
            )

            recipe_ingredients = helpers.prompt_recipe_ingredient(ingredient_service)
            if recipe_ingredients is None:
                continue

            try:
                recipe = recipe_service.create_recipe(new_recipe, recipe_ingredients)
            except ValueError as exc:
                print(exc)
                continue

            print("Recipe successfuly created.")
            helpers.display_recipe_details(recipe, recipe_ingredients)

        elif state == "3":
            list_recipes = recipe_service.list_recipes()
            if not list_recipes:
                print("No recipe to update")
                continue

            helpers.display_all_recipes(list_recipes)
            index = helpers.choose_index("recipe", len(list_recipes))

            recipe = list_recipes[index]

            updated_name = input("Update recipe name > ").strip()
            if not updated_name:
                print("Recipe name cannot be empty")
                continue

            updated_description = input("Update description > ").strip()

            try:
                updated_cooking_time = int(input("Update cooking time in minutes > ").strip())
                updated_number_meals = int(input("Update number of meals > ").strip())
            except ValueError:
                print("Invalid input")
                continue

            updated_recipe = Recipe(
                id=recipe.id,
                name=updated_name,
                description=updated_description,
                cooking_time=updated_cooking_time,
                number_meals=updated_number_meals
            )

            recipe_ingredients = helpers.prompt_recipe_ingredient(ingredient_service)
            if recipe_ingredients is None:
                continue

            try:
                recipe_service.update_recipe(updated_recipe, recipe_ingredients)
            except ValueError as exc:
                print(exc)
                continue

            print("Recipe successfuly updated.")
            helpers.display_recipe_details(updated_recipe, recipe_ingredients)

        elif state == "4":
            list_recipes = recipe_service.list_recipes()
            if not list_recipes:
                print("No recipe to delete")
                continue

            helpers.display_all_recipes(list_recipes)
            index = helpers.choose_index("recipe", len(list_recipes))
            recipe_id = list_recipes[index].id

            try:
                recipe_service.delete_recipe(recipe_id)
            except ValueError as exc:
                print(exc)
                continue

            print("Recipe successfuly deleted.")

        elif state == "5":
            break

        else:
            print("Invalid input")

def cli_ingredients(ingredient_service: IngredientApplicationService):
    while True:
        print("\n================\n")
        print("Ingredient management\n")
        print("1 - Display all ingredients")
        print("2 - Create ingredient")
        print("3 - Update ingredient")
        print("4 - Delete ingredient")
        print("5 - Return to main menu\n")

        state = input("> ")

        if state == "1":
            ingredients = ingredient_service.list_ingredients()
            helpers.display_ingredients(ingredients)

        elif state == "2":
            ingredient_name = input("Ingredient name > ").strip()
            ingredient_unit = helpers.prompt_standard_unit(STANDARD_UNITS)
            new_ingredient = NewIngredient(ingredient_name, ingredient_unit)

            try:
                ingredient = ingredient_service.create_ingredient(new_ingredient)
            except ValueError as exc:
                print(exc)
                continue
            else:
                print(f"Ingredient '{ingredient.name}' created.")

        elif state == "3":
            ingredients = ingredient_service.list_ingredients()
            helpers.display_ingredients(ingredients)

            if not ingredients:
                print("There are no ingredients to update.")
                continue

            index = helpers.choose_index("ingredient", len(ingredients))

            ingredient = ingredients[index]

            new_name = input("New name > ").strip()

            if not new_name:
                print("Ingredient name cannot be empty. Update cancelled.\n")
                continue

            new_standard_unit = helpers.prompt_standard_unit(STANDARD_UNITS)

            updated = Ingredient(
                id=ingredient.id,
                name=new_name,
                standard_unit=new_standard_unit
            )

            try:
                ingredient_service.update_ingredient(updated)
            except ValueError as exc:
                print(exc)
                continue

            print("Ingredient successfully updated.\n")
            helpers.display_ingredients(ingredient_service.list_ingredients())

        elif state == "4":
            ingredients = ingredient_service.list_ingredients()
            helpers.display_ingredients(ingredients)

            if not ingredients:
                print("There are no ingredients to delete.")
                continue

            index = helpers.choose_index("ingredient", len(ingredients))

            try:
                ingredient_service.delete_ingredient(ingredients[index].id)
            except ValueError as exc:
                print(exc)
                continue

            print("Ingredient successfully deleted.\n")
            helpers.display_ingredients(ingredient_service.list_ingredients())

        elif state == "5":
            break

        else :
            print("Invalid input")