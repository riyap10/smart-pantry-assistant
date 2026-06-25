from database.database import create_table, add_ingredient, view_pantry, create_recipe_table, save_recipe, view_recipes
from api.spoonacular_api import get_nutrition, find_recipes_by_ingredients, get_recipe_instructions
from api.gemini_api import generate_recipe_from_pantry

create_table()
create_recipe_table()

def menu():
    print("\n==================================")
    print("STOCKD")
    print("==================================")
    print("1. Add Ingredient")
    print("2. View Pantry")
    print("3. See Nutrition Facts")
    print("4. Generate Recipe")
    print("5. View Saved Recipes")
    print("6. Close")

def nutrition_menu():
    pantry_items = view_pantry()
    if not pantry_items:
        print("Your pantry is empty.")
        return
    print("Which ingredient do you want nutrition info for?")
    for i, item in enumerate(pantry_items, 1):
        print(f"{i}. {item[1]}")
    selection = input("Enter number: ")
    if selection.isdigit() and 1 <= int(selection) <= len(pantry_items):
        selected = pantry_items[int(selection) - 1]
        result = get_nutrition(selected[1])
        if result:
            print(f"\nNutrition for {result['name']} (per 1 cup):")
            for nutrient, value in result["nutrients"].items():
                print(f"  {nutrient}: {value}")
    else:
        print("Invalid choice.")

while True:
    menu()
    choice = input("Choice: ")
    if choice == "1":
        ingredient = input("Enter ingredient: ")
        quantity = input("Enter quantity: ")
        expiration = input("Enter expiration date (MM-DD-YYYY): ")
        add_ingredient(ingredient, quantity, expiration)
        print("\nIngredient added to pantry!")
    elif choice == "2":
        pantry = view_pantry()
        print("\nThis is your current pantry!")
        for item in pantry:
            print(item)
    elif choice == "3":
        nutrition_menu()
    elif choice == "4":
        pantry_items = view_pantry()
        if not pantry_items:
            print("Your pantry is empty!")
            continue
        ingredients_list = [item[1] for item in pantry_items]
        print("\nWhat meal type are you looking for?")
        print("1. Breakfast")
        print("2. Lunch")
        print("3. Dinner")
        meal_choice = input("Choice: ")
        meal_map = {"1": "breakfast", "2": "lunch", "3": "dinner"}
        meal_type = meal_map.get(meal_choice, "any meal")
        cuisine = input("\nWhat cuisine are you in the mood for? (e.g. Indian, Italian, Chinese, or press Enter to skip): ").strip()
        if not cuisine:
            cuisine = "any cuisine"
        exclude = input("\nAny ingredients you want to exclude today? (e.g. rice, eggs, or press Enter to skip): ").strip()
        if not exclude:
            exclude = "none"
    
        
        print(f"\nSending {len(ingredients_list)} ingredients to Gemini...")
        print("\n==================================")
        print("           CUSTOM RECIPE          ")
        print("==================================")
        base_recipe = find_recipes_by_ingredients(ingredients_list)
        instructions = get_recipe_instructions(base_recipe.get("id"))
        recipe = generate_recipe_from_pantry(ingredients_list, base_recipe, instructions, meal_type, cuisine, exclude)        
        print("\n")
        save_recipe(recipe)
        print("Recipe saved!")

    elif choice == "5":
        recipes = view_recipes()
        if not recipes:
            print("\nNo saved recipes yet!")
        else:
            print("\nYour saved recipes:")
            for recipe in recipes:
                print(f"\n[{recipe[2]}]\n{recipe[1]}")
    elif choice == "6":
        print("Bye!")
        break
    else:
        print("Invalid choice.")