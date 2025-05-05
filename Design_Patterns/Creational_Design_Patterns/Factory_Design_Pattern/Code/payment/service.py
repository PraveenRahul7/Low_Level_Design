from gateways.base import PaymentGatewayAdapter, GiftCardCapable

class PaymentService:
    def __init__(self, gateway: PaymentGatewayAdapter):
        self.gateway = gateway

    def make_payment(self, amount, currency, card_info):
        return self.gateway.charge(amount, currency, card_info)

    def process_gift_card_payment(self, gift_card_code, amount):
        if isinstance(self.gateway, GiftCardCapable):
            return self.gateway.process_gift_card(gift_card_code, amount)
        raise NotImplementedError("Gift card processing not supported")
