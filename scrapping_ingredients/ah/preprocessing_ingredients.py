import re


def remove_brackets_from_ingredients_text(ingredients_text: str) -> str:
    ingredients_text = ingredients_text.replace("[", "(")
    ingredients_text = ingredients_text.replace("]", ")")

    if len(re.findall(r"\(", ingredients_text)) != len(
        re.findall(r"\)", ingredients_text)
    ):
        raise ValueError(
            f"Number of brackets is not equal in {ingredients_text}. "
            f"Number of ( is {len(re.findall(r'\(', ingredients_text))} and number of ) is {len(re.findall(r'\)', ingredients_text))}"
        )
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
    ingredient = re.sub(r"[\.:\*]", "", ingredient)
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

    # Remove all 19,3% 12 % and 43.1% that are used
    ingredients_text = re.sub(r"[\d,\.]+\s?%", "", ingredients_text)

    # Remove the word "ingredient" and "ingrediënten"
    ingredients_text = re.sub(r"ingredi[eë]nten", "", ingredients_text)

    # When the string "Kan sporen " starts it is the end of the ingredients
    ingredients_text = re.sub(r"kan sporen .*", "", ingredients_text)
    ingredients_text = re.sub(r"kan bevatten.*", "", ingredients_text)
    ingredients_text = re.sub(r"bevatten:.*", "", ingredients_text)
    ingredients_text = re.sub(r"waarvan toegevoegd.*", "", ingredients_text)
    ingredients_text = re.sub(r"allergie-informatie.*", "", ingredients_text)
    ingredients_text = re.sub(r"kan [\w\d\s]*? bevatten.*", "", ingredients_text)

    # Split based on ,
    ingredients = split_ingredients(ingredients_text)

    if "" in ingredients:
        ingredients.remove("")
    return ingredients


if __name__ == "__main__":
    from pathlib import Path
    import json

    # Load the products
    products_path = Path(__file__).parent / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))

    # Preprocess the ingredients
    for product_url, product in products.items():
        ingredients = product["ingredients"]
        if len(ingredients) == 0:
            continue
        try:
            product["processed_ingredients"] = preprocess_ingredients(ingredients)
        except ValueError as e:
            print(f"ValueError for product {product_url}: {e}")
            product["processed_ingredients"] = None
            product["error"] = str(e)
            continue
        except Exception as e:
            print(f"Error processing ingredients for product {product_url}: {e}")
            raise e

    # Save the products
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
