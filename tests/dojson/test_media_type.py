import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator

validator = validator('common/media_type-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('http://rdvocab.info/termList/RDAMediaType/1003')


def test_simple_from_marc():
    record = marc2record({
        '980__': {
            'a': 'BOOK'
        }
    })
    ref = 'http://rdvocab.info/termList/RDAMediaType/1003'
    assert record.get('media_type') == ref


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'media_type': 'http://rdvocab.info/termList/RDAMediaType/1003'
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://rdaregistry.info/Elements/u/mediaType': [{
            '@id': 'http://rdvocab.info/termList/RDAMediaType/1003'
        }]
    }]
