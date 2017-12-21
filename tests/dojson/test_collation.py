import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/collation-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'pages': '100 p.',
        'other': 'ill.',
        'dimension': '25 x 30 cm',
        'full': '100 p. ill. 25 x 30 cm'
    })


def test_from_marc():
    record = marc2record({
        '300__': {
            'a': '100 p.',
            'b': 'ill.',
            'c': '25 x 30 cm'
        }
    })
    assert record.get('collation') == {
        'pages': '100 p.',
        'other': 'ill.',
        'dimension': '25 x 30 cm',
        'full': '100 p. ill. 25 x 30 cm'
    }


def test_marc2marc():
    marc = {
        '300__': {
            'a': '100 p.',
            'b': 'ill.',
            'c': '25 x 30 cm'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'collation': {
            'pages': '100 p.',
            'other': 'ill.',
            'dimension': '25 x 30 cm',
            'full': '100 p. ill. 25 x 30 cm'
        }
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/elements/1.1/format': [{
            '@value': '100 p. ill. 25 x 30 cm'
        }]
    }]
