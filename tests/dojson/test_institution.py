import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/institution-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'name': 'HES-SO Valais',
        'code': 'HEVS_',
        'locality': 'Sion'
    })
    with pytest.raises(ValidationError):
        validator.validate([{'code': 'TOTO'}])


def test_from_marc():
    record = marc2record({
        '919__': {
            'a': 'HES-SO Valais',
            'b': 'Sion'
        },
        '980__': {
            'b': 'HEVS_',
            'a': 'BOOK'
        }
    })
    assert record.get('institution') == {
        'name': 'HES-SO Valais',
        'code': 'HEVS_',
        'locality': 'Sion'
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
            'a': 'BOOK'
        }
    }

    converted = marc2marc(marc)
    assert marc == converted
