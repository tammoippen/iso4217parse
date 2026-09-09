# Changelog

This project is pre-1.0: minor version bumps may contain breaking changes.

## 0.7.0

### Breaking

- **Python 3.11+ is required.** Support for 3.9 and 3.10 has been dropped — use
  [0.6.2](https://pypi.org/project/iso4217parse/0.6.2/) on those, or
  [0.5.1](https://pypi.org/project/iso4217parse/0.5.1/) on 2.7 and anything older than 3.9.
- **`parse()` raises `TypeError` instead of `ValueError`** when `v` is neither `str` nor `int`.
  `TypeError` is not a subclass of `ValueError`, so existing `except ValueError:` handlers
  need updating.
- **Currency-name lookups return every match instead of a single currency.**
  `parse("Renminbi")` now returns `[CNY, CNH, CNT, RMB]` rather than a single currency.
  Matches are ordered by ISO numeric code, so officially assigned currencies come first
  and `parse(...)[0]` still yields `CNY`.

### Data

Currency data regenerated from [Wikipedia's ISO 4217 page](https://en.wikipedia.org/w/index.php?title=ISO_4217&oldid=1373880935)
(189 → 192 entries). Renamed and removed currencies are breaking for name-based lookups:
`parse()` returns `[]` and `by_alpha3()` returns `None` for anything no longer listed.

**Removed**

| Code | Currency | Replaced by |
| --- | --- | --- |
| `ANG` | Netherlands Antillean guilder | `XCG` |
| `BGN` | Bulgarian lev | `EUR` |
| `CUC` | Cuban convertible peso | `CUP` |
| `HRK` | Croatian kuna | `EUR` |
| `MRO` | Mauritanian ouguiya | `MRU` |
| `SLL` | Sierra Leonean leone | `SLE` |
| `STD` | São Tomé and Príncipe dobra | `STN` |
| `VEF` | Venezuelan bolívar | `VES` |
| `ZWL` | Zimbabwean dollar | `ZWG` |

**Added** — `BDS` (Barbados dollar), `MRU`, `RMB` (Renminbi), `SLE`, `STG` (Sterling),
`STN`, `UYW` (Unidad previsional), `VED` (Venezuelan digital bolívar), `VES`,
`XAD` (Arab Accounting Dinar), `XCG` (Caribbean guilder), `ZWG` (Zimbabwe Gold).

**Renamed** — lookups by the old name no longer match:

- `CNY`, `CNH`, `CNT` — Chinese yuan → Renminbi
- `CHE` / `CHW` — WIR Euro / WIR Franc → WIR euro / WIR franc
- `CVE` — Cape Verde escudo → Cape Verdean escudo
- `IMP` — Isle of Man pound → Manx pound
- `NIS` — New Israeli Shekel → Israeli shekel
- `NTD` — New Taiwan Dollar → New Taiwan dollar
- `PEN` — Peruvian Sol → Peruvian sol
- `SEK` — Swedish krona/kronor → Swedish krona
- `UZS` — Uzbekistan som → Uzbekistani sum
- `XTS` — Code reserved for testing purposes → Code reserved for testing

**Country coverage** — `EUR` gained `BG` and `HR`; `ZAR` gained `LS`, `NA` and `SZ`;
`USD` dropped `BB`, `BM` and `HT`; `DZD` dropped `EH`.

### Changed

- `Currency` is now a documented, fully annotated `NamedTuple`. `code_num` is typed
  `int | None`, reflecting that unofficial currencies have no ISO numeric code.
- Python 3.13 and 3.14 added to the test matrix.
- Internals modernized: PEP 604 type hints, `importlib.resources.files()`, and `pathlib`
  throughout `gen_data.py`.

Older releases: https://github.com/tammoippen/iso4217parse/releases
