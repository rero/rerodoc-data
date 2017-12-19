import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/type-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate(['bibrec', 'book', 'text'])

    with pytest.raises(ValidationError):
        validator.validate(['book'])


def test_from_marc():
    record = marc2record({
        '980__': {'a': 'BOOK'}
    })
    assert record.get('type') == ['bibrec', 'book', 'text']


def test_marc2marc():
    marc = {
        '919__': {
            'a': 'HES-SO Valais',
            'b': 'Sion',
            'd': 'doc.support@rero.ch'
        },
        '980__': {
            'b': 'HEVS_',
            'a': 'BOOK'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'type': ['bibrec', 'book', 'text']
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        '@type': [
            'http://purl.org/dc/terms/BibliographicResource',
            'http://purl.org/ontology/bibo/Book',
            'http://purl.org/dc/dcmitype/Text',
        ]
    }]
    assert converted == jsonld
