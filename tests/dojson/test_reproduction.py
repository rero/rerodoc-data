import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator

validator = validator('common/reproduction-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'type': 'Type',
        'location': 'Location',
        'agency': 'Agency',
        'date': '2015.',
        'full': 'Type Location Agency 2015.'
    })


def test_from_marc():
    record = marc2record({
        '533__': {
            'a': 'Type',
            'b': 'Location',
            'c': 'Agency',
            'd': '2015.'
        }
    })
    assert record.get('reproduction') == {
        'type': 'Type',
        'location': 'Location',
        'agency': 'Agency',
        'date': '2015.',
        'full': 'Type Location Agency 2015.'
    }


def test_marc2marc():
    marc = {
        '533__': {
            'a': 'Type',
            'b': 'Location',
            'c': 'Agency',
            'd': '2015.'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted
