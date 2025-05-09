from ...ah.preprocessing_ingredients import split_ingredients


def test_split_ingredients_empty():
    ingredients_text = ""
    expected_result = [""]
    result = split_ingredients(ingredients_text)

    assert result == expected_result


def test_split_ingredients_wasa_sesam():
    ingredients_text = (
        "volkoren tarwemeel, tarwemeel, sesamzaad, gist, zonnebloemolie, suiker, zout"
    )
    expected_result = [
        "volkoren tarwemeel",
        "tarwemeel",
        "sesamzaad",
        "gist",
        "zonnebloemolie",
        "suiker",
        "zout",
    ]
    result = split_ingredients(ingredients_text)

    assert result == expected_result


def test_split_ingredients_one_bracket():
    """
    This test if the brackets get resolved for the first, middle, and last ingredient
    """
    ingredients_text = (
        "meel (tarwe, wit), tarwemeel, sesamzaad, gist, olie zonnebloem, suiker"
    )
    expected_result = [
        "meel tarwe",
        "meel wit",
        "tarwemeel",
        "sesamzaad",
        "gist",
        "olie zonnebloem",
        "suiker",
    ]
    result = split_ingredients(ingredients_text)

    assert result == expected_result


def test_split_ingredients_brackets():
    """
    This test if the brackets get resolved for the first, middle, and last ingredient
    """
    ingredients_text = "meel (tarwe, wit), tarwemeel, sesamzaad, gist, olie (zonnebloem, raap), suiker, zout (zee, grof)"
    expected_result = [
        "meel tarwe",
        "meel wit",
        "tarwemeel",
        "sesamzaad",
        "gist",
        "olie zonnebloem",
        "olie raap",
        "suiker",
        "zout zee",
        "zout grof",
    ]
    result = split_ingredients(ingredients_text)

    assert result == expected_result


def test_split_ingredients_nested_brackets():
    """
    This test if the brackets get resolved for the first, middle, and last ingredient
    """
    ingredients_text = "meel (tarwe, wit (pretty, ugly)), tarwemeel, sesamzaad, gist, olie (zonnebloem, raap (pretty, ugly)), suiker, zout (zee (pretty, ugly), grof)"
    expected_result = [
        "meel tarwe",
        "meel wit pretty",
        "meel wit ugly",
        "tarwemeel",
        "sesamzaad",
        "gist",
        "olie zonnebloem",
        "olie raap pretty",
        "olie raap ugly",
        "suiker",
        "zout zee pretty",
        "zout zee ugly",
        "zout grof",
    ]
    result = split_ingredients(ingredients_text)

    assert result == expected_result
