# -*- coding: utf-8 -*-

import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/title-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'maintitle': 'Main Title',
        'subtitle': 'Subtitle',
        'lang': 'en',
        'full': 'Main Title Subtitle'
    })

    with pytest.raises(ValidationError):
        validator.validate({'title': {'lang': 'eng'}})


def test_from_marc():
    record = marc2record({
        '245__': {
            'a': 'Main Title',
            'b': "Subtitle",
            '9': 'eng'
        }
    })
    assert record == {
        'title': {
            'maintitle': 'Main Title',
            'subtitle': 'Subtitle',
            'lang': 'en',
            'full': 'Main Title Subtitle'
        }
    }


def test_from_marc_utf8():
    record = marc2record({
        '245__': {
            'a': 'Neuchâtel mon amour',
            'b': "Subtitle",
            '9': 'eng'
        }
    })
    assert record == {
        'title': {
            'maintitle': 'Neuchâtel mon amour',
            'subtitle': 'Subtitle',
            'lang': 'en',
            'full': 'Neuchâtel mon amour Subtitle'
        }
    }


def test_marc2marc():
    marc = {
        '245__': {
            'a': 'Main Title',
            'b': "Subtitle",
            '9': 'eng'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'title': {
            'maintitle': 'Main Title',
            'subtitle': 'Subtitle',
            'lang': 'en',
            'full': 'Main Title Subtitle'
        }
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/terms/title': [{
            '@value': 'Main Title Subtitle',
            '@language': 'en'
        }]
    }]
    assert converted == jsonld
