from google import genai

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
The user does NOT want to use these ingredients today, do not include them anywhere in the recipe: {exclude}.
You must completely ignore and omit {exclude} from the title, ingredients list, and all steps.
        
        Here are the EXACT cooking instructions from the original recipe:
        {instructions}
        
        The user has ONLY these ingredients in their pantry: {ingredients_str}
        The original recipe uses these items we HAVE: {", ".join(used)}
        But it also requires these 'Missed Ingredients' which the user DOES NOT HAVE: {", ".join(missed)}

        YOUR TASK:
            1. Adapt the original step-by-step instructions provided above so they can be executed WITHOUT the missed
                ingredients.
            2. Professionally substitute or alter the steps using ONLY what is available in the user's pantry.
            3. Keep the original core cooking techniques, temperatures, and timings, but adjust them so the directions 
                make complete sense without the missing items.
            4. Explicitly do NOT use or list any of the missed items in your final output.
            5. Do not feel pressured to use all of the ingredients in the pantry.
            6. Make sure the recipe fits the requested meal type and cuisine.
        
        Format the output cleanly with a Title, an Ingredients list showing what they will use, and the modified 
        numbered Steps.
        CRUCIAL FORMATTING RULE: The very first line of your response must be a standard markdown header containing ONLY the title of the dish, like this: # Name of the Dish. 
        Do not include any greetings, introductory text, or blank lines before the title.
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
                    print(event.delta.text, end="", flush=True)
                    full_recipe_text += event.delta.text

        if full_recipe_text:
            return full_recipe_text

    except Exception as e:
        print(f"Error generating recipe: {str(e)}")
        return f"Error generating recipe: {str(e)}"

    print(f"\n{model} is temporarily unavailable.")
    return f"\n{model} is temporarily unavailable."