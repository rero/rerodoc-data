import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator

validator = validator('common/note-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('Note line 1\n Line 2')


def test_from_marc():
    record = marc2record({
        '500__': {'a': 'Note Line 1\n Line 2'}
    })
    assert record.get('note') == 'Note Line 1\n Line 2'


def test_marc2marc():
    marc = {'500__': {'a': 'Note line 1\n Line 2'}}
    converted = marc2marc(marc)
    assert marc == converted
