[![CircleCI](https://circleci.com/gh/tammoippen/iso4217parse.svg?style=svg)](https://circleci.com/gh/tammoippen/iso4217parse)
[![Coverage Status](https://coveralls.io/repos/github/tammoippen/iso4217parse/badge.svg?branch=master)](https://coveralls.io/github/tammoippen/iso4217parse?branch=master)
[![Tested CPython Versions](https://img.shields.io/badge/cpython-2.7%2C%203.5%2C%203.6%2C%203.7-brightgreen.svg)](https://img.shields.io/badge/cpython-2.7%2C%203.5%2C%203.6%2C%203.7-brightgreen.svg)
[![Tested PyPy Versions](https://img.shields.io/badge/pypy-2.7--6.0.0%2C%203.5--6.0.0-brightgreen.svg)](https://img.shields.io/badge/pypy-2.7--6.0.0%2C%203.5--6.0.0-brightgreen.svg)
[![PyPi version](https://img.shields.io/pypi/v/iso4217parse.svg)](https://pypi.python.org/pypi/iso4217parse)
[![PyPi license](https://img.shields.io/pypi/l/iso4217parse.svg)](https://pypi.python.org/pypi/iso4217parse)

# ISO4217 Currency Parser

Parse currencies (symbols and codes) from and to [ISO4217](https://en.wikipedia.org/wiki/ISO_4217).

Similar to [iso4217](https://github.com/spoqa/iso4217) package, but

 * data is aquired by scraping wikipedia (see [below](#data-aquisition)) - this is repeatable and you stay on the most current data
 * currency symbols are currated by hand - this allows some fuzzy currency matching
 * no download and parsing during install
 * no external dependancies (`enum34`)

When you want to *reuse* the [*data.json*](https://github.com/tammoippen/iso4217parse/blob/master/iso4217parse/data.json) file for your projects, please leave a attribution note. I licence the file under (CC BY 4.0).

Install:
```
pip install iso4217parse
```

## Documentation

Each currency is modeled as a `collections.namedtuple`:
```python
Currency = namedtuple('Currency', [
    'alpha3',     # unicode:       the ISO4217 alpha3 code
    'code_num',   # int:           the ISO4217 numeric code
    'name',       # unicode:       the currency name
    'symbols',    # List[unicode]: list of possible symbols;
                  #                first is opinionated choice for representation
    'minor',      # int:           number of decimal digits to round
    'countries',  # List[unicode]: list of countries that use this currency.
])
```

**parse:**  Try to parse the input in a best effort approach by using `by_alpha3()`, `by_code_num()`, ... functions:
```python
In [1]: import iso4217parse

In [2]: iso4217parse.parse('CHF')
Out[2]: [Currency(alpha3='CHF', code_num=756, name='Swiss franc',
                  symbols=['SFr.', 'fr', 'Fr.', 'F', 'franc', 'francs', 'Franc', 'Francs'],
                  minor=2, countries=['CH', 'LI'])]

In [3]: iso4217parse.parse(192)
Out[3]:
[Currency(alpha3='CUP', code_num=192, name='Cuban peso',
          symbols=['₱', '＄', '﹩', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', '＄MN', '﹩MN', '$MN'],
          minor=2, countries=['CU'])]

In [4]: iso4217parse.parse('Price is 5 €')
Out[4]: [Currency(alpha3='EUR', code_num=978, name='Euro',
         symbols=['€', 'euro', 'euros'], minor=2,
         countries=['AD', 'AT', 'AX', 'BE', 'BL', 'CY', 'DE', 'EE', 'ES', 'FI',
                   'FR', 'GF', 'GP', 'GR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MC',
                   'ME', 'MF', 'MQ', 'MT', 'NL', 'PM', 'PT', 'RE', 'SI', 'SK',
                   'SM', 'TF', 'VA', 'XK', 'YT'])]

In [5]: iso4217parse.parse('CA﹩15.76')
Out[5]: [Currency(alpha3='CAD', code_num=124, name='Canadian dollar',
         symbols=['CA$', 'CA＄', '＄', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', 'CA﹩', '﹩'],
         minor=2, countries=['CA'])]

In [6]: iso4217parse.parse?
Signature: iso4217parse.parse(v, country_code=None)
Docstring:
Try parse `v` to currencies; filter by country_code

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
```

**by_alpha3:** Get the currency by its iso4217 alpha3 code:
```python
In [1]: import iso4217parse

In [2]: iso4217parse.by_alpha3('CHF')
Out[2]: Currency(alpha3='CHF', code_num=756, name='Swiss franc',
                 symbols=['SFr.', 'fr', 'Fr.', 'F', 'franc', 'francs', 'Franc', 'Francs'],
                 minor=2, countries=['CH', 'LI'])

In [3]: iso4217parse.by_alpha3?
Signature: iso4217parse.by_alpha3(code)
Docstring:
Get Currency for ISO4217 alpha3 code

Parameters:
    code: unicode  An alpha3 iso4217 code.

Returns:
    Currency: Currency object for `code`, if available.
```

**by_code_num:** Get the currency by its iso4217 numeric code:
```python
In [1]: import iso4217parse

In [2]: iso4217parse.by_code_num(51)
Out[2]: Currency(alpha3='AMD', code_num=51, name='Armenian dram',
                 symbols=['֏', 'դր', 'dram'], minor=2, countries=['AM'])

In [3]: iso4217parse.by_code_num?
Signature: iso4217parse.by_code_num(code_num)
Docstring:
Get Currency for ISO4217 numeric code

Parameters:
    code_num: int  An iso4217 numeric code.

Returns:
    Currency: Currency object for `code_num`, if available.
```

**by_country:** Get currencies used in a country:
```python
In [1]: import iso4217parse

In [2]: iso4217parse.country('HK')
Out[2]:
[
  Currency(alpha3='HKD', code_num=344, name='Hong Kong dollar',
           symbols=['HK$', 'HK＄', '＄', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', 'HK﹩', '﹩', '元'],
           minor=2, countries=['HK']),
  Currency(alpha3='CNH', code_num=None, name='Chinese yuan (when traded offshore)',
           symbols=['CN¥', '￥', 'CN￥', '¥', 'RMB', '元'],
           minor=2, countries=['HK'])
]

In [3]: iso4217parse.country?
Signature: iso4217parse.by_country(country_code)
Docstring:
Get all currencies used in country

Parameters:
    country_code: unicode  iso3166 alpha2 country code

Returns:
    List[Currency]: Currency objects used in country.
```

**by_symbol:** Get currencies that use the given symbol:
```python
In [1]: import iso4217parse

In [2]: iso4217parse.by_symbol('＄MN')
Out[2]:
[
  Currency(alpha3='CUP', code_num=192, name='Cuban peso',
           symbols=['₱', '＄', '﹩', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', '＄MN', '﹩MN', '$MN'],
           minor=2, countries=['CU'])
]

In [3]: iso4217parse.by_symbol('＄')
Out[3]: [...] # 35 different currencies

In [4]: [c.alpha3 for c in iso4217parse.by_symbol('＄')]
Out[4]:
['ARS', 'AUD', 'BBD', 'BMD', 'BZD', 'SBD', 'BND', 'CAD', 'CVE', 'KYD', 'CLP',
 'COP', 'CUP', 'DOP', 'FJD', 'GYD', 'HKD', 'JMD', 'LRD', 'MXN', 'NAD', 'NZD',
 'SGD', 'TTD', 'USD', 'UYU', 'TWD', 'CUC', 'ZWL', 'XCD', 'SRD', 'BRL', 'KID',
 'NTD', 'TVD']

In [5]: iso4217parse.by_symbol('＄', country_code='US')
Out[5]:
[
  Currency(alpha3='USD', code_num=840, name='United States dollar',
           symbols=['US$', '$', '＄', '﹩', 'dollar', 'dollars', 'Dollar', 'Dollars', 'US＄', 'US﹩'],
           minor=2,
           countries=['AS', 'EC', 'GU', 'HT', 'MH', 'MP', 'PR', 'PW', 'SV', 'TC', 'TL', 'UM', 'US'])
]

In [6]: iso4217parse.by_symbol?
Signature: iso4217parse.by_symbol(symbol, country_code=None)
Docstring:
Get list of possible currencies for symbol; filter by country_code

Look for all currencies that use the `symbol`. If there are currencies used
in the country of `country_code`, return only those; otherwise return all
found currencies.

Parameters:
    symbol: unicode                  Currency symbol.
    country_code: Optional[unicode]  Iso3166 alpha2 country code.

Returns:
    List[Currency]: Currency objects for `symbol`; filter by country_code.
```

**by_symbol_match:** Look for currency symbol occurence in input string:
```python
In [1]: import iso4217parse

In [2]: iso4217parse.by_symbol_match('RD$35.8')
Out[2]:
[
  Currency(alpha3='DOP', code_num=214, name='Dominican peso',
           symbols=['RD$', '＄', '﹩', '$', 'dollar', 'dollars', 'Dollar', 'Dollars', 'RD＄', 'RD﹩'],
           minor=2, countries=['DO'])
]

In [3]: iso4217parse.by_symbol_match('The price is ₨ 35.8 !')
Out[3]:
[
  Currency(alpha3='LKR', code_num=144, name='Sri Lankan rupee',
           symbols=['රු', '₨', 'Rs', 'ரூ', 'SLRs', 'rupees', 'rupee'],
           minor=2, countries=['LK']),
  Currency(alpha3='MUR', code_num=480, name='Mauritian rupee',
           symbols=['₨', 'rupees', 'rupee'], minor=2, countries=['MU']),
  Currency(alpha3='NPR', code_num=524, name='Nepalese rupee',
           symbols=['रु', '₨', 'Rs', 'Re', 'rupees', 'rupee'], minor=2, countries=['NP']),
  Currency(alpha3='PKR', code_num=586, name='Pakistani rupee',
           symbols=['₨', 'Rs', 'rupees', 'rupee'],
           minor=2, countries=['PK'])
]

In [4]: iso4217parse.by_symbol_match('The price is ₨ 35.8 !', country_code='NP')
Out[4]:
[
  Currency(alpha3='NPR', code_num=524, name='Nepalese rupee',
           symbols=['रु', '₨', 'Rs', 'Re', 'rupees', 'rupee'],
           minor=2, countries=['NP'])
]

In [5]: iso4217parse.by_symbol_match?
Signature: iso4217parse.by_symbol_match(value, country_code=None)
Docstring:
Get list of possible currencies where the symbol is in value; filter by country_code (iso3166 alpha2 code)

Look for first matching currency symbol in `value`. Filter similar to `by_symbol`.
Symbols are sorted by length and relevance of first character (see `_symbols()`).

Note: This is a [heuristic](https://en.wikipedia.org/wiki/Heuristic) !

Parameters:
    value: unicode                   Some input string.
    country_code: Optional[unicode]  Iso3166 alpha2 country code.

Returns:
    List[Currency]: Currency objects found in `value`; filter by country_code.
```


## Data aquisition

Basic ISO4217 currency information is gathered from wikipedia: https://en.wikipedia.org/wiki/ISO_4217 . The tables are parsed with `gen_data.py` and stored in `iso4217parse/data.json`. This gives information for `alpha3`, `code_num`, `name`, `minor` and `countries`. The currency symbol information is hand gathered from:

* individuel wikipedia pages, i.e. [EUR](https://en.wikipedia.org/wiki/Euro) has a `Denominations` -> `Symbol` section.
* http://www.iotafinance.com/en/ISO-4217-Currency-Codes.html
* http://www.xe.com/currency/ , i.e. [GBP](http://www.xe.com/currency/gbp-british-pound) has a `Currency Facts` -> `Symbol` section

and stored in `iso4217parse/symbols.json`. Each currency can have multiple currency symbols - the first symbol in the list is the (opinionated) choice
for the currency.

**Contribution Note**: Possible ways to contribute here:

* hand check symbols for currency code.
* automatic generation of the `iso4217parse/symbols.json` file.
