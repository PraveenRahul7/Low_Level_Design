"""
GENERALIZATION IN PYTHON
=========================

Generalization: The process of extracting common patterns and creating more
general, reusable solutions that work for multiple specific cases.

Opposite of Specialization: Moving from specific implementations to general ones.

Benefits:
- Reduces code duplication (DRY principle)
- Increases flexibility and adaptability
- Makes code more maintainable
- Enables polymorphism and abstraction
"""

from typing import List, Dict, Any, Callable, TypeVar, Generic, Protocol
from abc import ABC, abstractmethod
from functools import reduce
import operator


# ============================================================================
# PART 1: FUNCTION GENERALIZATION
# ============================================================================

# SPECIFIC: Separate functions for each calculation
def calculate_total_price(prices: List[float]) -> float:
    """Specific function for summing prices."""
    total = 0
    for price in prices:
        total += price
    return total


def calculate_total_quantity(quantities: List[int]) -> int:
    """Specific function for summing quantities."""
    total = 0
    for qty in quantities:
        total += qty
    return total


def calculate_average_rating(ratings: List[float]) -> float:
    """Specific function for averaging ratings."""
    total = 0
    for rating in ratings:
        total += rating
    return total / len(ratings) if ratings else 0


# GENERAL: Single generalized function
def aggregate(items: List[Any], operation: Callable, initial: Any = None) -> Any:
    """
    Generalized aggregation function.

    Works for any type of data and any aggregation operation.

    Args:
        items: List of items to aggregate
        operation: Function that combines two values
        initial: Initial value for aggregation

    Returns:
        Aggregated result
    """
    if not items:
        return initial

    result = initial if initial is not None else items[0]
    start_idx = 0 if initial is not None else 1

    for item in items[start_idx:]:
        result = operation(result, item)

    return result


# Using the generalized function
def sum_values(values: List[float]) -> float:
    """Sum using generalized function."""
    return aggregate(values, operator.add, 0)


def multiply_values(values: List[float]) -> float:
    """Product using generalized function."""
    return aggregate(values, operator.mul, 1)


def find_maximum(values: List[float]) -> float:
    """Maximum using generalized function."""
    return aggregate(values, max)


# ============================================================================
# PART 2: CLASS HIERARCHY GENERALIZATION
# ============================================================================

# SPECIFIC: Separate classes for each shape
class CircleSpecific:
    """Specific implementation for circles."""

    def __init__(self, radius: float):
        self.radius = radius

    def calculate_area(self) -> float:
        return 3.14159 * self.radius ** 2

    def calculate_perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class RectangleSpecific:
    """Specific implementation for rectangles."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def calculate_area(self) -> float:
        return self.width * self.height

    def calculate_perimeter(self) -> float:
        return 2 * (self.width + self.height)


# GENERAL: Abstract base class with common interface
class Shape(ABC):
    """
    Generalized Shape class.

    Defines common interface for all shapes through abstraction.
    Specific shapes inherit and implement specific behavior.
    """

    @abstractmethod
    def area(self) -> float:
        """Calculate area - implemented by subclasses."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter - implemented by subclasses."""
        pass

    def describe(self) -> str:
        """
        Generalized method working for all shapes.

        Uses polymorphism - calls specific implementations
        through the common interface.
        """
        return f"{self.__class__.__name__}: Area={self.area():.2f}, Perimeter={self.perimeter():.2f}"


class Circle(Shape):
    """Specific circle implementing general interface."""

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    """Specific rectangle implementing general interface."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Another specific shape - fits the general pattern."""

    def __init__(self, base: float, height: float, side1: float, side2: float):
        self.base = base
        self.height = height
        self.side1 = side1
        self.side2 = side2

    def area(self) -> float:
        return 0.5 * self.base * self.height

    def perimeter(self) -> float:
        return self.base + self.side1 + self.side2


def calculate_total_area(shapes: List[Shape]) -> float:
    """
    Generalized function working with any shape.

    Thanks to polymorphism, works with Circle, Rectangle, Triangle,
    or any future shape that implements the Shape interface.
    """
    return sum(shape.area() for shape in shapes)


# ============================================================================
# PART 3: GENERIC TYPES (TYPE PARAMETERS)
# ============================================================================

T = TypeVar('T')  # Type variable for generics


class Stack(Generic[T]):
    """
    Generic Stack that works with any type.

    Instead of creating IntStack, StringStack, etc.,
    we create one generalized Stack[T].
    """

    def __init__(self):
        """Initialize empty stack."""
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """
        Push item onto stack.

        Type T is determined when Stack is instantiated.
        """
        self._items.append(item)

    def pop(self) -> T:
        """
        Pop item from stack.

        Returns type T, maintaining type safety.
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """Peek at top item without removing."""
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Get stack size."""
        return len(self._items)


# Generic function
def find_first(items: List[T], predicate: Callable[[T], bool]) -> T | None:
    """
    Generalized search function.

    Works with any type T and any search condition.

    Args:
        items: List of any type
        predicate: Function that returns True for desired item

    Returns:
        First matching item or None
    """
    for item in items:
        if predicate(item):
            return item
    return None


# ============================================================================
# PART 4: STRATEGY PATTERN - GENERALIZED BEHAVIOR
# ============================================================================

class PaymentStrategy(ABC):
    """
    Generalized payment interface.

    Allows different payment methods to be used interchangeably.
    """

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process payment - implemented by specific strategies."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate payment method."""
        pass


class CreditCardPayment(PaymentStrategy):
    """Specific strategy: Credit card payment."""

    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} with credit card ending in {self.card_number[-4:]}"

    def validate(self) -> bool:
        return len(self.card_number) == 16 and len(self.cvv) == 3


class PayPalPayment(PaymentStrategy):
    """Specific strategy: PayPal payment."""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via PayPal account {self.email}"

    def validate(self) -> bool:
        return '@' in self.email


class CryptoPayment(PaymentStrategy):
    """Specific strategy: Cryptocurrency payment."""

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via crypto wallet {self.wallet_address[:10]}..."

    def validate(self) -> bool:
        return len(self.wallet_address) > 20


class PaymentProcessor:
    """
    Generalized processor using Strategy pattern.

    Works with any payment strategy without knowing specifics.
    """

    def __init__(self, strategy: PaymentStrategy):
        """Initialize with a payment strategy."""
        self.strategy = strategy

    def process_payment(self, amount: float) -> str:
        """
        Process payment using current strategy.

        Same method works for credit card, PayPal, crypto, etc.
        """
        if not self.strategy.validate():
            return "Payment validation failed"

        return self.strategy.pay(amount)

    def change_strategy(self, strategy: PaymentStrategy) -> None:
        """Change payment strategy at runtime."""
        self.strategy = strategy


# ============================================================================
# PART 5: PROTOCOL-BASED GENERALIZATION (DUCK TYPING)
# ============================================================================

class Comparable(Protocol):
    """
    Protocol defining comparison interface.

    Any class with __lt__ method satisfies this protocol.
    More flexible than inheritance-based generalization.
    """

    def __lt__(self, other: Any) -> bool:
        """Less than comparison."""
        ...


def sort_items(items: List[Comparable]) -> List[Comparable]:
    """
    Generalized sorting function.

    Works with ANY type that implements comparison,
    without requiring inheritance from a common base class.
    """
    return sorted(items)


class Product:
    """Product class with comparison based on price."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __lt__(self, other: 'Product') -> bool:
        """Compare products by price."""
        return self.price < other.price

    def __repr__(self) -> str:
        return f"Product({self.name}, ${self.price})"


class Student:
    """Student class with comparison based on grade."""

    def __init__(self, name: str, grade: float):
        self.name = name
        self.grade = grade

    def __lt__(self, other: 'Student') -> bool:
        """Compare students by grade."""
        return self.grade < other.grade

    def __repr__(self) -> str:
        return f"Student({self.name}, {self.grade})"


# ============================================================================
# PART 6: TEMPLATE METHOD PATTERN
# ============================================================================

class DataProcessor(ABC):
    """
    Generalized data processing template.

    Defines algorithm structure, delegates specifics to subclasses.
    """

    def process(self, data: Any) -> Any:
        """
        Template method defining processing steps.

        This is the generalized algorithm that all processors follow.
        Specific steps are implemented by subclasses.
        """
        validated_data = self.validate(data)
        transformed_data = self.transform(validated_data)
        processed_data = self.analyze(transformed_data)
        return self.format_output(processed_data)

    @abstractmethod
    def validate(self, data: Any) -> Any:
        """Validate input - specific to each processor."""
        pass

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transform data - specific to each processor."""
        pass

    @abstractmethod
    def analyze(self, data: Any) -> Any:
        """Analyze data - specific to each processor."""
        pass

    def format_output(self, data: Any) -> Any:
        """
        Format output - default implementation.

        Can be overridden by subclasses if needed.
        """
        return data


class CSVProcessor(DataProcessor):
    """Specific processor for CSV data."""

    def validate(self, data: str) -> List[str]:
        """Validate CSV has content."""
        lines = data.strip().split('\n')
        if not lines:
            raise ValueError("Empty CSV")
        return lines

    def transform(self, data: List[str]) -> List[List[str]]:
        """Transform CSV lines into rows."""
        return [line.split(',') for line in data]

    def analyze(self, data: List[List[str]]) -> Dict[str, int]:
        """Count rows and columns."""
        return {
            'rows': len(data),
            'columns': len(data[0]) if data else 0
        }


class JSONProcessor(DataProcessor):
    """Specific processor for JSON data."""

    def validate(self, data: str) -> str:
        """Validate JSON is not empty."""
        if not data.strip():
            raise ValueError("Empty JSON")
        return data

    def transform(self, data: str) -> Dict:
        """Transform JSON string to dictionary."""
        import json
        return json.loads(data)

    def analyze(self, data: Dict) -> Dict[str, int]:
        """Count keys in JSON."""
        return {'keys': len(data)}


# ============================================================================
# PART 7: HIGHER-ORDER FUNCTIONS - ULTIMATE GENERALIZATION
# ============================================================================

def apply_operation(data: List[T], operation: Callable[[T], Any]) -> List[Any]:
    """
    Most general transformation function.

    Applies any operation to any data type.
    """
    return [operation(item) for item in data]


def filter_items(data: List[T], condition: Callable[[T], bool]) -> List[T]:
    """
    Most general filtering function.

    Filters any data based on any condition.
    """
    return [item for item in data if condition(item)]


def compose(*functions: Callable) -> Callable:
    """
    Function composition - ultimate generalization.

    Combines multiple functions into one.

    Example: compose(f, g, h)(x) == f(g(h(x)))
    """

    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result

    return inner


# ============================================================================
# PART 8: MIXIN-BASED GENERALIZATION
# ============================================================================

class JSONSerializableMixin:
    """
    Generalized serialization behavior.

    Can be mixed into any class to add JSON serialization.
    """

    def to_json(self) -> Dict[str, Any]:
        """Convert object to JSON-serializable dictionary."""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }


class TimestampMixin:
    """
    Generalized timestamp behavior.

    Adds creation and update tracking to any class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def touch(self) -> None:
        """Update the timestamp."""
        from datetime import datetime
        self.updated_at = datetime.now()


class User(JSONSerializableMixin, TimestampMixin):
    """
    User class gaining generalized behaviors from mixins.

    Gets JSON serialization and timestamps without reimplementing.
    """

    def __init__(self, username: str, email: str):
        super().__init__()
        self.username = username
        self.email = email


class Article(JSONSerializableMixin, TimestampMixin):
    """
    Article class gaining same generalized behaviors.

    Same mixins provide same functionality to different classes.
    """

    def __init__(self, title: str, content: str):
        super().__init__()
        self.title = title
        self.content = content


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=== FUNCTION GENERALIZATION ===")
    prices = [10.5, 20.0, 15.75]
    print(f"Sum: {sum_values(prices)}")
    print(f"Product: {multiply_values([2, 3, 4])}")
    print(f"Maximum: {find_maximum(prices)}")

    print("\n=== CLASS HIERARCHY GENERALIZATION ===")
    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 3, 5)
    ]
    for shape in shapes:
        print(shape.describe())
    print(f"Total Area: {calculate_total_area(shapes):.2f}")

    print("\n=== GENERIC TYPES ===")
    int_stack = Stack[int]()
    int_stack.push(1)
    int_stack.push(2)
    print(f"Stack pop: {int_stack.pop()}")

    string_stack = Stack[str]()
    string_stack.push("hello")
    string_stack.push("world")
    print(f"Stack pop: {string_stack.pop()}")

    print("\n=== STRATEGY PATTERN ===")
    processor = PaymentProcessor(CreditCardPayment("1234567890123456", "123"))
    print(processor.process_payment(99.99))

    processor.change_strategy(PayPalPayment("user@example.com"))
    print(processor.process_payment(49.99))

    print("\n=== PROTOCOL-BASED GENERALIZATION ===")
    products = [Product("Laptop", 999), Product("Mouse", 25), Product("Keyboard", 75)]
    sorted_products = sort_items(products)
    print(f"Sorted products: {sorted_products}")

    students = [Student("Alice", 85), Student("Bob", 92), Student("Charlie", 78)]
    sorted_students = sort_items(students)
    print(f"Sorted students: {sorted_students}")

    print("\n=== TEMPLATE METHOD ===")
    csv_data = "name,age\nAlice,30\nBob,25"
    csv_processor = CSVProcessor()
    result = csv_processor.process(csv_data)
    print(f"CSV analysis: {result}")

    print("\n=== HIGHER-ORDER FUNCTIONS ===")
    numbers = [1, 2, 3, 4, 5]
    doubled = apply_operation(numbers, lambda x: x * 2)
    print(f"Doubled: {doubled}")

    evens = filter_items(numbers, lambda x: x % 2 == 0)
    print(f"Even numbers: {evens}")

    print("\n=== MIXIN GENERALIZATION ===")
    user = User("john_doe", "john@example.com")
    print(f"User JSON: {user.to_json()}")
    print(f"Created at: {user.created_at}")