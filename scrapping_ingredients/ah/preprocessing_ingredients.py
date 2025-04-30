import regex as re


def remove_brackets_from_ingredients_text(ingredients_text: str) -> str:
    """Remove brackets from the ingredients text and merge the ingredients
    Meaning "meel (tarwe, wit)" will be changed to "meel tarwe, meel wit"

    :param ingredients_text: full block of ingredients text
    :type ingredients_text: str
    :raises ValueError: if the number of opening and closing brackets are not equal
    :return: ingredient_text without brackets
    :rtype: str
    """
    # Only deal with 1 kind of brackets
    ingredients_text = ingredients_text.replace("[", "(")
    ingredients_text = ingredients_text.replace("]", ")")

    # Check if the number of opening and closing brackets are equal
    if len(re.findall(r"\(", ingredients_text)) != len(
        re.findall(r"\)", ingredients_text)
    ):
        raise ValueError(
            f"Number of brackets is not equal in {ingredients_text}. "
            f"Number of ( is {len(re.findall(r'\(', ingredients_text))} and number of ) is {len(re.findall(r'\)', ingredients_text))}"
        )

    # Keep going as long as there is a bracket in the text
    while "(" in ingredients_text:
        # Get the first ingredient with brackets
        search_bracket_ingredient = re.search(r"[^,]*?\(", ingredients_text)
        start_index = search_bracket_ingredient.start()
        end_index = search_bracket_ingredient.end()
        number_of_brackets = 1

        # If there are brackets within the bracket ingredient we need to go longer
        # So we get "zout (zee (noord, zuid), mijn)" we need to go to the end of the last bracket
        while number_of_brackets > 0:
            next_char = ingredients_text[end_index]
            if next_char == "(":
                number_of_brackets += 1
            elif next_char == ")":
                number_of_brackets -= 1
            end_index += 1

        full_ingredient = ingredients_text[start_index:end_index]

        # Split it in 3 parts. e.q "zout (zee (noord, zuid), mijn)" will become
        # ing_raw = "zout (zee (noord, zuid), mijn)"
        # ing_base = "zout"
        # ing_types_raw = "zee (noord, zuid), mijn"
        ing_raw, ing_base, ing_types_raw = re.findall(
            r"(([^\(]*)\((.*)\))", full_ingredient
        )[0]

        # If we have nested brackets time to remove them
        if "(" in ing_types_raw:
            ing_types_raw = remove_brackets_from_ingredients_text(ing_types_raw)

        # Really remove the brackets
        ing_types = ing_types_raw.split(",")
        ing_no_brackets = ", ".join(
            [f"{ing_base} {ingredient_type.strip()}" for ingredient_type in ing_types]
        )
        ingredients_text = ingredients_text.replace(ing_raw, ing_no_brackets)

    return ingredients_text


def clean_up_ingredient(ingredient: str) -> str:
    # Remove all symbols we do not care about
    ingredient = re.sub(r"[^\p{L}\s\d\-\`\'\’]", "", ingredient)
    # Remove all extra spaces
    ingredient = re.sub(r"\s+", " ", ingredient)
    return ingredient.strip()


def split_ingredients(ingredients_text: str) -> list[str]:
    # Ingedredients with brackets (like "meel (tarwe, wit)") are split into two
    # ingredients (like "meel tarwe" and "meel wit")
    ingredients_text = remove_brackets_from_ingredients_text(ingredients_text)

    # SPLIT
    ingredients_list = ingredients_text.split(",")

    # Clean up
    ingredients_list = [
        clean_up_ingredient(ingredient) for ingredient in ingredients_list
    ]
    return ingredients_list


def preprocess_ingredients(ingredients_text: str) -> list[str]:
    # Capital letters do not add the meaning we need
    ingredients_text = ingredients_text.lower()

    # Remove indication of amounts like "19,3%", "12 %", and "43.1g"
    ingredients_text = re.sub(r"\d[\d,\.]*\s?%", "", ingredients_text)
    ingredients_text = re.sub(r"\d[\d,\.]*\s?g", "", ingredients_text)

    # Remove the words "ingredient" and "ingrediënten"
    ingredients_text = re.sub(r"ingredi[eë]nten", "", ingredients_text)

    # Cut the string if when the extra information starts
    ingredients_text = re.sub(r"kan sporen .*", "", ingredients_text)
    ingredients_text = re.sub(r"kan .*bevatten.*", "", ingredients_text)
    ingredients_text = re.sub(r"bevatten:.*", "", ingredients_text)
    ingredients_text = re.sub(r"waarvan toegevoegd.*", "", ingredients_text)
    ingredients_text = re.sub(r"allergie-informatie.*", "", ingredients_text)
    ingredients_text = re.sub(r"kan [\w\d\s]*? bevatten.*", "", ingredients_text)

    # Split ingredients
    ingredients_list = split_ingredients(ingredients_text)

    if "" in ingredients_list:
        ingredients_list.remove("")
    return ingredients_list


if __name__ == "__main__":
    from pathlib import Path
    import json
    import time

    # Load the products
    products_path = Path(__file__).parent / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))

    # Preprocess the ingredients
    start_time = time.time()
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
    # Preprocessing completed for 1186 products in 0.13 seconds
    print(
        f"Preprocessing completed for {len(products)} products in {time.time() - start_time:.2f} seconds"
    )
    # Save the products
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
