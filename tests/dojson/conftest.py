# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import pytest
import os

import json
import jsonschema
from pkg_resources import resource_filename


def validator(schema):
    schema = resource_filename('rerodoc_data.jsonschemas', schema)

    schema_dir = os.path.dirname(os.path.abspath(schema))
    schema_name = os.path.basename(schema)

    with open(schema) as f:
        schema_json = json.load(f)

    # check if schema is valid
    jsonschema.Draft4Validator.check_schema(schema_json)

    resolver = jsonschema.RefResolver(
        'file://' + '/'.join(os.path.split(schema_dir)) + '/', schema_name
    )

    validator = jsonschema.Draft4Validator(
        schema_json, resolver=resolver, types=(('array', (list, tuple)), )
    )

    return validator


def marc2record(marc, record_type='book'):
    from rerodoc_data.dojson import book, audio
    if record_type == 'book':
        return book.do(marc)
    if record_type == 'audio':
        return audio.do(marc)


def marc2marc(marc, record_type='book'):
    from rerodoc_data.dojson import book, book2marc
    from rerodoc_data.dojson import audio, audio2marc
    if record_type == 'book':
        record = book.do(marc)
        return book2marc.do(record)
    if record_type == 'audio':
        record = audio.do(marc)
        return audio2marc.do(record)


def record2jsonld(record, context):
    from pyld import jsonld
    import json
    import rdflib_jsonld
    from rdflib import Graph
    import copy
    rec = copy.deepcopy(record)
    rec.update(context)
    compacted = jsonld.compact(rec, context)
    return jsonld.expand(compacted)


def get_demo_record(rec):
    """Get a record in Json format from a MarcXML."""

    from dojson.contrib.marc21.utils import create_record
    from rerodoc_data.dojson import book
    blob = create_record(rec)
    data = book.do(blob)
    return data


@pytest.fixture(scope='session')
def simple_book_record():
    """A sample book record."""
    return get_demo_record(file(os.path.join(os.path.dirname(__file__),
                                             "book_record.xml")).read())


@pytest.fixture(scope='session')
def book_schema():
    """Session-wide book schema."""
    from rerodoc_data.dojson.utils import get_schema
    return get_schema("book")


@pytest.fixture(scope='session')
def book_context():
    """Session-wide book context."""
    from rerodoc_data.dojson.utils import get_context
    return get_context("book")
