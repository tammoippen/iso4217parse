# The MIT License

# Copyright (c) 2017 - 2024 Tammo Ippen, tammo.ippen@posteo.de

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
from dataclasses import dataclass
from functools import lru_cache
import importlib.resources
import json
import re
from typing import Optional


__all__ = [
    "Currency",
    "by_alpha3",
    "by_code_num",
    "by_symbol",
    "by_symbol_match",
    "by_country",
    "parse",
]

Currency = namedtuple(
    "Currency",
    [
        "alpha3",  # unicode:       the ISO4217 alpha3 code
        "code_num",  # int:           the ISO4217 numeric code
        "name",  # unicode:       the currency name
        "symbols",  # List[unicode]: list of possible symbols;
        #                first is opinionated choice for representation
        "minor",  # int:           number of decimal digits to round
        "countries",  # List[unicode]: list of countries that use this currency.
    ],
)


@dataclass
class Data:
    alpha3: dict[str, Currency]
    code_num: dict[str, Currency]
    symbol: dict[str, list[Currency]]
    name: dict[str, Currency]
    country: dict[str, list[Currency]]


_DATA: Optional[Data] = None
_SYMBOLS: Optional[list[tuple[str, str]]] = None


def _data() -> Data:
    """(Lazy)load index data structure for currencies

    Load the `data.json` file (created with `gen_data.py`) and index by alpha3,
    code_num, symbol and country.

    Returns:
        Dict[str, Dict[str, Any]]: Currency data indexed by different angles
    """
    global _DATA
    if _DATA is None:
        with importlib.resources.open_text("iso4217parse", "data.json") as f:
            alpha3 = {k: Currency(**v) for k, v in json.load(f).items()}

        code_num = {d.code_num: d for d in alpha3.values() if d.code_num is not None}
        symbol: dict[str, list[Currency]] = defaultdict(list)
        for d in alpha3.values():
            for s in d.symbols:
                symbol[s] += [d]

        for s, ds in symbol.items():
            symbol[s] = sorted(
                ds, key=lambda d: 10000 if d.code_num is None else d.code_num
            )

        name = {}
        for d in alpha3.values():
            if d.name in name:
                assert 'Duplicate name "{}"!'.format(d.name)
            name[d.name] = d

        country: dict[str, list[Currency]] = defaultdict(list)
        for d in alpha3.values():
            for cc in d.countries:
                country[cc] += [d]

        for s, ds in country.items():
            country[s] = sorted(
                ds,
                key=lambda d: (
                    int(d.symbols == []),  # at least one symbol
                    10000 if d.code_num is None else d.code_num,  # official first
                    len(d.countries),  # the fewer countries the more specific
                ),
            )
        _DATA = Data(
            alpha3=alpha3, code_num=code_num, symbol=symbol, name=name, country=country
        )

    return _DATA


def _symbols() -> list[tuple[str, str]]:
    """(Lazy)load list of all supported symbols (sorted)

    Look into `_data()` for all currency symbols, then sort by length and
    unicode-ord (A-Z is not as relevant as ֏).

    Returns:
        List[unicode]: Sorted list of possible currency symbols.
    """
    global _SYMBOLS
    if _SYMBOLS is None:
        tmp = [(s, "symbol") for s in _data().symbol.keys()]
        tmp += [(s, "alpha3") for s in _data().alpha3.keys()]
        tmp += [(s, "name") for s in _data().name.keys()]
        _SYMBOLS = sorted(tmp, key=lambda s: (len(s[0]), ord(s[0][0])), reverse=True)

    return _SYMBOLS


def by_alpha3(code: str) -> Optional[Currency]:
    """Get Currency for ISO4217 alpha3 code

    Parameters:
        code: unicode  An alpha3 iso4217 code.

    Returns:
        Currency: Currency object for `code`, if available.
    """
    return _data().alpha3.get(code)


def by_code_num(code_num: str) -> Optional[Currency]:
    """Get Currency for ISO4217 numeric code

    Parameters:
        code_num: int  An iso4217 numeric code.

    Returns:
        Currency: return Currency object for `code_num`, if available.
    """
    return _data().code_num.get(code_num)


def by_symbol(
    symbol: str, country_code: Optional[str] = None
) -> Optional[list[Currency]]:
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
    res = _data().symbol.get(symbol)
    if res:
        tmp_res = []
        for d in res:
            if country_code in d.countries:
                tmp_res += [d]

        if tmp_res:
            return tmp_res
        if country_code is None:
            return res
    return None


@lru_cache(maxsize=1024)
def _symbol_pattern(symbol: str) -> re.Pattern:
    symbol_pattern = re.escape(symbol)
    return re.compile(rf"(^|\b|\d|\s){symbol_pattern}([^A-Z]|$)", re.I)


def by_symbol_match(
    value: str, country_code: Optional[str] = None
) -> Optional[list[Currency]]:
    """Get list of possible currencies where the symbol is in value; filter by country_code (iso3166 alpha2 code)

    Look for first matching currency symbol in `value`. Filter similar to `by_symbol`.
    Symbols are sorted by length and relevance of first character (see `_symbols()`).

    Symbols are considered to be currency symbols, alpha3 codes or currency names.

    Note: This is a [heuristic](https://en.wikipedia.org/wiki/Heuristic) !

    Parameters:
        value: unicode                   Some input string.
        country_code: Optional[unicode]  Iso3166 alpha2 country code.

    Returns:
        List[Currency]: Currency objects found in `value`; filter by country_code.
    """
    res: Optional[list[Currency]] = None
    for symbol, group in _symbols():
        symbol_pattern = _symbol_pattern(symbol)
        if symbol_pattern.search(value):
            if group == "symbol":
                res = by_symbol(symbol, country_code)
            if group == "alpha3":
                curr = by_alpha3(symbol)
                assert curr is not None
                res = [curr]
            if group == "name":
                curr = _data().name[symbol]
                assert curr is not None
                res = [curr]
            if res and country_code is not None:
                res = [
                    currency for currency in res if country_code in currency.countries
                ]
            res = list(filter(None, res or []))
            if res:
                return res
    return None


def by_country(country_code: str) -> Optional[list[Currency]]:
    """Get all currencies used in country

    Parameters:
        country_code: unicode  iso3166 alpha2 country code

    Returns:
        List[Currency]: Currency objects used in country.

    """
    return _data().country.get(country_code)


def parse(v: str, country_code: Optional[str] = None) -> Optional[list[Currency]]:
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
        res = by_code_num(v)
        return [] if not res else [res]

    if not isinstance(v, str):
        raise ValueError(
            "`v` of incorrect type {}. Only accepts str, bytes, unicode and int."
        )

    # check alpha3
    if re.match("^[A-Z]{3}$", v):
        res = by_alpha3(v)
        if res:
            return [res]

    # check by symbol
    ress = by_symbol(v, country_code)
    if ress:
        return ress

    # check by country code
    ress = by_country(v)
    if ress:
        return ress

    # more or less fuzzy match by symbol
    ress = by_symbol_match(v, country_code)
    if ress:
        return ress
    return None
