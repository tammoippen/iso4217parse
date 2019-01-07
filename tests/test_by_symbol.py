# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function,
    unicode_literals,
)

import pytest

import iso4217parse


@pytest.mark.parametrize(
    'symbol, country_code',
    (
        ('$', 'DOESNT_EXIST'),
        ('£', 'DOESNT_EXIST'),
        ('€', 'DOESNT_EXIST'),
    ),
)
def test_symbol_match_ignored_without_country_match(symbol, country_code):
    assert iso4217parse.by_symbol(symbol, country_code) is None


@pytest.mark.parametrize(
    'invalid1, invalid2, valid, country_code, expected',
    (
        ('$', 'Pounds Sterling', 'EUR', 'FR', 'EUR'),
        ('Euro', 'USD', '£', 'GB', 'GBP'),
        ('GBP', '€', 'United States dollar', 'US', 'USD'),
    ),
)
def test_by_symbol_match_filters_country_code(
        invalid1, invalid2, valid, country_code, expected):
    example_string = 'You cannot pay in {} or {}. The price is {}3.25'.format(
        invalid1, invalid2, valid,
    )
    res = iso4217parse.by_symbol_match(example_string, country_code)
    assert len(res) == 1
    assert res[0].alpha3 == expected
