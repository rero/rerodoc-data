import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/document-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'name': 'file_name.pdf',
        'mime': 'application/pdf',
        'size': 1014,
        'url': 'http://doc.rero.ch/record/file_name.pdf',
        'order': 1,
        'label': 'Main file'
    }])
    with pytest.raises(ValidationError):
        validator.validate([{'url': 'http://rero.ch/files/test.pdf'}])


def test_from_marc():
    record = marc2record({
        '8564_': [{
            'f': 'file_name.pdf',
            'q': 'application/pdf',
            's': '1014',
            'u': 'http://doc.rero.ch/record/file_name.pdf',
            'y': 'order:1',
            'z': 'Main file'
        }]
    })
    assert record == {
        'document': [{
            'name': 'file_name.pdf',
            'mime': 'application/pdf',
            'size': 1014,
            'url': 'http://doc.rero.ch/record/file_name.pdf',
            'order': 1,
            'label': 'Main file'
        }]
    }


def test_marc2marc():
    marc = {
        '8564_': [{
            'f': 'file_name.pdf',
            'q': 'application/pdf',
            's': '1014',
            'u': 'http://doc.rero.ch/record/file_name.pdf',
            'y': 'order:1',
            'z': 'Main file'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_multiple_marc2marc():
    marc = {
        '8564_': [{
            'u': 'http://www.unige.ch/lettres/alman/digs/welcome.html',
            'y': '2007-11-25 23:47:43',
            'z': 'Homepage DiGS'
        }, {
            'f': 'digs_complete_abstract.pdf',
            'q': 'application/pdf',
            's': '6361',
            'u': 'http://doc.rero.ch/record/8488/files/' +
                 'digs_complete_abstract.pdf',
            'y': 'order:4',
            'z': u'R\xe9sum\xe9'
        }, {
            'f': 'digs_complete_postprint_v1.pdf',
            'q': 'application/pdf',
            's': '2086891',
            'u': 'http://doc.rero.ch/record/8488/files/' +
                 'digs_complete_postprint_v1.pdf',
            'y': 'order:1',
            'z': u'Texte int\xe9gral'
        }, {
            'f': 'digs_cover_front.pdf',
            'q': 'application/pdf',
            's': '2605703',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_front.pdf',
            'y': 'order:2',
            'z': 'Couverture avant'
        }, {
            'f': 'digs_cover_rear.pdf',
            'q': 'application/pdf',
            's': '192617',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_rear.pdf',
            'y': 'order:3',
            'z': u'Couverture arri\xe8re'
        }]
    }
    converted = marc2marc(marc)
    import json
    assert marc == converted
