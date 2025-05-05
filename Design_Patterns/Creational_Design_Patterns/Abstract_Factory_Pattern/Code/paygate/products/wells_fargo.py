from base import RequestParser, ResponseBuilder

class WellsFargoRequestParser(RequestParser):
    def parse(self, data: dict) -> dict:
        return {"wells_parsed": data}

class WellsFargoResponseBuilder(ResponseBuilder):
    def build(self, result: dict) -> dict:
        return {"wells_response": result}
