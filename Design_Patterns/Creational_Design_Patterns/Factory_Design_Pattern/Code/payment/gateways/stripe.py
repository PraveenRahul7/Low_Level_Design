from .base import PaymentGatewayAdapter, GiftCardCapable

class StripeAdapter(PaymentGatewayAdapter, GiftCardCapable):
    def charge(self, amount, currency, card_info):
        return {"status": "success", "gateway": "stripe", "transaction_id": "txn_123"}

    def refund(self, transaction_id, amount):
        return {"status": "refunded", "transaction_id": transaction_id}

    def process_gift_card(self, gift_card_code, amount):
        return {"status": "applied", "remaining_balance": 20.0}
