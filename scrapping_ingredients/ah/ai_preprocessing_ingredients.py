import re

import ollama
from tqdm import tqdm

ollama.create(
    model="ingredients-preprocessing",
    from_="llama3.2",
    system="Geef een de lijst van alle ingrediënten in de input text. Geef alleen de ingrediënten terug, zonder enige uitleg. Als een ingredient haakjes heeft splits het in meerdere ingredienten. De ingrediënten moeten in een lijst staan, met elk ingrediënt op een nieuwe regel.",
    parameters={
        "temperature": 0.1,
    },
)


def preprocess_ingredients(ingredients_text: str) -> list[str]:
    response = ollama.generate(
        model="ingredients-preprocessing",
        prompt=ingredients_text,
    )
    ingredients_raw = response.response
    ingredients_list = re.findall(r"[\d+\.\s\-\*]*(.*)\n", ingredients_raw)
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
    print("Preprocessing ingredients...")
    for product_url, product in tqdm(products.items()):
        ingredients = product["ingredients"]
        if len(ingredients) == 0:
            continue
        try:
            product["ai_processed_ingredients"] = preprocess_ingredients(ingredients)
        except ValueError as e:
            print(f"ValueError for product {product_url}: {e}")
            product["ai_processed_ingredients"] = None
            product["error"] = str(e)
            continue
        except Exception as e:
            print(f"Error processing ingredients for product {product_url}: {e}")
            raise e
    # Preprocessing completed for 1186 products in 1854.80 seconds
    print(
        f"Preprocessing completed for {len(products)} products in {time.time() - start_time:.2f} seconds"
    )
    # Save the products
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
