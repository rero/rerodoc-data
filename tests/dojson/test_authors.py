import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/authors-0.0.1.json')
assert validator


def test_validate_record():
    record = [{
        'name': 'LastName, FirstName',
        'name': 'LastName, FirstName',
        'date': '1971-',
        'role': 'Dir.',
        'affiliation': 'Affiliation',
        'full': 'LastName, FirstName 1971-',
        'orcid': 'http://orcid.org/0000-0001-8368-5460'
    }]
    validator.validate(record)
    with pytest.raises(ValidationError):
        validator.validate([{'role': 'foo'}])
    with pytest.raises(ValidationError):
        validator.validate([{'orcid': '0000-0001-8368-5460'}])


def test_first_author_from_marc():
    record = marc2record({
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'e': 'Dir.',
            'u': 'Affiliation'
        }
    })
    assert record == {
        'authors': [{
            'name': 'LastName, FirstName',
            'date': '1971-',
            'role': 'Dir.',
            'affiliation': 'Affiliation',
            'full': 'LastName, FirstName 1971-'
        }]
    }


def test_first_author_marc2marc():
    marc = {
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'e': 'Dir.',
            'u': 'Affiliation'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_multiple_authors_from_marc():
    record = marc2record({
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'u': 'Affiliation'
        },
        '700__': [{
            'a': 'LastName2, FirstName2',
            'd': '1972-',
            'e': 'Dir.',
            'u': 'Affiliation2'
        }, {
            'a': 'LastName3, FirstName3',
            'd': '1974-',
            'e': 'Codir.',
            'u': 'Affiliation'
        }]
    })
    assert record == {
        'authors': [{
            'name': 'LastName, FirstName',
            'date': '1971-',
            'affiliation': 'Affiliation',
            'full': 'LastName, FirstName 1971-'
        }, {
            'name': 'LastName2, FirstName2',
            'date': '1972-',
            'role': 'Dir.',
            'affiliation': 'Affiliation2',
            'full': 'LastName2, FirstName2 1972-'
        }, {
            'name': 'LastName3, FirstName3',
            'date': '1974-',
            'affiliation': 'Affiliation',
            'role': 'Codir.',
            'full': 'LastName3, FirstName3 1974-'
        }]
    }


def test_multiple_authors_marc2marc():
    marc = {
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'u': 'Affiliation'
        },
        '700__': [{
            'a': 'LastName2, FirstName2',
            'd': '1972-',
            'e': 'Dir.',
            'u': 'Affiliation2'
        }, {
            'a': 'LastName3, FirstName3',
            'd': '1974-',
            'e': 'Codir.',
            'u': 'Affiliation'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_first_author_jsonld(book_context):
    record = {
        'recid': '1234',
        'authors': [{
            'name': 'LastName, FirstName',
            'date': '1971-',
            'role': 'Dir.',
            'affilation': 'Affiliation',
            'full': 'LastName, FirstName 1971-'
        }]
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/elements/1.1/creator': [{
            '@value': 'LastName, FirstName 1971-'
        }]
    }]
    assert converted == jsonld
