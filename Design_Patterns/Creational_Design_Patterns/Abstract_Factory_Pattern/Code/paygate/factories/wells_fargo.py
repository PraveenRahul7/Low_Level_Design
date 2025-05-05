from ..factories.base import PayGateFactory
from ..products.wells_fargo import WellsFargoRequestParser, WellsFargoResponseBuilder

class WellsFargoFactory(PayGateFactory):
    def create_request_parser(self):
        return WellsFargoRequestParser()

    def create_response_builder(self):
        return WellsFargoResponseBuilder()
