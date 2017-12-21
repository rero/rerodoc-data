from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/submission_number-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('20151116123706-NI')


def test_from_marc():
    record = marc2record({
        '990__': {'a': '20151116123706-NI'}
    })
    assert record.get('submission_number') == '20151116123706-NI'


def test_marc2marc():
    marc = {'990__': {'a': '20151116123706-NI'}}
    converted = marc2marc(marc)
    assert marc == converted
