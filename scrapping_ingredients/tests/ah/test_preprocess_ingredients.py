import pytest
from ...ah.preprocessing_ingredients import preprocess_ingredients


def test_preprocess_ingredients_empty():
    ingredients_text = ""
    expected_result = []
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_wasa_sesam():
    ingredients_text = "IngrediëntenIngredienten: Volkoren TARWEMEEL (49%), TARWEMEEL (39%), SESAMZAAD (11%), gist, zonnebloemolie, suiker, zout. Kan sporen van MELK bevatten.Allergie-informatieBevat: Tarwe, Sesamzaad, Glutenbevattende GranenKan bevatten: Melk"
    expected_result = [
        "volkoren tarwemeel",
        "tarwemeel",
        "sesamzaad",
        "gist",
        "zonnebloemolie",
        "suiker",
        "zout",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_lu_mini_crackers_zout():
    ingredients_text = "IngrediëntenIngrediënten: TARWEBLOEM 97%, palmolie, zout 2,1%, zuurteregelaar (natriumcarbonaten), GERSTEMOUTMEEL, gistKan bevatten: ei, melk.Allergie-informatieBevat: Gerst, Glutenbevattende Granen, TarweKan bevatten: Eieren, Melk"
    expected_result = [
        "tarwebloem",
        "palmolie",
        "zout",
        "zuurteregelaar natriumcarbonaten",
        "gerstemoutmeel",
        "gist",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_ah_ananas():
    ingredients_text = "IngrediëntenIngrediënten: ananas.Waarvan toegevoegde suikers 0.00g per 100 gram en waarvan toegevoegd zout 0.00g per 100 gram"
    expected_result = ["ananas"]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_ah_snoepgroente_komkommer():
    ingredients_text = "IngrediëntenIngrediënten: Waarvan toegevoegde suikers 0.00g per 100 gram en waarvan toegevoegd zout 0.00g per 100 gram"
    expected_result = []
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result
