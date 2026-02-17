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


# This is a helper script to generate `data.json`!
# use like `python3 gen_data.py <output-path> [<tmp-output = 0>]`

# execute with python 3.4 or later (pathlib)
# pip install requests lxml bs4 iso3166 dateparser

import json
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup
import iso3166
import requests

# symbols see subsequent pages and http://www.xe.com/currency/
res = requests.get(
    "https://en.wikipedia.org/wiki/ISO_4217",
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0 Safari/537.36"
    }
)
soup = BeautifulSoup(res.content, "lxml")

tables = soup.findAll("table")

if len(sys.argv) < 2:
    print("Use like: python3 {} <output-path> [<tmp-output = 0>]".format(sys.argv[0]))
    sys.exit(42)

p = Path(sys.argv[1]).absolute()
if not p.is_dir():
    print("Use like: python3 {} <output-path> [<tmp-output = 0>]".format(sys.argv[0]))
    sys.exit(42)

tmp_out = False
if len(sys.argv) == 3:
    tmp_out = bool(int(sys.argv[2]))

# some names do not resolve with iso3166 package; or are special
alt_iso3166 = {
    "Bolivia": "BO",
    "Democratic Republic of the Congo": "CD",
    "Somaliland": "SO",
    "Transnistria": "MD",
    "Venezuela": "VE",
    "Caribbean Netherlands": "BQ",
    "British Virgin Islands": "VG",
    "Federated States of Micronesia": "FM",
    "U.S. Virgin Islands": "VI",
    "Republic of the Congo": "CG",
    "Sint Maarten": "SX",
    "Cocos   Islands": "CC",
    "the Isle of Man": "IM",
    "and Guernsey": "GG",
    "Pitcairn Islands": "PN",
    "French territories of the Pacific Ocean: French Polynesia": "PF",
    "Kosovo": "XK",
}

additional_countries = {
    "EUR": [
        "Åland Islands",
        "French Guiana",
        "French Southern Territories",
        "Holy See",
        "Saint Martin (French part)",
    ],
    "SEK": ["Åland Islands"],
    "EGP": [
        "Palestine, State of"
    ],  # see https://en.wikipedia.org/wiki/State_of_Palestine
    "ILS": ["Palestine, State of"],
    "JOD": ["Palestine, State of"],
    "FKP": ["South Georgia and the South Sandwich Islands"],
    # 'Sahrawi peseta': ['Western Sahara'],
    "MAD": ["Western Sahara"],
    "DZD": ["Western Sahara"],
    "MRO": ["Western Sahara"],
}

# get active table
active = []
for row in tables[1].findAll("tr"):  # noqa
    tds = row.findAll("td")
    if tds:
        try:
            minor = int(re.sub(r"\[[0-9]+\]", r"", tds[2].text.replace("*", "")))
        except:  # noqa: E722
            minor = 0
        d = dict(
            code=tds[0].text,
            code_num=int(tds[1].text),
            minor=minor,
            name=re.sub(r"\[[0-9]+\]", r"", tds[3].text).strip(),
            countries=tds[4].text.replace("\xa0", ""),
        )

        d["countries"] = re.sub(r"\([^)]+\)", r" ", d["countries"])
        d["countries"] = re.sub(r"\[[0-9]+\]", r" ", d["countries"]).strip()
        d["countries"] = [c.strip() for c in d["countries"].split(",") if c]
        if d["code"] in additional_countries:
            d["countries"] += additional_countries[d["code"]]
        ccodes = []
        for c in d["countries"]:
            if c in alt_iso3166:
                ccodes += [alt_iso3166[c]]
            m = re.match(r".*\(([A-Z]{2})\).*", c)
            if m:
                ccodes += [m.group(1)]
            else:
                code = iso3166.countries.get(c, None)
                if code:
                    ccodes += [code.alpha2]
                else:
                    code = iso3166.countries.get(d["code_num"], None)
                    if code:
                        ccodes += [code.alpha2]
        if len(d["countries"]) != len(set(ccodes)) and d["code"] not in {
            "SHP",
            "XDR",
            "XSU",
            "XUA",
        }:
            print(d["countries"], set(ccodes))
        d["country_codes"] = sorted(set(ccodes))
        active += [d]

if tmp_out:
    with open(f"{p}/active.json", "w") as f:
        json.dump(active, f, indent=4, sort_keys=True, ensure_ascii=False)



with open("{}/symbols.json".format(p), "r") as f:
    symbols = json.load(f)

data = dict()
for d in active:
    data[d["code"]] = dict(
        name=d["name"],
        alpha3=d["code"],
        code_num=d["code_num"],
        countries=d["country_codes"],
        minor=d["minor"],
        symbols=symbols.get(d["code"], []),
    )


with open("{}/data.json".format(p), "w") as f:
    json.dump(data, f, sort_keys=True, ensure_ascii=False, indent=4)
