import pytest

import iso4217parse as iso4217


def test_invalid():
    for v in (None, [], {}, 3.14):
        with pytest.raises(ValueError):
            iso4217.parse(v)


def test_examples_code():
    for code, exp in iso4217._data().alpha3.items():
        assert [exp] == iso4217.parse(code)


def test_examples_numbers():
    for num in range(1000):
        exp = iso4217.by_code_num(num)
        if exp is None:
            assert [] == iso4217.parse(num)
        else:
            assert [exp] == iso4217.parse(num)


def test_examples_EUR():
    exp = iso4217.Currency(
        alpha3="EUR",
        code_num=978,
        name="Euro",
        symbols=["€", "euro", "euros"],
        minor=2,
        countries=[
            "AD",
            "AT",
            "AX",
            "BE",
            "BL",
            "CY",
            "DE",
            "EE",
            "ES",
            "FI",
            "FR",
            "GF",
            "GP",
            "GR",
            "IE",
            "IT",
            "LT",
            "LU",
            "LV",
            "MC",
            "ME",
            "MF",
            "MQ",
            "MT",
            "NL",
            "PM",
            "PT",
            "RE",
            "SI",
            "SK",
            "SM",
            "TF",
            "VA",
            "XK",
            "YT",
        ],
    )

    assert [exp] == iso4217.parse("Price is 5 €")
    assert [exp] == iso4217.parse("Price is 5 EUR")
    assert [exp] == iso4217.parse("Price is 5 eur")
    assert [exp] == iso4217.parse("Price is 5 euro")
    assert [exp] == iso4217.parse("Price is 5 Euro")

    exp = iso4217.Currency(
        alpha3="CAD",
        code_num=124,
        name="Canadian dollar",
        symbols=[
            "CA$",
            "CA＄",
            "＄",
            "$",
            "dollar",
            "dollars",
            "Dollar",
            "Dollars",
            "CA﹩",
            "﹩",
        ],
        minor=2,
        countries=["CA"],
    )

    assert [exp] == iso4217.parse("CA﹩15.76")


def test_examples_CZK():
    expect = iso4217.by_alpha3("CZK")

    assert [expect] == iso4217.parse("1499 CZK")
