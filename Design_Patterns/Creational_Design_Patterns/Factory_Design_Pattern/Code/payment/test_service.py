import pytest
from unittest.mock import MagicMock
from service import PaymentService
from gateways.base import PaymentGatewayAdapter, GiftCardCapable


def test_make_payment():
    mock_gateway = MagicMock(spec=PaymentGatewayAdapter)
    mock_gateway.charge.return_value = {"status": "success", "transaction_id": "mock_txn"}

    service = PaymentService(mock_gateway)
    result = service.make_payment(100.0, "USD", {"card": "4242"})

    assert result["status"] == "success"
    mock_gateway.charge.assert_called_once()


def test_process_gift_card_supported():
    mock_gateway = MagicMock(spec=GiftCardCapable)
    mock_gateway.process_gift_card.return_value = {"status": "applied"}

    service = PaymentService(mock_gateway)
    result = service.process_gift_card_payment("GC123", 50.0)

    assert result["status"] == "applied"
    mock_gateway.process_gift_card.assert_called_once()


def test_process_gift_card_not_supported():
    mock_gateway = MagicMock(spec=PaymentGatewayAdapter)
    service = PaymentService(mock_gateway)

    with pytest.raises(NotImplementedError):
        service.process_gift_card_payment("GC999", 25.0)
