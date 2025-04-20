import re


def preprocess_ingredients(ingredient_text: str) -> list[str]:
    # Capital letters do not add the meaning we need
    ingredient_text = ingredient_text.lower()

    # Remove all (19%) that are used
    ingredient_text = re.sub("\(\d+%\)", "", ingredient_text)

    # Remove the word "ingredient" and "ingrediënten"
    ingredient_text = re.sub("ingredi[eë]nten", "", ingredient_text)

    # When the string "Kan sporen " starts it is the end of the ingredients
    ingredient_text = re.sub("kan sporen .*", "", ingredient_text)
    # Split based on ,
    ingredients_raw = ingredient_text.split(",")

    filtered_ingredients = []
    for ingredient in ingredients_raw:
        # Remove symbols that are not letters
        ingredient_filtered = re.sub("[\.:]", "", ingredient)

        # I the string is empty it was not an ingredient
        if len(ingredient_filtered) == 0:
            continue

        # Remove leading space
        if ingredient_filtered[0] == " ":
            ingredient_filtered = ingredient_filtered[1:]

        # Remove trailing space
        if ingredient_filtered[-1] == " ":
            ingredient_filtered = ingredient_filtered[:-1]

        filtered_ingredients.append(ingredient_filtered)
    return filtered_ingredients
