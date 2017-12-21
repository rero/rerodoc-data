from invenio_records_rest.serializers.json import JSONSerializer
from flask import json
from invenio_records_rest.serializers.schemas.json import RecordSchemaJSONV1


from marshmallow import Schema, fields


class HighlightRecordSchemaJSONV1(RecordSchemaJSONV1):
    """Schema for records v1 in JSON."""

    highlight = fields.Raw()

class HighlightJSONSerializer(JSONSerializer):
    """Marshmallow based JSON serializer for records.

    Note: This serializer is not suitable for serializing large number of
    records.
    """
    @staticmethod
    def preprocess_search_hit(pid, record_hit, links_factory=None):
        """Prepare a record hit from Elasticsearch for serialization."""
        links_factory = links_factory or (lambda x: dict())
        record = dict(
            pid=pid,
            metadata=record_hit['_source'],
            links=links_factory(pid),
            revision=record_hit['_version'],
            created=None,
            updated=None,
        )
        if record_hit.get('highlight'):
            record['highlight'] = record_hit.get('highlight')
        # Move created/updated attrs from source to object.
        for key in ['_created', '_updated']:
            if key in record['metadata']:
                record[key[1:]] = record['metadata'][key]
                del record['metadata'][key]
        return record

json_v1 = HighlightJSONSerializer(HighlightRecordSchemaJSONV1)

from invenio_records_rest.serializers.response import record_responsify, search_responsify
json_v1_search = search_responsify(json_v1, 'application/json')