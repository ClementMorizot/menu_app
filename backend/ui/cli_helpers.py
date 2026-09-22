from backend.domain.measured_ingredients import ShoppingListItem
from backend.domain.menu import Menu
from backend.domain.units import Unit
from backend.domain.unit_conversion import UNIT_CONVERSION_TO_STANDARD
from backend.domain.recipe import Recipe
from backend.domain.ingredient import Ingredient
from backend.domain.measured_ingredients import RecipeIngredient
from backend.application.ingredient_service import IngredientApplicationService
from decimal import Decimal, InvalidOperation

def display_menu(menu: Menu | None) -> None:

    if menu is None:
        print("Menu cannot be displayed\n")
    else:
        timeslots = menu.planned_timeslots()
        print("Generated menu:\n")
        for timeslot in timeslots:
            bloc = menu.get_mealblock(timeslot)
            print(f"{timeslot.day} {timeslot.meal_time}: {bloc.recipe_snapshot.name}")

def display_shopping_list(shopping_list: list[ShoppingListItem] | None) -> None:

    if shopping_list is None:
        print("Shopping list cannot be displayed\n")

    else:
        print("Shopping list:\n")
        for item in shopping_list:
            print(f"{item.ingredient.name}: {item.quantity} {item.unit.value}")

def display_ingredients(ingredients: list[Ingredient]) -> None:
    for index, ingredient in enumerate(ingredients, start=1):
                print(f"{index} - "
                    f"{ingredient.name} "
                    f"[{ingredient.standard_unit.value}]"
                    f"    ID: {ingredient.id}"
                )

def display_recipe(recipe: Recipe, index: int | None = None) -> None:
    if index is not None:
        print(f"{index} - {recipe.name}")
    else:
        print(recipe.name)

    print(f"Preparation time: {recipe.cooking_time}")
    print(f"Number of meals: {recipe.number_meals}\n")

def display_recipe_details(recipe: Recipe, recipe_ingredients: list[RecipeIngredient]) -> None:
    display_recipe(recipe)

    print("Ingredients:")
    for recipe_ingredient in recipe_ingredients:
        print(f"- {recipe_ingredient.ingredient.name}: {recipe_ingredient.quantity} {recipe_ingredient.unit.value}")

def display_all_recipes(list_recipes: list[Recipe]) -> None:

    for index, recipe in enumerate(list_recipes, start=1):
        display_recipe(recipe, index)

def prompt_standard_unit(available_units: list[Unit]) -> Unit:

    while True:
        print("\n================\n")
        print("Choose ingredient's unit.")

        for index, unit in enumerate(available_units, start=1):
            print(f"{index} - {unit.value}")

        choice = input("> ").strip()

        try:
            selected_index = int(choice)
        except ValueError:
            print("Invalid choice.\n")
            continue

        if 1 <= selected_index <= len(available_units):
            return available_units[selected_index - 1]

        print("Invalid choice.\n")

def prompt_recipe_ingredient(ingredient_service: IngredientApplicationService) -> list[RecipeIngredient] | None:
    recipe_ingredients: list[RecipeIngredient] = []
    ingredients = ingredient_service.list_ingredients()
    if ingredients == []:
        print("There is no ingredient to add to the recipe")
        return None

    while True:
        print("Those are the available ingredients:")
        display_ingredients(ingredients)
        print("Do you want to add an ingredient to your recipe?")
        choice = input("y/n/quit > ").strip()

        if choice == "n":
            if not recipe_ingredients:
                print("There are no ingredient in your recipe.")
                print("Recipe cannot be empty.")
                continue

            return recipe_ingredients

        elif choice == "y":
            index = choose_index("ingredient", len(ingredients))
            ingredient = ingredients[index]
            available_units = list(UNIT_CONVERSION_TO_STANDARD[ingredient.standard_unit].keys())
            unit = prompt_standard_unit(available_units)

            while True:
                try:
                    quantity = Decimal(input("Quantity > ").strip())
                    recipe_ingredient = RecipeIngredient(
                        ingredient=ingredient,
                        unit=unit,
                        quantity=quantity
                    )
                except (InvalidOperation, ValueError):
                    print("Invalid input")
                    continue
                break

            recipe_ingredients.append(recipe_ingredient)

        elif choice == "quit":
            print("Ingredient list for recipe could not be properly finished.")
            return None

        else:
            print("Invalid input")

def choose_index(intent: str, index_max: int) -> int:
    while True:
        user_input = input(f"Select {intent} number > ").strip()

        if not user_input:
            print("Input cannot be empty")
            continue

        try :
            index = int(user_input)
        except ValueError as exc:
            print(exc)
            continue

        if index <=0 :
            print("Input cannot be lesser than 1")
            continue
        if index > index_max:
            print(f"Input cannot be gretter than {index_max}")
            continue

        return index-1