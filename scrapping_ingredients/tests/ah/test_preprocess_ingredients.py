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


def test_preprocess_ingredients_zuivelhoeve_boer_n_muesli_aardbei():
    ingredients_text = "IngrediëntenIngrediënten: YOGHURT, 10% muesli [HAVERVLOKKEN, suiker, zonnebloemolie, glucose-fructosestroop, TARWEVLOKKEN, kokos, HAZELNOOT, rijstebloem, TARWEMOUT, TARWEMEEL, TARWEGLUTEN, dextrose, invertsuiker, zout, GERSTEMOUT, melasse, antioxidant (tocoferolrijk extract)], suiker, 4,2% aardbei, 1,4% aardbeipuree uit concentraat, MELKEIWIT, 1,2% aardbeiensap, rijstzetmeel, verdikkingsmiddelen (pectinen, guarpitmeel), wortelconcentraat, citroensapconcentraat, natuurlijk aroma.Allergie-informatieBevat: Melk, Glutenbevattende Granen, Noten, Hazelnoot, Tarwe, Gerst, Haver"
    expected_result = [
        "yoghurt",
        "muesli havervlokken",
        "muesli suiker",
        "muesli zonnebloemolie",
        "muesli glucose-fructosestroop",
        "muesli tarwevlokken",
        "muesli kokos",
        "muesli hazelnoot",
        "muesli rijstebloem",
        "muesli tarwemout",
        "muesli tarwemeel",
        "muesli tarwegluten",
        "muesli dextrose",
        "muesli invertsuiker",
        "muesli zout",
        "muesli gerstemout",
        "muesli melasse",
        "muesli antioxidant tocoferolrijk extract",
        "suiker",
        "aardbei",
        "aardbeipuree uit concentraat",
        "melkeiwit",
        "aardbeiensap",
        "rijstzetmeel",
        "verdikkingsmiddelen pectinen",
        "verdikkingsmiddelen guarpitmeel",
        "wortelconcentraat",
        "citroensapconcentraat",
        "natuurlijk aroma",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_ah_kruidkoekreep_zero_5_pack():
    ingredients_text = "IngrediëntenIngrediënten: roggebloem, oligofructose, zoetstof (xylitol [E967]), water, stabilisator (glycerol [E422]), rijsmiddel (natriumwaterstofcarbonaat [E500(ii)], difosfaten [E450]), zonnebloemolie, kaneel, conserveermiddel (kaliumsorbaat [E202]), specerijen.Waarvan toegevoegde suikers 0.00g per 100 gram en waarvan toegevoegd zout 0.00g per 100 gramAllergie-informatieBevat: Glutenbevattende Granen, RoggeKan bevatten: Melk, Noten, Lactose, Amandel, Hazelnoot"
    expected_result = [
        "roggebloem",
        "oligofructose",
        "zoetstof xylitol e967",
        "water",
        "stabilisator glycerol e422",
        "rijsmiddel natriumwaterstofcarbonaat e500 ii",
        "rijsmiddel difosfaten e450",
        "zonnebloemolie",
        "kaneel",
        "conserveermiddel kaliumsorbaat e202",
        "specerijen",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_ah_cocktail_augurken_zoetzuur():
    ingredients_text = "Ingrediënten: 52% augurk, water, azijn, suiker, zout, groente (rode paprika, ui), mosterdzaad, verstevigingsmiddel (calciumchloride [E509]), natuurlijk aroma.Waarvan toegevoegde suikers 4.9g per 100 gram en waarvan toegevoegd zout 0.69g per 100 gram"
    expected_result = [
        "augurk",
        "water",
        "azijn",
        "suiker",
        "zout",
        "groente rode paprika",
        "groente ui",
        "mosterdzaad",
        "verstevigingsmiddel calciumchloride e509",
        "natuurlijk aroma",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_iglo_biologische_spinazie_a_la_creme():
    ingredients_text = "Ingrediënten: Gehakte spinazie* 84%, water, ROOM* (MELK) 2,7%, magere MELKpoeder*, TARWEbloem*, koolzaadolie*, zeezout, tapiocazetmeel*, suiker*, witte peper*, nootmuskaat*. Kan MOSTERD en SELDERIJ bevatten. *van biologische oorsprong."
    expected_result = [
        "gehakte spinazie",
        "water",
        "room melk",
        "magere melkpoeder",
        "tarwebloem",
        "koolzaadolie",
        "zeezout",
        "tapiocazetmeel",
        "suiker",
        "witte peper",
        "nootmuskaat",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_ah_pureersoep_broccoli_spinazie():
    ingredients_text = "Ingrediënten: groente (52% broccoli, 17% ui, 8,9% spinazie), 19% kikkererwt, specerijen, kruiden (o.a. 0,8% peterselie), zout, gedroogde groente (prei, tomaat, wortel), natuurlijke aroma's (selderij), water, gistextract.Waarvan toegevoegde suikers 0.00g per 100 milliliter en waarvan toegevoegd zout 0.48g per 100 milliliter"
    expected_result = [
        "groente broccoli",
        "groente ui",
        "groente spinazie",
        "kikkererwt",
        "specerijen",
        "kruiden oa peterselie",
        "zout",
        "gedroogde groente prei",
        "gedroogde groente tomaat",
        "gedroogde groente wortel",
        "natuurlijke aroma's selderij",
        "water",
        "gistextract",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_indo_mie_noodles_kip_smaak():
    ingredients_text = "IngrediëntenIngrediënten: Noedels (87.8%): TARWEMEEL, palmolie (antioxidant: TBHQ), tapiocazetmeel, zout, emulgator (SOJAlecithinen), zuurteregelaars (natirumcarbonaten, kaliumcarbonaten), Kruiding (11.7%): Zout, smaakversterker (mononatriumglutamaat, dinatriuminosinaat, dinatriumguanylaat), getextureerde plantaardige proteïne, gedroogde groenten, kunstmatige kipsmaak (GRONDNOOT, SESAM), witte peper, knoflook, ui, karamel kleur. Chili poeder (0.5%). BEVATTEN: TARWE, SOJA, SESAM, GRONDNOOT. GEPRODUCEERD IN EEN FACILITEIT WAAR OOK PRODUCTEN WORDEN VERWERKT DIE SCHAALDIEREN, VIS, EI, ZUIVEL, SELDERIJ EN KEMIRINOOT BEVATTEN.Allergie-informatieBevat: Tarwe, Soja, Sesamzaad, Pinda's, Glutenbevattende GranenKan bevatten: Schaaldieren, Vis, Eieren, Selderij"
    expected_result = [
        "noedels tarwemeel",
        "palmolie antioxidant tbhq",
        "tapiocazetmeel",
        "zout",
        "emulgator sojalecithinen",
        "zuurteregelaars natirumcarbonaten",
        "zuurteregelaars kaliumcarbonaten",
        "kruiding zout",
        "smaakversterker mononatriumglutamaat",
        "smaakversterker dinatriuminosinaat",
        "smaakversterker dinatriumguanylaat",
        "getextureerde plantaardige proteïne",
        "gedroogde groenten",
        "kunstmatige kipsmaak grondnoot",
        "kunstmatige kipsmaak sesam",
        "witte peper",
        "knoflook",
        "ui",
        "karamel kleur chili poeder",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_unox_good_noodles_pittige_kip():
    ingredients_text = "IngrediëntenIngrediënten: Deegwaar (noedels) 86% (TARWEBLOEM, zonnebloemolie, zout, gemodificeerd zetmeel, suiker, rijsmiddelen (E500i, E501i), kurkuma-extract), zetmeel, smaakversterkers (E621, E631, E627), aroma, suiker, cayennepeper, mineraalzout (kalium), paprikapoeder, wortel¹, prei¹, gember 0,63%, knoflookpoeder¹, uienpoeder¹, rode chilipeper 0,31%, kleurstof (paprika-extract), peterselie¹ 0,16%, peper. Kan rogge, gerst, haver, ei, soja, melk, selderij, mosterd bevatten. ¹op duurzame wijze geteeld. Kijk voor meer informatie op: www.unox.nl.Allergie-informatieBevat: Tarwe, Glutenbevattende GranenKan bevatten: Rogge, Haver, Soja, Eieren, Mosterd, Selderij, Melk, Gerst"
    expected_result = [
        "deegwaar noedels tarwebloem",
        "deegwaar noedels zonnebloemolie",
        "deegwaar noedels zout",
        "deegwaar noedels gemodificeerd zetmeel",
        "deegwaar noedels suiker",
        "deegwaar noedels rijsmiddelen e500i",
        "deegwaar noedels rijsmiddelen e501i",
        "deegwaar noedels kurkuma-extract",
        "zetmeel",
        "smaakversterkers e621",
        "smaakversterkers e631",
        "smaakversterkers e627",
        "aroma",
        "suiker",
        "cayennepeper",
        "mineraalzout kalium",
        "paprikapoeder",
        "wortel",
        "prei",
        "gember",
        "knoflookpoeder",
        "uienpoeder",
        "rode chilipeper",
        "kleurstof paprika-extract",
        "peterselie",
        "peper",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_wasa_dun_rogge_volkoren():
    ingredients_text = "IngrediëntenIngrediënten: Volkoren ROGGEMEEL (98 g*), SESAMZAAD (11 g*), zout, gist. Kan sporen van MELK bevatten. * in g voor 100 g product.Allergie-informatieBevat: Rogge, Glutenbevattende Granen, SesamzaadKan bevatten: Melk"
    expected_result = ["volkoren roggemeel", "sesamzaad", "zout", "gist"]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_ah_rauwkost_amsterdamse_uin():
    ingredients_text = "Ingrediënten: 29% spitskool, 28% rettich, 20% rode paprika, zilverui, 2% bieslook, 2% peterselie, water, azijn, zout, aroma, zuurteregelaar (calciumchloride [E509]), zoetstof (sacharine [E954]), conserveermiddel (natriumbenzoaat [E211]), antioxidant (natriumdisulfiet [E223]), kleurstof (riboflavine [E101]).Waarvan toegevoegde suikers 0.00g per 100 gram en waarvan toegevoegd zout 0.01g per 100 gram"
    expected_result = [
        "spitskool",
        "rettich",
        "rode paprika",
        "zilverui",
        "bieslook",
        "peterselie",
        "water",
        "azijn",
        "zout",
        "aroma",
        "zuurteregelaar calciumchloride e509",
        "zoetstof sacharine e954",
        "conserveermiddel natriumbenzoaat e211",
        "antioxidant natriumdisulfiet e223",
        "kleurstof riboflavine e101",
    ]
    result = preprocess_ingredients(ingredients_text)

    assert result == expected_result


def test_preprocess_ingredients_unox_cup_a_soup_kip():
    ingredients_text = "IngrediëntenIngrediënten: Deegwaar 24% (harde TARWEGRIES, zout), dextrose, aardappelzetmeel, aroma, wortel¹ 4,8%, zout, gistextract, suiker, palmvet, stukjes kippenvlees 2,3% (kippenvlees, palmolie, zout, antioxidant (E304i, E307), gejodeerd zout, mineraalzout (kalium), kippenvet 0,9% (kippenvet, antioxidant E392), prei¹, specerijen¹ (kurkuma, peterseliewortel), uipoeder¹, BLADSELDERIJ 0,2%. Kan ei, soja, melk, mosterd bevatten.¹ op duurzame wijze geteeld.Allergie-informatieBevat: Selderij, Glutenbevattende Granen, TarweKan bevatten: Soja, Eieren, Melk, Mosterd"

    with pytest.raises(ValueError):
        preprocess_ingredients(ingredients_text)
