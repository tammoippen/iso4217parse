# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from collections import defaultdict, namedtuple
import json
import re
import sys

from pkg_resources import resource_filename

_PY3 = sys.version_info[0] == 3

if _PY3:
    unicode = str


Currency = namedtuple('Currency', [
    'alpha3',     # unicode:       the ISO4217 alpha3 code
    'code_num',   # int:           the ISO4217 numeric code
    'name',       # unicode:       the currency name
    'symbols',    # List[unicode]: list of possible symbols;
                  #                first is opinionated choice for representation
    'minor',      # int:           number of decimal digits to round
    'countries',  # List[unicode]: list of countries that use this currency.
])


_DATA = None
_SYMBOLS = None


def _data():
    """(Lazy)load index data structure for currences

    Load the `data.json` file (created with `gen_data.py`) and index by alpha3,
    code_num, symbol and country.

    Returns:
        Dict[str, Dict[str, Any]]: Currency data indexed by different angles
    """
    global _DATA
    if _DATA is None:
        _DATA = {}
        with open(resource_filename(__name__, 'data.json'), 'r', encoding='utf-8') as f:
            _DATA['alpha3'] = {k: Currency(**v) for k, v in json.load(f).items()}

        _DATA['code_num'] = {d.code_num: d for d in _DATA['alpha3'].values() if d.code_num is not None}
        _DATA['symbol'] = defaultdict(list)
        for d in _DATA['alpha3'].values():
            for s in d.symbols:
                _DATA['symbol'][s] += [d]

        for s, d in _DATA['symbol'].items():
            _DATA['symbol'][s] = sorted(d, key=lambda d: 10000 if d.code_num is None else d.code_num)

        _DATA['country'] = defaultdict(list)
        for d in _DATA['alpha3'].values():
            for cc in d.countries:
                _DATA['country'][cc] += [d]

        for s, d in _DATA['country'].items():
            _DATA['country'][s] = sorted(d, key=lambda d: (
                int(d.symbols == []),  # at least one symbol
                10000 if d.code_num is None else d.code_num,  # official first
                len(d.countries),  # the fewer countries the more specific
            ))

    return _DATA


def _symbols():
    """(Lazy)load list of all supported symbols (sorted)

    Look into `_data()` for all currency symbols, then sort by length and
    unicode-ord (A-Z is not as relevant as ֏).

    Returns:
        List[unicode]: Sorted list of possible currency symbols.
    """
    global _SYMBOLS
    if _SYMBOLS is None:
        _SYMBOLS = sorted(
            _data()['symbol'].keys(),
            key=lambda s: (len(s), ord(s[0])),
            reverse=True)

    return _SYMBOLS


def by_alpha3(code):
    """Get Currency for ISO4217 alpha3 code

    Parameters:
        code: unicode  An alpha3 iso4217 code.

    Returns:
        Currency: Currency object for `code`, if available.
    """
    return _data()['alpha3'].get(code)


def by_code_num(code_num):
    """Get Currency for ISO4217 numeric code

    Parameters:
        code_num: int  An iso4217 numeric code.

    Returns:
        Currency: return Currency object for `code_num`, if available.
    """
    return _data()['code_num'].get(code_num)


def by_symbol(symbol, country_code=None):
    """Get list of possible currencies for symbol; filter by country_code

    Look for all currencies that use the `symbol`. If there are currencies used
    in the country of `country_code`, return only those; otherwise return all
    found currencies.

    Parameters:
        symbol: unicode                  Currency symbol.
        country_code: Optional[unicode]  Iso3166 alpha2 country code.

    Returns:
        List[Currency]: Currency objects for `symbol`; filter by country_code.
    """
    res = _data()['symbol'].get(symbol)
    if res:
        tmp_res = []
        for d in res:
            if country_code in d.countries:
                tmp_res += [d]

        if tmp_res:
            return tmp_res
        return res


def by_symbol_match(value, country_code=None):
    """Get list of possible currencies where the symbol is in value; filter by country_code (iso3166 alpha2 code)

    Look for first matching currency symbol in `value`. Filter similar to `by_symbol`.
    Symbols are sorted by length and relevance of first character (see `_symbols()`).

    Note: This is a [heuristic](https://en.wikipedia.org/wiki/Heuristic) !

    Parameters:
        value: unicode                   Some input string.
        country_code: Optional[unicode]  Iso3166 alpha2 country code.

    Returns:
        List[Currency]: Currency objects found in `value`; filter by country_code.
    """
    for s in _symbols():
        if s in value:
            res = by_symbol(s, country_code)
            if res:
                return res


def by_country(country_code):
    """Get all currencies used in country

    Parameters:
        country_code: unicode  iso3166 alpha2 country code

    Returns:
        List[Currency]: Currency objects used in country.

    """
    return _data()['country'].get(country_code)


def parse(v, country_code=None):
    """Try parse `v` to currencies; filter by country_code

    If `v` is a number, try `by_code_num()`; otherwise try:
        1) if `v` is 3 character uppercase: `by_alpha3()`
        2) Exact symbol match: `by_symbol()`
        3) Exact country code match: `by_country()`
        4) Fuzzy by symbol match heuristic: `by_symbol_match()`

    Parameters:
        v: Union[unicode, int]           Either a iso4217 numeric code or some string
        country_code: Optional[unicode]  Iso3166 alpha2 country code.

    Returns:
        List[Currency]: found Currency objects.
    """
    if isinstance(v, int):
        return [by_code_num(v)]

    if not isinstance(v, (str, unicode)):
        raise ValueError('`v` of incorrect type {}. Only accepts str, bytes, unicode and int.')

    # check alpha3
    if re.match('^[A-Z]{3}$', v):
        res = by_alpha3(v)
        if res:
            return [res]

    # check by symbol
    res = by_symbol(v, country_code)
    if res:
        return res

    # check by country code
    res = by_country(v)
    if res:
        return res

    # more or less fuzzy match by symbol
    res = by_symbol_match(v, country_code)
    if res:
        return res
