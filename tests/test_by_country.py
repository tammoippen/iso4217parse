# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import iso3166
import iso4217parse


def test_invalid():
    assert iso4217parse.by_country(None) is None
    assert iso4217parse.by_country(1234) is None
    assert iso4217parse.by_country('Blaa') is None


def test_all_countries():
    for country in iso3166._records:
        if 'AQ' == country.alpha2:  # ignore Antarctica
            continue
        cs = iso4217parse.by_country(country.alpha2)
        if cs is None:
            print(country.alpha2, country)
        # assert isinstance(cs, list)
        # assert len(cs) > 0


def test_examples():
    exp = [
        iso4217parse.Currency(alpha3='HKD', code_num=344, name='Hong Kong dollar',
                              symbols=['HK$', 'HK＄', '＄', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', 'HK﹩', '﹩', '元'],
                              minor=2, countries=['HK']),
        iso4217parse.Currency(alpha3='CNH', code_num=None, name='Chinese yuan',
                              symbols=['CN¥', '￥', 'CN￥', '¥', 'RMB', '元'],
                              minor=2, countries=['HK']),
    ]
    assert exp == iso4217parse.by_country('HK')
