import re


def split_ingredients(ingredients_text: str) -> list[str]:
    # Ingedredients with brackets (like "meel (tarwe, wit)") are split into two
    # ingredients (like "meel tarwe" and "meel wit")
    ingredients_with_brackets = re.findall(r"[\w\s]*?\(.*?\)", ingredients_text)
    for ingredient in ingredients_with_brackets:
        # Remove the brackets
        ingredient_base = re.findall(r"([\w\s]*?)\(.*?\)", ingredient)[0]
        # Remove the leading and trailing spaces
        ingredient_types_raw = re.findall(r"[\w\s]*?\((.*?)\)", ingredient)[0]
        ingredient_types = split_ingredients(ingredient_types_raw)
        # Merge them
        ingredient_no_brackets = ", ".join(
            [
                f"{ingredient_base} {ingredient_type}"
                for ingredient_type in ingredient_types
            ]
        )
        # Add the ingredient without brackets to the list
        ingredients_text = ingredients_text.replace(ingredient, ingredient_no_brackets)
    # Remove all extra spaces
    ingredients_text = re.sub(r"\s+", " ", ingredients_text)
    return ingredients_text.split(", ")


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

    # Split based on ,
    ingredients_raw = split_ingredients(ingredients_text)

    filtered_ingredients = []
    for ingredient in ingredients_raw:
        # Remove symbols that are not letters
        ingredient_filtered = re.sub(r"[\.:]", "", ingredient)

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
