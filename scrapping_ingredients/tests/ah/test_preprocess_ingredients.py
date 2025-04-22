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


def test_preprocess_ingredients_Liga_Cracotte_vezelrijk():
    ingredients_text = "IngrediëntenIngrediënten: Meel (VOLKORENTARWE 41,9 %, rijst 16,9 %, VOLKORENROGGE 16,2 %, ROGGE 13,5 %, gemoute TARWE 2,5 %, HAVER 2,2 %), TARWEZEMELEN, suiker, weipoeder (van MELK), palmolie, zout, TARWEKIEMEN.Allergie-informatieBevat: Tarwe, Melk, Glutenbevattende Granen"
    expected_result = [
        "meel volkorentarwe",
        "meel rijst",
        "meel volkorenrogge",
        "meel rogge",
        "meel gemoute tarwe",
        "meel haver",
        "tarwezemelen",
        "suiker",
        "weipoeder van melk",
        "palmolie",
        "zout",
        "tarwekiemen",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_barber_cream_crackers():
    ingredients_text = "IngrediëntenIngrediënten: TARWEmeel, palmolie, gist, zout, rijsmiddel (natriumwaterstofcarbonaat)Kan ook melk bevatten.Voor allergenen, waaronder glutenbevattende granen, zie de HOOFDLETTERS ingrediënten.Allergie-informatieBevat: Tarwe, Glutenbevattende GranenKan bevatten: Melk"
    expected_result = [
        "tarwemeel",
        "palmolie",
        "gist",
        "zout",
        "rijsmiddel natriumwaterstofcarbonaat",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result
