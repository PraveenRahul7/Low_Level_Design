"""
DECOMPOSITION IN PYTHON
========================

Decomposition: Breaking down complex problems into smaller, manageable pieces.

Benefits:
- Easier to understand and maintain
- Enables code reuse
- Simplifies testing and debugging
- Allows parallel development
- Reduces complexity
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# PART 1: FUNCTIONAL DECOMPOSITION
# ============================================================================

# BAD: Monolithic function doing everything
def process_order_bad(order_data: dict) -> dict:
    """
    Anti-pattern: One large function doing multiple tasks.

    Problems:
    - Hard to understand
    - Difficult to test individual parts
    - Cannot reuse components
    - Hard to maintain
    """
    # Validate
    if not order_data.get('items'):
        return {'error': 'No items'}
    if order_data.get('quantity', 0) <= 0:
        return {'error': 'Invalid quantity'}

    # Calculate
    subtotal = 0
    for item in order_data['items']:
        subtotal += item['price'] * item['quantity']

    tax = subtotal * 0.08
    shipping = 10 if subtotal < 50 else 0
    total = subtotal + tax + shipping

    # Apply discount
    if order_data.get('coupon') == 'SAVE10':
        total *= 0.9

    # Format result
    result = {
        'subtotal': round(subtotal, 2),
        'tax': round(tax, 2),
        'shipping': round(shipping, 2),
        'total': round(total, 2),
        'order_id': f"ORD-{datetime.now().timestamp()}"
    }

    return result


# GOOD: Decomposed into smaller, focused functions
def validate_order(order_data: dict) -> Tuple[bool, str]:
    """
    Single responsibility: Validate order data.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not order_data.get('items'):
        return False, 'No items in order'

    for item in order_data['items']:
        if item.get('quantity', 0) <= 0:
            return False, 'Invalid quantity for item'
        if item.get('price', 0) < 0:
            return False, 'Invalid price for item'

    return True, ''


def calculate_subtotal(items: List[dict]) -> float:
    """
    Single responsibility: Calculate subtotal from items.

    Args:
        items: List of item dictionaries with 'price' and 'quantity'

    Returns:
        Subtotal amount
    """
    return sum(item['price'] * item['quantity'] for item in items)


def calculate_tax(subtotal: float, tax_rate: float = 0.08) -> float:
    """
    Single responsibility: Calculate tax amount.

    Args:
        subtotal: Order subtotal
        tax_rate: Tax rate (default 8%)

    Returns:
        Tax amount
    """
    return subtotal * tax_rate


def calculate_shipping(subtotal: float, free_shipping_threshold: float = 50) -> float:
    """
    Single responsibility: Determine shipping cost.

    Args:
        subtotal: Order subtotal
        free_shipping_threshold: Minimum for free shipping

    Returns:
        Shipping cost
    """
    return 0 if subtotal >= free_shipping_threshold else 10


def apply_discount(total: float, coupon_code: str) -> float:
    """
    Single responsibility: Apply discount coupon.

    Args:
        total: Current total
        coupon_code: Coupon code to apply

    Returns:
        Discounted total
    """
    discounts = {
        'SAVE10': 0.10,
        'SAVE20': 0.20,
        'SUMMER': 0.15
    }

    discount_rate = discounts.get(coupon_code, 0)
    return total * (1 - discount_rate)


def generate_order_id() -> str:
    """
    Single responsibility: Generate unique order ID.

    Returns:
        Unique order identifier
    """
    timestamp = int(datetime.now().timestamp() * 1000)
    return f"ORD-{timestamp}"


def process_order_good(order_data: dict) -> dict:
    """
    Well-decomposed function orchestrating smaller functions.

    Each sub-function has a single, clear responsibility.
    Easy to test, maintain, and extend.
    """
    # Validate
    is_valid, error_msg = validate_order(order_data)
    if not is_valid:
        return {'error': error_msg}

    # Calculate costs
    subtotal = calculate_subtotal(order_data['items'])
    tax = calculate_tax(subtotal)
    shipping = calculate_shipping(subtotal)
    total = subtotal + tax + shipping

    # Apply discounts
    if coupon := order_data.get('coupon'):
        total = apply_discount(total, coupon)

    # Return formatted result
    return {
        'order_id': generate_order_id(),
        'subtotal': round(subtotal, 2),
        'tax': round(tax, 2),
        'shipping': round(shipping, 2),
        'total': round(total, 2)
    }


# ============================================================================
# PART 2: CLASS-BASED DECOMPOSITION
# ============================================================================

@dataclass
class Item:
    """
    Decomposed data structure for an item.

    Encapsulates item-related data and behavior.
    """
    name: str
    price: float
    quantity: int

    def get_total(self) -> float:
        """Calculate total for this item."""
        return self.price * self.quantity

    def is_valid(self) -> bool:
        """Validate item data."""
        return self.price >= 0 and self.quantity > 0


class ShoppingCart:
    """
    Decomposed class handling cart operations.

    Separates cart logic from order processing.
    """

    def __init__(self):
        """Initialize empty cart."""
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add item to cart."""
        if item.is_valid():
            self.items.append(item)

    def remove_item(self, item_name: str) -> None:
        """Remove item from cart by name."""
        self.items = [item for item in self.items if item.name != item_name]

    def get_subtotal(self) -> float:
        """Calculate cart subtotal."""
        return sum(item.get_total() for item in self.items)

    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self.items) == 0


class TaxCalculator:
    """
    Decomposed class for tax calculations.

    Can be extended with different tax strategies.
    """

    def __init__(self, tax_rate: float = 0.08):
        """Initialize with tax rate."""
        self.tax_rate = tax_rate

    def calculate(self, amount: float) -> float:
        """Calculate tax on amount."""
        return amount * self.tax_rate


class ShippingCalculator:
    """
    Decomposed class for shipping calculations.

    Encapsulates shipping logic separately.
    """

    def __init__(self, base_cost: float = 10, free_threshold: float = 50):
        """Initialize shipping parameters."""
        self.base_cost = base_cost
        self.free_threshold = free_threshold

    def calculate(self, subtotal: float) -> float:
        """Calculate shipping cost."""
        return 0 if subtotal >= self.free_threshold else self.base_cost


class CouponManager:
    """
    Decomposed class for coupon management.

    Separates discount logic into its own component.
    """

    def __init__(self):
        """Initialize coupon database."""
        self.coupons = {
            'SAVE10': 0.10,
            'SAVE20': 0.20,
            'SUMMER': 0.15
        }

    def is_valid(self, code: str) -> bool:
        """Check if coupon code is valid."""
        return code in self.coupons

    def get_discount_rate(self, code: str) -> float:
        """Get discount rate for coupon."""
        return self.coupons.get(code, 0)

    def apply(self, amount: float, code: str) -> float:
        """Apply coupon to amount."""
        discount_rate = self.get_discount_rate(code)
        return amount * (1 - discount_rate)


class OrderProcessor:
    """
    Main class orchestrating decomposed components.

    Uses composition to combine smaller, focused classes.
    Each dependency can be easily tested or replaced.
    """

    def __init__(
            self,
            tax_calculator: TaxCalculator = None,
            shipping_calculator: ShippingCalculator = None,
            coupon_manager: CouponManager = None
    ):
        """
        Initialize with injected dependencies.

        Dependency injection makes components pluggable and testable.
        """
        self.tax_calculator = tax_calculator or TaxCalculator()
        self.shipping_calculator = shipping_calculator or ShippingCalculator()
        self.coupon_manager = coupon_manager or CouponManager()

    def process(self, cart: ShoppingCart, coupon_code: str = None) -> dict:
        """
        Process order using decomposed components.

        Each calculation is delegated to specialized objects.
        """
        if cart.is_empty():
            return {'error': 'Cart is empty'}

        # Calculate costs using specialized components
        subtotal = cart.get_subtotal()
        tax = self.tax_calculator.calculate(subtotal)
        shipping = self.shipping_calculator.calculate(subtotal)
        total = subtotal + tax + shipping

        # Apply coupon if valid
        if coupon_code and self.coupon_manager.is_valid(coupon_code):
            total = self.coupon_manager.apply(total, coupon_code)

        return {
            'order_id': generate_order_id(),
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'shipping': round(shipping, 2),
            'total': round(total, 2)
        }


# ============================================================================
# PART 3: ALGORITHMIC DECOMPOSITION (DIVIDE AND CONQUER)
# ============================================================================

def merge_sort(arr: List[int]) -> List[int]:
    """
    Classic example of algorithmic decomposition.

    Breaks problem into smaller subproblems recursively.
    Demonstrates divide-and-conquer strategy.
    """
    # Base case: array of size 1 or 0 is already sorted
    if len(arr) <= 1:
        return arr

    # Divide: split array in half
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # Conquer: recursively sort each half
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)

    # Combine: merge sorted halves
    return merge(left_sorted, right_sorted)


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Helper function: merges two sorted arrays.

    Separated from main function for clarity and reusability.
    """
    result = []
    i = j = 0

    # Merge while both arrays have elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ============================================================================
# PART 4: LAYERED DECOMPOSITION (SEPARATION OF CONCERNS)
# ============================================================================

# Data Layer
class DataStore:
    """
    Bottom layer: Data storage and retrieval.

    Handles all database/storage operations.
    """

    def __init__(self):
        """Simulate database with dictionary."""
        self._users = {}

    def save_user(self, user_id: str, user_data: dict) -> bool:
        """Save user to storage."""
        self._users[user_id] = user_data
        return True

    def get_user(self, user_id: str) -> dict:
        """Retrieve user from storage."""
        return self._users.get(user_id)

    def user_exists(self, email: str) -> bool:
        """Check if user exists by email."""
        return any(u.get('email') == email for u in self._users.values())


# Business Logic Layer
class UserService:
    """
    Middle layer: Business logic and validation.

    Contains rules and processing logic.
    """

    def __init__(self, data_store: DataStore):
        """Initialize with data store dependency."""
        self.data_store = data_store

    def register_user(self, email: str, password: str, name: str) -> Tuple[bool, str]:
        """
        Register new user with validation.

        Returns:
            Tuple of (success, message)
        """
        # Validation
        if not self._is_valid_email(email):
            return False, "Invalid email format"

        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if self.data_store.user_exists(email):
            return False, "User already exists"

        # Create user
        user_id = self._generate_user_id(email)
        user_data = {
            'email': email,
            'password': self._hash_password(password),
            'name': name,
            'created_at': datetime.now().isoformat()
        }

        # Save
        self.data_store.save_user(user_id, user_data)
        return True, f"User {email} registered successfully"

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        return '@' in email and '.' in email

    def _hash_password(self, password: str) -> str:
        """Hash password (simplified)."""
        return f"hashed_{password}"

    def _generate_user_id(self, email: str) -> str:
        """Generate unique user ID."""
        return f"user_{hash(email) % 10000}"


# Presentation Layer
class UserController:
    """
    Top layer: User interface and input handling.

    Coordinates between user input and business logic.
    """

    def __init__(self, user_service: UserService):
        """Initialize with user service dependency."""
        self.user_service = user_service

    def handle_registration(self, form_data: dict) -> dict:
        """
        Handle user registration request.

        Extracts data, calls service, formats response.
        """
        email = form_data.get('email', '').strip()
        password = form_data.get('password', '')
        name = form_data.get('name', '').strip()

        # Delegate to service layer
        success, message = self.user_service.register_user(email, password, name)

        # Format response for presentation
        return {
            'success': success,
            'message': message,
            'status_code': 200 if success else 400
        }


# ============================================================================
# PART 5: MODULAR DECOMPOSITION
# ============================================================================

class ReportGenerator:
    """
    Example of modular decomposition.

    Each method is a self-contained module that can be
    independently developed, tested, and maintained.
    """

    def generate_sales_report(self, sales_data: List[dict]) -> str:
        """
        Generate complete sales report.

        Orchestrates multiple specialized modules.
        """
        header = self._generate_header()
        summary = self._generate_summary(sales_data)
        details = self._generate_details(sales_data)
        footer = self._generate_footer()

        return f"{header}\n{summary}\n{details}\n{footer}"

    def _generate_header(self) -> str:
        """Module: Generate report header."""
        return "=" * 50 + "\n" + "SALES REPORT".center(50) + "\n" + "=" * 50

    def _generate_summary(self, sales_data: List[dict]) -> str:
        """Module: Generate summary statistics."""
        total_sales = sum(s['amount'] for s in sales_data)
        avg_sale = total_sales / len(sales_data) if sales_data else 0

        return f"\nTotal Sales: ${total_sales:.2f}\nAverage Sale: ${avg_sale:.2f}\n"

    def _generate_details(self, sales_data: List[dict]) -> str:
        """Module: Generate detailed transactions."""
        details = "\nDetailed Transactions:\n" + "-" * 50 + "\n"
        for sale in sales_data:
            details += f"{sale['date']}: ${sale['amount']:.2f} - {sale['item']}\n"
        return details

    def _generate_footer(self) -> str:
        """Module: Generate report footer."""
        return "=" * 50 + f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=== FUNCTIONAL DECOMPOSITION DEMO ===")
    order = {
        'items': [
            {'name': 'Book', 'price': 20, 'quantity': 2},
            {'name': 'Pen', 'price': 5, 'quantity': 3}
        ],
        'coupon': 'SAVE10'
    }
    result = process_order_good(order)
    print(f"Order Total: ${result['total']}")

    print("\n=== CLASS-BASED DECOMPOSITION DEMO ===")
    cart = ShoppingCart()
    cart.add_item(Item("Laptop", 999.99, 1))
    cart.add_item(Item("Mouse", 29.99, 2))

    processor = OrderProcessor()
    order_result = processor.process(cart, "SAVE20")
    print(f"Order ID: {order_result['order_id']}")
    print(f"Total: ${order_result['total']}")

    print("\n=== ALGORITHMIC DECOMPOSITION DEMO ===")
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = merge_sort(unsorted)
    print(f"Sorted: {sorted_arr}")

    print("\n=== LAYERED DECOMPOSITION DEMO ===")
    data_store = DataStore()
    user_service = UserService(data_store)
    controller = UserController(user_service)

    response = controller.handle_registration({
        'email': 'john@example.com',
        'password': 'securepass123',
        'name': 'John Doe'
    })
    print(f"Registration: {response['message']}")

    print("\n=== MODULAR DECOMPOSITION DEMO ===")
    sales = [
        {'date': '2024-01-15', 'amount': 150.00, 'item': 'Widget A'},
        {'date': '2024-01-16', 'amount': 200.00, 'item': 'Widget B'}
    ]
    generator = ReportGenerator()
    report = generator.generate_sales_report(sales)
    print(report)