# -*- coding: utf-8 -*-
import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/publication-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'location': 'Location',
        'publisher': 'Publisher',
        'date': '2015-',
        'print_location': 'Print Location',
        'printer': 'Printer',
        'full': 'Location Publisher 2015- Print Location Printer'
    })


def test_from_marc():
    record = marc2record({
        '260__': {
            'a': 'Location',
            'b': 'Publisher',
            'c': '2015-',
            'e': 'Print Location',
            'f': 'Printer'
        }
    })
    assert record.get('publication') == {
        'location': 'Location',
        'publisher': 'Publisher',
        'date': '2015-',
        'print_location': 'Print Location',
        'printer': 'Printer',
        'full': 'Location Publisher 2015- Print Location Printer'
    }


def test_marc2marc():
    marc = {
        '260__': {
            'a': 'Location',
            'b': 'Publisher',
            'c': '2015-',
            'e': 'Print Location',
            'f': 'Printer'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_empty_260_marc2marc():
    marc = {
        "260__": {
            "a": "A Lausanne :",
            "c": "1744",
            "b": "chez Bousquet & Compagnie,",
            "e": "Lausanne"
        },
        "035__": {
            "a": "R004127217"
        },
        "990__": {
            "a": "20061123145722-ML"
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'publication': {
            'location': 'Location',
            'publisher': 'Publisher',
            'date': '2015-',
            'print_location': 'Print Location',
            'printer': 'Printer',
            'full': 'Location Publisher 2015- Print Location Printer'
        }
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://rdaregistry.info/Elements/u/publicationStatement': [{
            '@value': 'Location Publisher 2015- Print Location Printer'
        }]
    }]
