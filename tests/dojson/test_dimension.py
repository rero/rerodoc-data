import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/dimension-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'width': 150,
        'height': 200
    })


def test_from_marc():
    record = marc2record({
        '300__': {
            'c': '150 x 200 cm'
        }
    })
    assert record.get('dimension') == {
        'width': 150,
        'height': 200
    }


def test_simple_from_marc():
    record = marc2record({
        '300__': {'c': '25 cm'}
    })
    assert record.get("dimension") == {"width": 25}


def test_invalid_from_marc():
    record = marc2record({
        '300__': {'c': '25 cn'}
    })
    assert record.get("dimension", None) is None
