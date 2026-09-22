from uuid import UUID
from backend.domain.user_exclusions import UserExclusions
from backend.application.recipe_service import RecipeApplicationService
from backend.domain.recipe import Recipe
import backend.ui.cli_helpers as helpers

def cli_exclusion_list(user_exclusions: UserExclusions, recipe_service: RecipeApplicationService) -> None:

    print("You are allowed to exclude recipes before the generation of your menu.")
    while True:
        list_recipes = recipe_service.list_recipes()
        excluded_ids = user_exclusions.list_all_user_exclusions()
        excluded_recipes = [
            recipe for recipe in list_recipes
            if recipe.id in excluded_ids
        ]
        print("This is the user exclusions menu")
        print("1 - Display exclusions")
        print("2 - Add recipe to exclusions")
        print("3 - Remove recipe from exclusions")
        print("4 - Return")

        choice = input("User choice > ").strip()

        if choice == "1":
            helpers.display_all_recipes(excluded_recipes)
            continue
        elif choice == "2":
            if len(excluded_recipes) == len(list_recipes):
                print("There is no available recipe")
                continue
            recipe_id = cli_excluding_recipe(excluded_recipes, list_recipes)
            if recipe_id is None:
                continue
            user_exclusions.add_user_exclusion(recipe_id)
        elif choice == "3":
            if not excluded_recipes:
                print("There is no excluded recipe")
                continue
            exclusion_id = cli_removing_from_exclusion(excluded_recipes)
            if exclusion_id is None:
                continue
            user_exclusions.remove_user_exclusion(exclusion_id)
        elif choice == "4":
            break
        else:
            print("Invalid user input")
            continue

        print("This is the current exclusion list:")
        excluded_ids = user_exclusions.list_all_user_exclusions()
        excluded_recipes = [
            recipe for recipe in list_recipes
            if recipe.id in excluded_ids
        ]
        helpers.display_all_recipes(excluded_recipes)

def cli_excluding_recipe(excluded_recipes: list[Recipe], list_recipes: list[Recipe]) -> UUID | None:
    available_recipes = [recipe for recipe in list_recipes
                            if recipe not in excluded_recipes]
    helpers.display_all_recipes(available_recipes)
    index = helpers.choose_index("recipe", len(available_recipes))
    return available_recipes[index].id


def cli_removing_from_exclusion(excluded_recipes: list[Recipe]) -> UUID | None:
    print("This is the current exclusion list:")
    helpers.display_all_recipes(excluded_recipes)
    index = helpers.choose_index("excluded recipe", len(excluded_recipes))
    return excluded_recipes[index].id