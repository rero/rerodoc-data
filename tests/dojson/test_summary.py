import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator

validator = validator('common/summary-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'lang': 'en',
        'content': 'Summary Line 1\n Line2'
    }])


def test_from_marc():
    record = marc2record({
        '520__': [{
            'a': 'Summary Line 1\n Line2',
            '9': 'eng'
        }]
    })
    assert record == {
        'summary': [{
            'lang': 'en',
            'content': 'Summary Line 1\n Line2'
        }]
    }


def test_marc2marc():
    marc = {
        '520__': [{
            'a': 'Summary Line 1\n Line2',
            '9': 'eng'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
