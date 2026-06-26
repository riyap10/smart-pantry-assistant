from database.database import create_table, add_ingredient, view_pantry, create_recipe_table, save_recipe, view_recipes
from api.spoonacular_api import get_nutrition, find_recipes_by_ingredients, get_recipe_instructions
from api.gemini_api import generate_recipe_from_pantry

import questionary
from rich import print
from rich.table import Table
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel

create_table()
create_recipe_table()
console = Console()

def menu():
    console.clear()
    console.rule("STOCKD")
    selection = questionary.select(
        "What would you like to do?",
        choices=["Add Ingredient",
                 "View Pantry",
                 "See Nutrition Facts",
                 "Generate Recipe",
                 "View Saved Recipes",
                 "Close"
        ],
        use_shortcuts=True,
    ).ask()

    return selection

def extract_recipe_title(markdown_text):
    lines = [line.strip() for line in markdown_text.split('\n') if line.strip()]
    if not lines:
        return "Custom Recipe"

    first_line = lines[0]
    return first_line.lstrip('#').replace('**', '').strip()

def nutrition_menu():
    pantry_items = view_pantry()
    if not pantry_items:
        print("Your pantry is empty.")
        return
    selection = questionary.select(
        "Which ingredient do you want nutrition info for?",
        choices=[pantry_item[1] for pantry_item in pantry_items]
    ).ask()
    if selection:
        with console.status(f"Retrieving nutrition info for {selection}..."):
            result = get_nutrition(selection)
        console.clear()
        console.rule("Nutrition Facts")
        if result:
            print(f"\nNutrition for {result['name']} (per 1 cup):")
            for nutrient, value in result["nutrients"].items():
                print(f"  {nutrient}: {value}")
    else:
        print("Invalid choice.")

def generate_recipe():
    pantry_items = view_pantry()
    if not pantry_items:
        print("Your pantry is empty!")
        return
    ingredients_list = [item[1] for item in pantry_items]
    meal_type = questionary.select(
        "\nWhat meal type are you looking for?",
        choices=["Breakfast",
                 "Lunch",
                 "Dinner",
                 "any meal"
        ],
        use_shortcuts=True,
        default="any meal"
    ).ask()
    cuisine = questionary.text(
        "\nWhat cuisine are you in the mood for? (e.g. Indian, Italian, Chinese, or press Enter to skip): "
    ).ask()
    if not cuisine:
        cuisine = "any cuisine"
    exclude = questionary.checkbox(
        "\nAny ingredients you want to exclude today? (e.g. rice, eggs, or press Enter to skip): ",
        choices=[pantry_item[1] for pantry_item in pantry_items]
    ).ask()
    if not exclude:
        exclude = "none"

    with console.status(f"Sending {len(ingredients_list)} ingredients to Gemini..."):
        base_recipe = find_recipes_by_ingredients(ingredients_list)
        instructions = get_recipe_instructions(base_recipe.get("id"))
        recipe = generate_recipe_from_pantry(ingredients_list, base_recipe, instructions, meal_type, cuisine, exclude)
    print("\n")
    save_recipe(recipe)
    print("Recipe saved!")
    return recipe

while True:
    choice = menu()
    if choice == "Add Ingredient":
        console.clear()
        console.rule("Add Ingredient")
        ingredient = questionary.text("Enter ingredient: ").ask()
        quantity = questionary.text("Enter quantity: ").ask()
        expiration = questionary.text("Enter expiration date (MM-DD-YYYY): ").ask()
        add_ingredient(ingredient, quantity, expiration)
        print("\nIngredient added to pantry!")
    elif choice == "View Pantry":
        console.clear()
        pantry = view_pantry()
        console.rule("Your Pantry")
        table = Table()
        table.add_column("Ingredient")
        table.add_column("Quantity")
        table.add_column("Expiration Date")
        for item in pantry:
            table.add_row(item[1], str(item[2]), item[3])
        print(table)
        input("\nPress Enter to continue...")
    elif choice == "See Nutrition Facts":
        console.clear()
        console.rule("Nutrition Facts")
        nutrition_menu()
        input("\nPress Enter to continue...")
    elif choice == "Generate Recipe":
        console.clear()
        console.rule("Generate Recipe")
        final_recipe = generate_recipe()
        if final_recipe:
            console.clear()
            console.rule("Generate Recipe")
            recipe_card = Panel(
                Markdown(final_recipe)
            )

            console.print(recipe_card)
        input("\nPress Enter to continue...")

    elif choice == "View Saved Recipes":
        console.clear()
        console.rule("Saved Recipes")
        recipes = view_recipes()
        if not recipes:
            print("\nNo saved recipes yet!")
        else:
            recipe_map = {}
            for recipe in recipes:
                recipe_text = recipe[1]
                saved_on = recipe[2]
                recipe_title = extract_recipe_title(recipe_text)
                recipe_map[recipe_title] = (recipe_text, saved_on)

            selection = questionary.select(
                "Which recipe would you like to open?",
                choices=list(recipe_map.keys()) + ["Back to Main Menu"]
            ).ask()

            if selection == "Back to Main Menu":
                continue

            console.clear()
            console.rule("Saved Recipes")

            recipe_card = Panel(
                Markdown(recipe_map[selection][0])
            )

            console.print(recipe_card)
            input("\nPress Enter to continue...")
    elif choice == "Close":
        console.clear()
        print("Bye!")
        break