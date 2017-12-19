import pytest
from conftest import marc2record, marc2marc, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/subject-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'vocabulary': 'rero',
        'tag': '650_7',
        'content': 'Inventaires'
    }])

    with pytest.raises(ValidationError):
        validator.validate([{'vocabulary': 'invalid'}])

    with pytest.raises(ValidationError):
        validator.validate([{'tag': '245__'}])

    with pytest.raises(ValidationError):
        validator.validate([{'tag': '65_0_'}])


def test_from_marc():
    record = marc2record({
        '600__': [{
            '2': 'rero',
            '9': '650_7',
            'a': 'Inventaires'
        }]
    })
    assert record == {
        'subject': [{
            'vocabulary': 'rero',
            'tag': '650_7',
            'content': 'Inventaires'
        }]
    }


def test_mesh_from_marc():
    record = marc2record({
        '600__': [{
            '9': '650_2',
            'a': 'Inventaires'
        }]
    })
    assert record == {
        'subject': [{
            'vocabulary': 'mesh',
            'tag': '650_2',
            'content': 'Inventaires'
        }]
    }


def test_mesh_marc2marc():
    marc = {
        '600__': [{
            '9': '650_2',
            'a': 'Inventaires'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_lcsh_from_marc():
    record = marc2record({
        '600__': [{
            '9': '650__',
            'a': 'Inventaires'
        }]
    })
    assert record == {
        'subject': [{
            'vocabulary': 'lcsh',
            'tag': '650__',
            'content': 'Inventaires'
        }]
    }


def test_lcsh_marc2marc():
    marc = {
        '600__': [{
            '9': '650__',
            'a': 'Inventaires'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
