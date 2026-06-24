from database.database import create_table
from database.database import add_ingredient
from database.database import view_pantry
from api.spoonacular_api import get_nutrition

create_table()

def menu():
    print("\n==================================")
    print("STOCKD")
    print("==================================")
    print("1. Add Ingredient")
    print("2. View Pantry")
    print("3. See Nutrition Facts")
    print("4. Close")

def nutrition_menu():
    pantry_items = view_pantry()
    if not pantry_items:
        print("Your pantry is empty.")
        return
    print("Which ingredient do you want nutrition info for?")
    for i, item in enumerate(pantry_items, 1):
        print(f"{i}, {item[1]}")
    selection = input("Enter number: ")
    if selection.isdigit() and 1 <= int(selection) <= len(pantry_items):
        selected = pantry_items[int(selection) - 1]
        result = get_nutrition(selected[1])
        if result:
            print(f"\nNutrition for {result["name"]} (per 1 cup):")
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
        print("Bye!")
        break
    else:
        print("Invalid choice.")

