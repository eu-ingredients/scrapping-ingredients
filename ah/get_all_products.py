import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

headers = {
    "Host": "www.ah.nl",
    "User-Agent": 'Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135',
    "Accept": "*/*",
    "Accept-Language": "en-US,nl;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "text/plain;charset=UTF-8",
}

all_products = []

resutling_file = Path("products.json")

if resutling_file.exists():
    results = json.loads(resutling_file.read_bytes())
else:
    results = {}

base_url = r"https://www.ah.nl/producten"
# Get all drinks from overview
# response_prod_cat = requests.get(base_url, headers=headers)
# last_response = response_prod_cat.status_code

# if last_response != 200:
#     raise ConnectionError(f"Did not get a 200 status from {base_url}")

# ah_soup = BeautifulSoup(response_prod_cat.content, "html.parser")

# all_products_cats = ah_soup.find_all(
#     "div",
#     class_="product-category-overview_category__vqzcb",
# )

for i in tqdm(range(1, 23)):
    href = f"https://www.ah.nl/producten/2457/tussendoortjes?page={i}&withOffset=true"

    response_prod = requests.get(href, headers=headers)
    last_response = response_prod.status_code

    if last_response != 200:
        raise ConnectionError(f"Did not get a 200 status from {href}")

    ah_cat_soup = BeautifulSoup(response_prod.content, "html.parser")

    products = ah_cat_soup.find_all(
        "article",
        class_="product-card-portrait_root__ZiRpZ",
    )
    all_products.extend(products)


print(f"Found {len(all_products)} products")
print(f"Already scrapped {len(results)} products")
for product_response in tqdm(all_products):
    href = f"https://www.ah.nl{product_response.find('a')['href']}"

    if href in results:
        continue
    response_prod_cat = requests.get(href, headers=headers)
    last_response = response_prod_cat.status_code

    if last_response != 200:
        print(f"[ERROR] Did not get a 200 status from {href}")
        time.sleep(10)
        continue

    product_soup = BeautifulSoup(response_prod_cat.content, "html.parser")

    ingredients_div = product_soup.find("h2", string="Ingrediënten")
    if not ingredients_div:
        continue

    ingredients = ingredients_div.parent.text.strip()
    results[href] = {
        "name": product_soup.find("h1").text,
        "ingredients": ingredients,
    }

print(f"Scrapped a total of {len(results)} products")

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
