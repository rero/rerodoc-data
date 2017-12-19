import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator

validator = validator('common/n_pages-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate(100)


def test_simple_from_marc():
    record = marc2record({
        '300__': {
            'a': '100'
        }
    })
    assert record.get('n_pages') == 100


def test_simple_fr_from_marc():
    record = marc2record({
        '300__': {'a': '25 p.'}
    })
    assert record.get("n_pages") == 25


def test_simple_ger_from_marc():
    record = marc2record({
        '300__': {'a': '230 s.'}
    })
    assert record.get("n_pages") == 230


def test_sheet_from_marc():
    record = marc2record({
        '300__': {'a': '230 f.'}
    })
    assert record.get("n_pages") == 230


def test_bad_pages():
    record = marc2record({
        '300__': {'a': 'A25 j. fjklad'}
    })
    assert record.get("n_pages") is None
