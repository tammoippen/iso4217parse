import pytest

import iso4217parse


@pytest.mark.parametrize(
    "symbol, country_code",
    (
        ("$", "DOESNT_EXIST"),
        ("£", "DOESNT_EXIST"),
        ("€", "DOESNT_EXIST"),
    ),
)
def test_symbol_match_ignored_without_country_match(symbol, country_code):
    assert iso4217parse.by_symbol(symbol, country_code) is None


@pytest.mark.parametrize(
    "invalid1, invalid2, valid, country_code, expected",
    (
        ("$", "Pounds Sterling", "EUR", "FR", "EUR"),
        ("Euro", "USD", "£", "GB", "GBP"),
        ("GBP", "€", "United States dollar", "US", "USD"),
    ),
)
def test_by_symbol_match_filters_country_code(
    invalid1, invalid2, valid, country_code, expected
):
    example_string = "You cannot pay in {} or {}. The price is {}3.25".format(
        invalid1,
        invalid2,
        valid,
    )
    res = iso4217parse.by_symbol_match(example_string, country_code)
    assert len(res) == 1
    assert res[0].alpha3 == expected


@pytest.mark.parametrize(
    "text, expected_alpha3",
    (
        # symbol should be lowercase
        ("lek", "ALL"),
        ("Lek", "ALL"),
        ("LEK", "ALL"),
        # symbol should be uppercase
        ("DH", "AED"),
        ("Dh", "AED"),
        ("dh", "AED"),
    ),
)
def test_parse_by_symbol_value_is_case_insensitive(text, expected_alpha3):
    res = iso4217parse.by_symbol_match(text)
    assert len(res) == 1
    assert res[0].alpha3 == expected_alpha3


@pytest.mark.parametrize(
    "text, ambiguous_alpha3, wanted_alpha3",
    (
        # ambiguous words + symbol
        ("cost $100", "WST", "USD"),  # st$ => WST
        # only letters found in words
        ("durée 100", "SZL", None),  # e => SWL / no currency
        ("maximum 100", "MRO", None),  # um => MRO / no currency
        ("flowers", "NPR", None),  # Re => NPR / no currency
        ("flowers", "LKR", None),  # Re => LKR / no currency
        ("flowers", "PKR", None),  # Re => PRK / no currency
        ("amount : 100 currency : Ks", "NPR", "MMK"),  # Re => NPR / Ks is MMK
        ("yes: 100l", "SOS", "ALL"),  # s gives SOS / l is ALL or LSL
        # alpha 3 codes found in words
        ("course", "COU", None),  # COU => COU
        ("finance", "ANG", None),  # ANG => ANG
    ),
)
def test_parse_by_symbol_value_disambiguation(text, ambiguous_alpha3, wanted_alpha3):
    assert iso4217parse.by_alpha3(ambiguous_alpha3) not in (
        iso4217parse.by_symbol_match(text) or []
    )

    if wanted_alpha3:
        assert iso4217parse.by_alpha3(wanted_alpha3) in iso4217parse.by_symbol_match(
            text
        )
    else:
        assert iso4217parse.by_symbol_match(text) is None
