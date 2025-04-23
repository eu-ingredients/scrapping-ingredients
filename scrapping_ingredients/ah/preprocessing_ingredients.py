import re


def remove_brackets_from_ingredients_text(ingredients_text: str) -> str:
    ingredients_text = ingredients_text.replace("[", "(")
    ingredients_text = ingredients_text.replace("]", ")")

    while "(" in ingredients_text:
        search_bracket_ingredient = re.search(r"[^,]*?\(", ingredients_text)

        # Get the first ingredient with brackets
        start_index = search_bracket_ingredient.start()
        end_index = search_bracket_ingredient.end()
        number_of_brackets = 1

        while number_of_brackets > 0:
            next_char = ingredients_text[end_index]
            if next_char == "(":
                number_of_brackets += 1
            elif next_char == ")":
                number_of_brackets -= 1
            end_index += 1

        full_ingredient = ingredients_text[start_index:end_index]

        ing_raw, ing_base, ing_types_raw = re.findall(
            r"(([^\(]*)\((.*)\))", full_ingredient
        )[0]
        if "(" in ing_types_raw:
            ing_types_raw = remove_brackets_from_ingredients_text(ing_types_raw)

        ing_types = ing_types_raw.split(",")

        # Merge them
        ing_no_brackets = ", ".join(
            [f"{ing_base} {ingredient_type.strip()}" for ingredient_type in ing_types]
        )
        ingredients_text = ingredients_text.replace(ing_raw, ing_no_brackets)

    return ingredients_text


def clean_up_ingredient(ingredient: str) -> str:
    # Remove all extra spaces
    ingredient = re.sub(r"\s+", " ", ingredient)
    return ingredient.strip()


def split_ingredients(ingredients_text: str) -> list[str]:
    # Ingedredients with brackets (like "meel (tarwe, wit)") are split into two
    # ingredients (like "meel tarwe" and "meel wit")
    ingredients_text = remove_brackets_from_ingredients_text(ingredients_text)

    # Remove all extra spaces
    ingredients_text = re.sub(r"\s+", " ", ingredients_text)
    ingredients_list = ingredients_text.split(",")
    ingredients_list = [
        clean_up_ingredient(ingredient) for ingredient in ingredients_list
    ]
    return ingredients_list


def preprocess_ingredients(ingredients_text: str) -> list[str]:
    # Capital letters do not add the meaning we need
    ingredients_text = ingredients_text.lower()

    # Remove all (19%) that are used
    ingredients_text = re.sub(r"[\d,]+\s?%", "", ingredients_text)

    # Remove the word "ingredient" and "ingrediënten"
    ingredients_text = re.sub(r"ingredi[eë]nten", "", ingredients_text)

    # When the string "Kan sporen " starts it is the end of the ingredients
    ingredients_text = re.sub(r"kan sporen .*", "", ingredients_text)
    ingredients_text = re.sub(r"kan bevatten.*", "", ingredients_text)
    ingredients_text = re.sub(r"waarvan toegevoegd.*", "", ingredients_text)
    ingredients_text = re.sub(r"allergie-informatie.*", "", ingredients_text)
    ingredients_text = re.sub(r"kan [\w\d\s]*? bevatten.*", "", ingredients_text)

    # Split based on ,
    ingredients_raw = split_ingredients(ingredients_text)

    filtered_ingredients = []
    for ingredient in ingredients_raw:
        # Remove symbols that are not letters
        ingredient_filtered = re.sub(r"[\.:\*]", "", ingredient)

        # I the string is empty it was not an ingredient
        if len(ingredient_filtered) == 0:
            continue

        # Remove leading space
        if ingredient_filtered[0] == " ":
            ingredient_filtered = ingredient_filtered[1:]
        if len(ingredient_filtered) == 0:
            continue

        # Remove trailing space
        if ingredient_filtered[-1] == " ":
            ingredient_filtered = ingredient_filtered[:-1]
        if len(ingredient_filtered) == 0:
            continue

        filtered_ingredients.append(ingredient_filtered)
    return filtered_ingredients


if __name__ == "__main__":
    from pathlib import Path
    import json

    # Load the products
    products_path = Path(__file__).parent / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))

    # Preprocess the ingredients
    for _, product in products.items():
        ingredients = product["ingredients"]
        if len(ingredients) == 0:
            continue
        try:
            product["processed_ingredients"] = preprocess_ingredients(ingredients)
        except Exception as e:
            print(f"Error processing ingredients for product {product['name']}: {e}")
            raise e

    # Save the products
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
