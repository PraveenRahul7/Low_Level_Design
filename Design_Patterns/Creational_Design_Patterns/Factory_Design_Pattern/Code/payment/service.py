from gateways.base import PaymentGatewayAdapter, GiftCardCapable
from factory import PaymentGatewayFactory

class PaymentService:
    def __init__(self, gateway: PaymentGatewayAdapter):
        self.gateway = gateway

    def make_payment(self, amount, currency, card_info):
        return self.gateway.charge(amount, currency, card_info)

    def process_gift_card_payment(self, gift_card_code, amount):
        if isinstance(self.gateway, GiftCardCapable):
            return self.gateway.process_gift_card(gift_card_code, amount)
        raise NotImplementedError("Gift card processing not supported")

if __name__ == '__main__':
    gateway_type = PaymentGatewayFactory.get_gateway("stripe")
    print(gateway_type.__dir__())
    service = PaymentService(gateway_type)
    gift_card_status = service.process_gift_card_payment("GC123", 50.0)
    print(gift_card_status)
    result = service.make_payment(100.0, "USD", {"card": "4242"})
    print(result)
