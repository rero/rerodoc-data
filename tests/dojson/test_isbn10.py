import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('book/isbn10-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('2-88147-009-2')

    with pytest.raises(ValidationError):
        validator.validate('9782882250209')


def test_from_marc():
    record = marc2record({
        '020__': {
            'a': '2-88147-009-2'
        }
    })
    assert record.get('isbn10') == '2-88147-009-2'


def test_marc2marc():
    marc = {'020__': {'a': '2-88147-009-2'}}
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'isbn10': '2-88147-009-2'
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/ontology/bibo/isbn10': [{
            '@value': '2-88147-009-2'
        }]
    }]
