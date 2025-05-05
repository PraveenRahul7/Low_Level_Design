
### ✅ **Payment Gateway Adapter Factory**

Imagine you're building an e-commerce system that supports **multiple payment gateways** (e.g., Stripe, PayPal, Wells Fargo). You want to handle each gateway differently, but expose a **common interface** to the rest of the system.

---

### 🎯 Goal:

* Encapsulate payment gateway logic.
* Support adding/removing gateways without changing business logic.
* Abstract away the gateway instantiation details.

---

### 🧱 Step-by-step Implementation (Python):

#### 1. **Define a common interface:**

```python
class PaymentGatewayAdapter:
    def charge(self, amount: float, currency: str, card_info: dict) -> dict:
        raise NotImplementedError

    def refund(self, transaction_id: str, amount: float) -> dict:
        raise NotImplementedError
```

---

#### 2. **Implement concrete adapters:**

```python
class StripeAdapter(PaymentGatewayAdapter):
    def charge(self, amount, currency, card_info):
        # Logic for Stripe API
        return {"status": "success", "transaction_id": "stripe_123"}

    def refund(self, transaction_id, amount):
        return {"status": "refunded", "transaction_id": transaction_id}


class PaypalAdapter(PaymentGatewayAdapter):
    def charge(self, amount, currency, card_info):
        # Logic for PayPal API
        return {"status": "success", "transaction_id": "paypal_abc"}

    def refund(self, transaction_id, amount):
        return {"status": "refunded", "transaction_id": transaction_id}
```

---

#### 3. **Create the factory:**

```python
class PaymentGatewayFactory:
    @staticmethod
    def get_gateway(provider_name: str) -> PaymentGatewayAdapter:
        if provider_name == "stripe":
            return StripeAdapter()
        elif provider_name == "paypal":
            return PaypalAdapter()
        else:
            raise ValueError(f"Unsupported payment provider: {provider_name}")
```

---

#### 4. **Usage in production code:**

```python
def process_payment(provider, amount, currency, card_info):
    gateway = PaymentGatewayFactory.get_gateway(provider)
    response = gateway.charge(amount, currency, card_info)
    return response

# Example usage
payment_info = process_payment(
    provider="stripe",
    amount=100.0,
    currency="USD",
    card_info={"number": "4242...", "cvv": "123"}
)
```

---

### 🔥 Real-World Benefits:

* You can easily **add new gateways** (e.g., `WellsFargoAdapter`) without changing existing logic.
* Useful for **multi-tenant systems** where each client uses a different payment provider.
* Fully testable via **mocking the factory** and adapter methods.
* Decouples **business logic** from **integration code**.




Awesome — here’s a concise, **production-level summary** of how to apply the **Factory Design Pattern** along with the **Interface Segregation Principle** (Option 3) in a real-world scenario like payment gateways.

---

## ✅ **Design Goal**

Build a flexible, extensible system to support multiple payment gateways (e.g., Stripe, PayPal, Wells Fargo), where:

* All gateways implement **core payment actions** (`charge`, `refund`).
* Some gateways implement **optional features** (e.g., `gift card processing`).
* You can easily add new gateways without touching existing logic.

---

## 🏗️ **Design Pattern Used**

### 1. **Factory Pattern**

Encapsulates creation logic for different gateways.

### 2. **Interface Segregation Principle (ISP)**

Split large interfaces into smaller, role-specific ones.

---

## 🧱 Code Structure

### ✅ **Core Interfaces**

```python
class PaymentGatewayAdapter:
    def charge(self, amount, currency, card_info):
        raise NotImplementedError

    def refund(self, transaction_id, amount):
        raise NotImplementedError
```

### ✅ **Optional Interface**

```python
class GiftCardCapable:
    def process_gift_card(self, gift_card_code, amount):
        raise NotImplementedError
```

---

### ✅ **Concrete Adapters**

```python
class StripeAdapter(PaymentGatewayAdapter, GiftCardCapable):
    def charge(self, amount, currency, card_info):
        # Stripe charge logic
        ...

    def refund(self, transaction_id, amount):
        # Stripe refund logic
        ...

    def process_gift_card(self, gift_card_code, amount):
        # Gift card logic for Stripe
        ...
```

```python
class PayPalAdapter(PaymentGatewayAdapter):
    def charge(self, amount, currency, card_info):
        # PayPal logic
        ...

    def refund(self, transaction_id, amount):
        ...
```

---

### ✅ **Factory**

```python
class PaymentGatewayFactory:
    @staticmethod
    def get_gateway(provider_name):
        if provider_name == "stripe":
            return StripeAdapter()
        elif provider_name == "paypal":
            return PayPalAdapter()
        else:
            raise ValueError("Unsupported gateway")
```

---

### ✅ **Client Code Example**

```python
gateway = PaymentGatewayFactory.get_gateway("stripe")

# Core functionality
gateway.charge(100.0, "USD", card_info={...})

# Optional functionality
if isinstance(gateway, GiftCardCapable):
    gateway.process_gift_card("GC123", 25.0)
else:
    print("Gift card not supported")
```

---

## 🚀 Benefits

| Feature                  | Benefit                                                  |
| ------------------------ | -------------------------------------------------------- |
| Factory Pattern          | Clean, extensible gateway creation                       |
| Interface Segregation    | Smaller, focused interfaces                              |
| Duck typing / isinstance | Runtime flexibility without breaking Liskov Principle    |
| Easy to test             | Each adapter and interface can be unit tested and mocked |

---


The **Factory Pattern** and **Interface Segregation** naturally lead into using **Dependency Injection (DI)** — especially in large, testable, modular systems.

---

## 🧩 What Is Dependency Injection?

**Dependency Injection** means you don’t create dependencies (like `StripeAdapter`) *inside* your classes — you **inject them from outside**, often through constructors, function arguments, or frameworks.

This allows:

* Decoupling classes from specific implementations
* Easier testing via mocking/stubbing
* More flexible and extensible code

---

## 🔗 How Factory + Interface Segregation Ties Into DI

### Scenario:

Let’s say you have a `PaymentService` that needs to process payments. It shouldn't care *which* gateway (Stripe, PayPal) is being used — just that it receives a gateway implementing the required interface.

---

### ✅ Without DI (hardcoded inside service):

```python
class PaymentService:
    def __init__(self):
        self.gateway = PaymentGatewayFactory.get_gateway("stripe")  # tightly coupled

    def make_payment(self, ...):
        self.gateway.charge(...)
```

### ❌ Problems:

* Hard to test (can’t swap gateway easily)
* Hard to change implementation
* Violates Inversion of Control (IoC)

---

### ✅ With DI (good practice):

```python
class PaymentService:
    def __init__(self, gateway: PaymentGatewayAdapter):
        self.gateway = gateway

    def make_payment(self, ...):
        self.gateway.charge(...)
```

Now you can inject at runtime:

```python
gateway = PaymentGatewayFactory.get_gateway("paypal")
service = PaymentService(gateway)
```

Or even mock in tests:

```python
mock_gateway = MagicMock(spec=PaymentGatewayAdapter)
mock_gateway.charge.return_value = {"status": "success"}

service = PaymentService(mock_gateway)
```

---

## 🎯 Summary of the Ties

| Concept                  | Role                                                                         |
| ------------------------ | ---------------------------------------------------------------------------- |
| **Factory Pattern**      | Creates the right implementation (`StripeAdapter`, `PayPalAdapter`)          |
| **Interfaces (ISP)**     | Define contracts like `PaymentGatewayAdapter`, `GiftCardCapable`             |
| **Dependency Injection** | Allows injecting these implementations into services (like `PaymentService`) |
| **Result**               | Flexible, decoupled, testable system architecture                            |

---

