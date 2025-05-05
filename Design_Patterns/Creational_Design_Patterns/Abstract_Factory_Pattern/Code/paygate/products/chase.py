from base import RequestParser, ResponseBuilder

class ChaseRequestParser(RequestParser):
    def parse(self, data: dict) -> dict:
        return {"chase_parsed": data}

class ChaseResponseBuilder(ResponseBuilder):
    def build(self, result: dict) -> dict:
        return {"chase_response": result}
