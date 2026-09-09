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
  `parse("Chinese yuan")` now returns `[CNY, CNH, CNT]` rather than `[CNY]`. Matches are
  ordered by ISO numeric code, so officially assigned currencies come first and
  `parse(...)[0]` still yields `CNY`.

### Changed

- `Currency` is now a documented, fully annotated `NamedTuple`. `code_num` is typed
  `int | None`, reflecting that unofficial currencies have no ISO numeric code.
- Python 3.13 and 3.14 added to the test matrix.
- Internals modernized: PEP 604 type hints, `importlib.resources.files()`, and `pathlib`
  throughout `gen_data.py`.

Older releases: https://github.com/tammoippen/iso4217parse/releases
