from google import genai


def generate_recipe_from_pantry(ingredients_list):
    try:
        model = "gemini-2.5-flash-lite"

        ingredients_str = ", ".join(ingredients_list)

        prompt = f"""
        You are a chef assistant.
        The user has these ingredients in their pantry: {ingredients_str}

        Please generate a recipe using these items. 
        Requirements:
        1. Give it a title.
        2. List the ingredients used with realistic, estimated portions.
        3. Provide clear, step-by-step cooking instructions.
        4. Do NOT assume or add complex ingredients they don't have (basic salt, pepper, water, and cooking oil are fine).
        5. Ensure safe cooking instructions.
        6. Output will be sent through the command line, so keep that in mind when formatting the recipe.
        """

        client = genai.Client()
        stream = client.interactions.create(
            model=model,
            input=prompt,
            stream=True
        )

        full_recipe_text = ""
        for event in stream:
            # print(repr(event))
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