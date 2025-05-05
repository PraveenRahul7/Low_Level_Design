from ..factories.base import PayGateFactory
from ..products.chase import ChaseRequestParser, ChaseResponseBuilder

class ChaseFactory(PayGateFactory):
    def create_request_parser(self):
        return ChaseRequestParser()

    def create_response_builder(self):
        return ChaseResponseBuilder()
