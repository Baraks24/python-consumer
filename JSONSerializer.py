import json
from bson.objectid import ObjectId
import uuid
from datetime import date, datetime
from decimal import Decimal

string_types = str, bytes

class JSONSerializer(json.JSONEncoder):
    mimetype = 'application/json'

    def default(self, data):
        if isinstance(data, (date, datetime)):
            return data.isoformat()
        elif isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, uuid.UUID):
            return str(data)
        elif isinstance(data, ObjectId):
            return str(data)
        raise TypeError("Unable to serialize %r (type: %s)" % (data, type(data)))

    def loads(self, s):
        try:
            return json.loads(s)
        except (ValueError, TypeError) as e:
            raise SerializationError(s, e)

    def dumps(self, data):
        # don't serialize strings
        if isinstance(data, string_types):
            return data

        try:
            return json.dumps(
                data,
                default=self.default,
                ensure_ascii=False,
                separators=(',', ':'),
            )
        except (ValueError, TypeError) as e:
            raise SerializationError(data, e)