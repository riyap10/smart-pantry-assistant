from google import genai
from rich.console import Console

console = Console()

def generate_recipe_from_pantry(ingredients_list, base_recipe, instructions, meal_type="any meal", cuisine="any cuisine", exclude="none"):
    try:
        base_title = base_recipe.get("title", "Custom Dish")
        missed = [img.get("name") for img in base_recipe.get("missedIngredients", [])]
        used = [img.get("name") for img in base_recipe.get("usedIngredients", [])]

        model = "gemini-3.1-flash-lite"

        ingredients_str = ", ".join(ingredients_list)

        # debug print statements:
        #print(instructions)
        #print(ingredients_str)
        #print(used)
        #print(missed)

        
        prompt = f"""
          You are a chef assistant.
          We want to make a dish inspired by the recipe: "{base_title}"
          The user wants a {meal_type} with {cuisine} cuisine.

          STRICT RULES - YOU MUST FOLLOW THESE:
          1. You may ONLY use ingredients from this list: {ingredients_str}
          2. Do NOT use any ingredient not in that list, even if the original recipe calls for it.
          3. Do NOT use these excluded ingredients under any circumstances: {exclude}
          4. Basic pantry staples like salt, pepper, water, and cooking oil are allowed.

          Here are the original cooking instructions for inspiration only:
          {instructions}

          The original recipe used: {", ".join(used)}
          The original recipe also needed: {", ".join(missed)} — DO NOT use these, they are not available.

          YOUR TASK:
          1. Adapt the recipe using ONLY the available ingredients listed above.
          2. Substitute or remove any missing ingredients creatively.
          3. Keep cooking techniques and timings similar where possible.
          4. Make sure the recipe fits the requested meal type and cuisine.

          Format the output with:
          - A Title
          - Yields, Prep time, and Cook time
          - An Ingredients list with realistic quantities for each item used
          - Numbered Steps
          """

        client = genai.Client()
        stream = client.interactions.create(
            model=model,
            input=prompt,
            stream=True
        )

        full_recipe_text = ""
        for event in stream:
            # print(repr(event)) # Debug
            if event.event_type == "step.delta":
                if event.delta.type == "text":
                    console.print(event.delta.text, end="", markup=False)
                    full_recipe_text += event.delta.text

        if full_recipe_text:
            return full_recipe_text

    except Exception as e:
        print(f"[bold red]Error generating recipe: [/bold red]{str(e)}")
        return f"Error generating recipe: {str(e)}"

    print(f"\n{model} [bold red]is temporarily unavailable.[/bold red]")
    return f"\n{model} is temporarily unavailable."