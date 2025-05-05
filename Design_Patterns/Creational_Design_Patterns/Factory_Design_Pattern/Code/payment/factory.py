from gateways.stripe import StripeAdapter
from gateways.paypal import PayPalAdapter
from gateways.base import PaymentGatewayAdapter

class PaymentGatewayFactory:
    @staticmethod
    def get_gateway(provider_name: str) -> PaymentGatewayAdapter:
        if provider_name == "stripe":
            return StripeAdapter()
        elif provider_name == "paypal":
            return PayPalAdapter()
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
