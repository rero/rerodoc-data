import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/other_title-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'maintitle': 'Other Title',
        'lang': 'en',
        'full': 'Other Title'
    })
    with pytest.raises(ValidationError):
        validator.validate({'other_title': {'lang': 'eng'}})


def test_from_marc():
    record = marc2record({
        '246__': {
            'a': 'Other Title',
            '9': 'eng'
        }
    })
    assert record == {
        'other_title': {
            'maintitle': 'Other Title',
            'lang': 'en',
            'full': 'Other Title'
        }
    }


def test_marc2marc():
    marc = {
        '246__': {
            'a': 'Other Title',
            '9': 'eng'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'other_title': {
            'maintitle': 'Other Title',
            'lang': 'en',
            'full': 'Other Title'
        }
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/terms/alternative': [{
            '@value': 'Other Title',
            '@language': 'en'
        }]
    }]
    assert converted == jsonld
