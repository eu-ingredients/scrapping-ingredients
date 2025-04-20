import pytest
from ...ah.preprocessing_ingredients import preprocess_ingredients


def test_preprocess_ingredients_empty():
    ingredients_text = ""
    expected_result = []
    result = preprocess_ingredients(ingredients_text)

    result == expected_result
