import orjson


class JSONParserMixin:
    json_parser = orjson

    def parse(self, data):
        parser = self.get_json_parser()
        return parser.loads(data)

    def dumps(self, data) -> str:
        parser = self.get_json_parser()
        return parser.dumps(data).decode()

    def get_json_parser(self):
        return self.json_parser
