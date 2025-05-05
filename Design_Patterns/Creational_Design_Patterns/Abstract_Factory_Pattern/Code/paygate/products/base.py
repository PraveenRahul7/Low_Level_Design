from abc import ABC, abstractmethod

class RequestParser(ABC):
    """
    Abstract base class for request parsers used by payment gateways.
    """

    @abstractmethod
    def parse(self, data: dict) -> dict:
        """
        Parse raw request data into gateway-specific format.
        """
        pass

class ResponseBuilder(ABC):
    """
    Abstract base class for response builders used by payment gateways.
    """

    @abstractmethod
    def build(self, result: dict) -> dict:
        """
        Build response data from processing result.
        """
        pass
