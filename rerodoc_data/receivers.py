# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""Signals connections for RERO DOC."""

from celery import shared_task
from dojson.contrib.marc21.utils import create_record
from flask import current_app
from invenio_jsonschemas import current_jsonschemas as jsonschemas

from rerodoc_data.dojson import book

from .tasks import create_records


def publish_harvested_records(sender=None, records=[], *args, **kwargs):
    """Create, index the harvested records."""
    converted_records = []
    schema = current_app.config.get('RERODOC_DATA_OAI_JSONSCHEMA')
    schema_url = jsonschemas.path_to_url(schema)
    for record in records:
        identifier = record.header.identifier
        deleted = record.deleted
        rec = create_record(record.xml)
        rec = book.do(rec)
        rec['$schema'] = schema_url
        converted_records.append(rec)
    create_records(converted_records)
