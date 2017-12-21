import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/document_type-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'main': 'book',
        'sub': 'book_proceed'
    })

    with pytest.raises(ValidationError):
            validator.validate({'main': 'foo', 'sub': 'book_proceed'})

    with pytest.raises(ValidationError):
            validator.validate({'main': 'foo', 'sub': 'book_proceed'})


def test_from_marc():
    record = marc2record({
        '980__': {'a': 'BOOK', 'f': 'BOOK_PROCEED'}
    })
    assert record.get('document_type') == {
        'main': 'book',
        'sub': 'book_proceed'
    }


def test_marc2marc():
    marc = {
        '919__': {
            'a': 'HES-SO Valais',
            'b': 'Sion',
            'd': 'doc.support@rero.ch'
        },
        '980__': {
            'b': 'HEVS_',
            'a': 'BOOK',
            'f': 'BOOK_PROCEED'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted
