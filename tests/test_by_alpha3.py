# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import iso4217parse


def test_invalid():
    assert iso4217parse.by_alpha3(None) is None
    assert iso4217parse.by_alpha3(1234) is None
    assert iso4217parse.by_alpha3('Blaa') is None


def test_all_currencies():
    for code in iso4217parse._data()['alpha3'].keys():
        assert isinstance(iso4217parse.by_alpha3(code), iso4217parse.Currency)


def test_examples():
    exp = iso4217parse.Currency(alpha3='CHF', code_num=756, name='Swiss franc',
                                symbols=['SFr.', 'fr', 'Fr.', 'F', 'franc', 'francs', 'Franc', 'Francs'],
                                minor=2, countries=['CH', 'LI'])
    assert exp == iso4217parse.by_alpha3('CHF')
