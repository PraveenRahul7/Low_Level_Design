from abc import ABC, abstractmethod
from ..products.base import RequestParser, ResponseBuilder

class PayGateFactory(ABC):
    """
    Abstract Factory to produce request parsers and response builders for gateways.
    """

    @abstractmethod
    def create_request_parser(self) -> RequestParser:
        pass

    @abstractmethod
    def create_response_builder(self) -> ResponseBuilder:
        pass
