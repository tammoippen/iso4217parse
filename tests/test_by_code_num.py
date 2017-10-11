# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import iso4217parse


def test_invalid():
    assert iso4217parse.by_code_num(None) is None
    assert iso4217parse.by_code_num(1234) is None
    assert iso4217parse.by_code_num('Blaa') is None


def test_all_currencies():
    for code in iso4217parse._data()['code_num'].keys():
        assert isinstance(iso4217parse.by_code_num(code), iso4217parse.Currency)


def test_examples():
    exp = iso4217parse.Currency(alpha3='AMD', code_num=51, name='Armenian dram',
                                symbols=['֏', 'դր', 'dram'], minor=2, countries=['AM'])
    assert exp == iso4217parse.by_code_num(51)
