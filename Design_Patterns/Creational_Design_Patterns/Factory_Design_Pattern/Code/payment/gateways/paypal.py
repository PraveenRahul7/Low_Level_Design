from .base import PaymentGatewayAdapter

class PayPalAdapter(PaymentGatewayAdapter):
    def charge(self, amount, currency, card_info):
        return {"status": "success", "gateway": "paypal", "transaction_id": "txn_456"}

    def refund(self, transaction_id, amount):
        return {"status": "refunded", "transaction_id": transaction_id}
