from abc import ABC, abstractmethod

class PaymentGatewayAdapter(ABC):
    @abstractmethod
    def charge(self, amount, currency, card_info):
        pass

    @abstractmethod
    def refund(self, transaction_id, amount):
        pass


class GiftCardCapable(ABC):
    @abstractmethod
    def process_gift_card(self, gift_card_code, amount):
        pass
