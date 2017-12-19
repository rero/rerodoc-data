import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator
from jsonschema import validate, ValidationError

validator = validator('common/publication_date-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'from': 2010,
        'to': 2011,
        'full': '2010-2011'
    })


def test_complete_from_marc():
    record = marc2record({
        '260__': {
            'c': '2015-2016'
        }
    })
    assert record.get('publication_date') == {
        'from': 2015,
        'to': 2016,
        'full': '2015-2016'
    }


def test_simple_from_marc():
    record = marc2record({
        '260__': {'c': '2015'}
    })
    assert record.get("publication_date") == {'to': 2015,
                                              'full': '2015',
                                              'from': 2015}


def test_from_only_from_marc():
    record = marc2record({
        '260__': {'c': '2015-'}
    })
    assert record.get("publication_date") == {'full': '2015-', 'from': 2015}


def test_complete_noisy_from_marc():
    record = marc2record({
        '260__': {'c': '2015 bla 2013 bla 2001'}
    })
    assert record.get("publication_date") == {'to': 2015,
                                              'full': '2001-2015',
                                              'from': 2001}


def test_invalid_from_marc():
    record = marc2record({
        '260__': {'c': '209 jfkad afje788'}
    })
    assert record.get("publication_date", None) is None


def test_missing_from_marc():
    record = marc2record({
        '260__': {'a': 'Name'}
    })
    assert record.get("publication_date", None) is None


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'publication_date': {
            'from': 2015,
            'to': 2016,
            'full': '2015-2016'
        }
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/terms/issued': [{
            '@value': '2015-2016'
        }]
    }]
