from iso4217parse import parse

import pytest


@pytest.mark.parametrize('sample, expect', [
    ('Eure Pizza kostet 5$', 'USD'),
    ('Eure Pizza kostet 5 $', 'USD'),
    ('Eure Pizza kostet 5 $ ', 'USD'),
    ('Eure Pizza kostet 5$ ', 'USD'),
    ('Eure Pizza kostet $5', 'USD'),
    ('Eure Pizza kostet $ 5', 'USD'),
    ('Eure Pizza kostet$5', 'USD'),
    ('Eure Pizza kostet $5 ', 'USD'),
    ('man.EUR', 'EUR'),
    ('man. 5 EUR', 'EUR'),
    ('man. 5 EUR ', 'EUR'),
    ('man. EUR5', 'EUR'),
    ('man.EUR5', 'EUR'),
])
def test_samples(sample, expect):
    res = parse(sample)
    assert res
    assert expect in {r.alpha3 for r in res}
