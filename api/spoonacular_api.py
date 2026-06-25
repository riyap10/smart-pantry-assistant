import requests
import os 
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_KEY = os.getenv("SPOONACULAR_API_KEY")

def get_nutrition(ingredient_name):
    search_url = "https://api.spoonacular.com/food/ingredients/search"
    search_params = {
        "query" : ingredient_name,
        "number" : 1,
        "apiKey" : SPOONACULAR_KEY
    }

    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()

    if not search_data["results"]:
        print(f"No results found for {ingredient_name}.")
        return None
    
    ingredient_id = search_data["results"][0]["id"]
    
    nutrition_url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information"
    nutrition_params = {
        "amount" : 1, 
        "unit" : "cup",
        "apiKey" : SPOONACULAR_KEY
    }

    nutrition_response = requests.get(nutrition_url, params=nutrition_params)
    nutrition_data = nutrition_response.json()

    nutrients = nutrition_data.get("nutrition", {}).get("nutrients", [])
    nutrients_to_show = ["Calories", "Protein", "Carbohydrates", "Fat", "Fiber"]
    summary = {}
    for n in nutrients:
        if n["name"] in nutrients_to_show:
            summary[n["name"]] = f'{round(n["amount"])}{n["unit"]}'
    
    return {
        "name" : nutrition_data.get("name"),
        "nutrients" : summary
    }