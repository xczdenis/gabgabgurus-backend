import codecs

import orjson
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from gabgabgurus.common.renderers import ORJSONRenderer


class ORJSONParser(JSONParser):
    """
    Parses JSON-serialized data by orjson parser.
    """

    media_type = "application/json"
    renderer_class = ORJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses JSON-serialized data using orjson parser.
        """
        parser_context = parser_context or {}
        encoding: str = parser_context.get("encoding", settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            return orjson.loads(decoded_stream.read())
        except ValueError as exc:
            raise ParseError("JSON parse error - %s" % str(exc))
