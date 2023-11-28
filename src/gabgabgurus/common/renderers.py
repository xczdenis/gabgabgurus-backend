import orjson
from loguru import logger
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from gabgabgurus.api.v1.fake.decorators import timer


@timer
def stringify_keys(d):
    """Преобразует все ключи словаря в строки."""
    if not isinstance(d, dict):
        return d
    return {str(k): stringify_keys(v) for k, v in d.items()}


class ORJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """

        def orjson_dumps(_data):
            return orjson.dumps(_data, default=serialize_arbitrary_type, option=orjson.OPT_INDENT_2)

        if data is None:
            return bytes()

        rendered_result = ""
        try:
            rendered_result = orjson_dumps(data)
        except TypeError as e:
            logger.error(e)
            rendered_result = orjson_dumps(stringify_keys(data))
        except Exception as e:
            logger.error(e)
            rendered_result = super().render(data, accepted_media_type=None, renderer_context=None)

        return rendered_result


def serialize_arbitrary_type(data):
    if isinstance(data, ReturnDict):
        return dict(data)

    if isinstance(data, ReturnList):
        items = []
        for item in data:
            items.append(dict(item))
        return list(items)
