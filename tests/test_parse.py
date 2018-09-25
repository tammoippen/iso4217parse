# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import iso4217parse as iso4217


def test_examples():
    exp = iso4217.Currency(
        alpha3='CHF',
        code_num=756,
        name='Swiss franc',
        symbols=['SFr.', 'fr', 'Fr.', 'F', 'franc', 'francs', 'Franc', 'Francs'],
        minor=2,
        countries=['CH', 'LI'],
    )

    assert [exp] == iso4217.parse('CHF')

    exp = iso4217.Currency(
        alpha3='CUP',
        code_num=192,
        name='Cuban peso',
        symbols=['₱', '＄', '﹩', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', '＄MN', '﹩MN', '$MN'],
        minor=2,
        countries=['CU'],
    )

    assert [exp] == iso4217.parse(192)

    exp = iso4217.Currency(
        alpha3='EUR',
        code_num=978,
        name='Euro',
        symbols=['€', 'euro', 'euros'],
        minor=2,
        countries=['AD', 'AT', 'AX', 'BE', 'BL', 'CY', 'DE', 'EE', 'ES', 'FI',
                   'FR', 'GF', 'GP', 'GR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MC',
                   'ME', 'MF', 'MQ', 'MT', 'NL', 'PM', 'PT', 'RE', 'SI', 'SK',
                   'SM', 'TF', 'VA', 'XK', 'YT'],
    )

    assert [exp] == iso4217.parse('Price is 5 €')

    exp = iso4217.Currency(
        alpha3='CAD',
        code_num=124,
        name='Canadian dollar',
        symbols=['CA$', 'CA＄', '＄', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', 'CA﹩', '﹩'],
        minor=2,
        countries=['CA'],
    )

    assert [exp] == iso4217.parse('CA﹩15.76')
