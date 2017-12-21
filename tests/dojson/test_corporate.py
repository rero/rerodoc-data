import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/corporate-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate(["Corporate name"])


def test_from_marc():
    record = marc2record({
        '710__': {
            'a': 'Corporate name'
        }
    })
    assert record == {
        'corporate': ['Corporate name']
    }


def test_marc2marc():
    marc = {
        '710__': [{
            'a': 'Corporate name',
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'corporate': ['Corporate name', 'Corporate name2']
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/elements/1.1/contributor': [{
            '@value': 'Corporate name'
        }, {
            '@value': 'Corporate name2'
        }]
    }]
