"""
ABSTRACTION & ENCAPSULATION IN PYTHON
======================================

Abstraction: Hiding implementation details and showing only essential features.
Encapsulation: Bundling data and methods together, restricting direct access.
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
import functools


# ============================================================================
# PART 1: ENCAPSULATION - ACCESS MODIFIERS
# ============================================================================

class BankAccount:
    """
    Demonstrates encapsulation using Python's naming conventions.

    Python uses naming conventions for access control:
    - public: normal_name (accessible everywhere)
    - protected: _single_underscore (convention: internal use)
    - private: __double_underscore (name mangling applied)
    """

    def __init__(self, account_number: str, balance: float):
        """
        Initialize a bank account.

        Args:
            account_number: Public account identifier
            balance: Initial account balance
        """
        self.account_number = account_number  # Public
        self._account_type = "savings"  # Protected (convention)
        self.__balance = balance  # Private (name mangled)

    def deposit(self, amount: float) -> None:
        """Public method to deposit money."""
        if amount > 0:
            self.__balance += amount
            self.__log_transaction("deposit", amount)

    def withdraw(self, amount: float) -> bool:
        """Public method to withdraw money."""
        if self.__validate_withdrawal(amount):
            self.__balance -= amount
            self.__log_transaction("withdrawal", amount)
            return True
        return False

    def get_balance(self) -> float:
        """Public getter for private balance."""
        return self.__balance

    def __validate_withdrawal(self, amount: float) -> bool:
        """
        Private method - name mangled to _BankAccount__validate_withdrawal.

        Only accessible within this class (enforced by name mangling).
        """
        return amount > 0 and amount <= self.__balance

    def __log_transaction(self, transaction_type: str, amount: float) -> None:
        """Private method to log transactions."""
        print(f"{transaction_type.title()}: ${amount:.2f}")


# ============================================================================
# PART 2: PROPERTY DECORATOR - PYTHONIC ENCAPSULATION
# ============================================================================

class Temperature:
    """
    Demonstrates @property decorator for getters/setters.

    Properties allow controlled access to attributes while maintaining
    a clean, Pythonic interface (no Java-style getCelsius/setCelsius).
    """

    def __init__(self, celsius: float = 0):
        """Initialize temperature in Celsius."""
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """
        Getter for celsius temperature.

        Accessed as: temp.celsius (not temp.celsius())
        """
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """
        Setter for celsius temperature with validation.

        Usage: temp.celsius = 25
        """
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Computed property - converts Celsius to Fahrenheit."""
        return (self._celsius * 9 / 5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Setter that converts Fahrenheit to Celsius."""
        self.celsius = (value - 32) * 5 / 9

    @celsius.deleter
    def celsius(self) -> None:
        """
        Deleter for celsius property.

        Usage: del temp.celsius
        """
        print("Deleting temperature data")
        del self._celsius


# ============================================================================
# PART 3: ABSTRACT BASE CLASSES (ABC)
# ============================================================================

class Animal(ABC):
    """
    Abstract base class using abc.ABC.

    Cannot be instantiated directly. Subclasses MUST implement
    all @abstractmethod decorated methods.
    """

    def __init__(self, name: str):
        """Initialize animal with name."""
        self.name = name

    @abstractmethod
    def make_sound(self) -> str:
        """
        Abstract method - must be implemented by subclasses.

        Raises TypeError if subclass doesn't implement this.
        """
        pass

    @abstractmethod
    def move(self) -> str:
        """Another abstract method requiring implementation."""
        pass

    def eat(self) -> str:
        """
        Concrete method - provides default implementation.

        Subclasses inherit this but can override if needed.
        """
        return f"{self.name} is eating"


class Dog(Animal):
    """Concrete implementation of Animal ABC."""

    def make_sound(self) -> str:
        """Implement required abstract method."""
        return "Woof!"

    def move(self) -> str:
        """Implement required abstract method."""
        return "Running on four legs"


class Bird(Animal):
    """Another concrete implementation."""

    def make_sound(self) -> str:
        return "Chirp!"

    def move(self) -> str:
        return "Flying in the sky"

    def eat(self) -> str:
        """Override concrete method from parent."""
        return f"{self.name} is pecking at seeds"


# ============================================================================
# PART 4: ABSTRACT PROPERTIES
# ============================================================================

class Shape(ABC):
    """Demonstrates abstract properties."""

    @property
    @abstractmethod
    def area(self) -> float:
        """
        Abstract property - subclasses must implement as property.

        Note: @property comes BEFORE @abstractmethod
        """
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        """Another abstract property."""
        pass


class Rectangle(Shape):
    """Concrete shape implementing abstract properties."""

    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def area(self) -> float:
        """Implement abstract property."""
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        """Implement abstract property."""
        return 2 * (self._width + self._height)


# ============================================================================
# PART 5: PROTOCOLS (STRUCTURAL SUBTYPING) - Python 3.8+
# ============================================================================

@runtime_checkable
class Drawable(Protocol):
    """
    Protocol defines an interface via duck typing.

    Unlike ABC, classes don't need to explicitly inherit.
    They just need to implement the required methods.

    @runtime_checkable allows isinstance() checks.
    """

    def draw(self) -> str:
        """Method signature that implementing classes must have."""
        ...


class Circle:
    """
    Implicitly implements Drawable protocol.

    No explicit inheritance needed!
    """

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        """Implements the protocol method."""
        return f"Drawing a circle with radius {self.radius}"


class Square:
    """Another class implicitly implementing Drawable."""

    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"Drawing a square with side {self.side}"


def render(obj: Drawable) -> None:
    """
    Function accepting any Drawable object.

    Works with any object that has a draw() method,
    regardless of inheritance hierarchy.
    """
    print(obj.draw())


# ============================================================================
# PART 6: DESCRIPTOR PROTOCOL - ADVANCED ENCAPSULATION
# ============================================================================

class ValidatedString:
    """
    Descriptor for validated string attributes.

    Descriptors implement __get__, __set__, and/or __delete__
    to control attribute access at the class level.
    """

    def __init__(self, min_length: int = 0, max_length: int = 100):
        """Initialize descriptor with validation rules."""
        self.min_length = min_length
        self.max_length = max_length
        # Use unique names to avoid conflicts
        self.name = None

    def __set_name__(self, owner, name):
        """
        Called when descriptor is assigned to a class attribute.

        Automatically gets the attribute name.
        """
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        """
        Getter for descriptor.

        Args:
            obj: Instance of the class (None for class access)
            objtype: The class itself
        """
        if obj is None:
            return self
        return getattr(obj, self.name, "")

    def __set__(self, obj, value):
        """
        Setter for descriptor with validation.

        Args:
            obj: Instance of the class
            value: Value being set
        """
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value).__name__}")
        if len(value) < self.min_length:
            raise ValueError(f"String too short (min: {self.min_length})")
        if len(value) > self.max_length:
            raise ValueError(f"String too long (max: {self.max_length})")
        setattr(obj, self.name, value)


class Person:
    """Class using descriptor for validated attributes."""

    # Class attributes using descriptors
    first_name = ValidatedString(min_length=1, max_length=50)
    last_name = ValidatedString(min_length=1, max_length=50)

    def __init__(self, first_name: str, last_name: str):
        """Descriptor validation automatically applies."""
        self.first_name = first_name
        self.last_name = last_name


# ============================================================================
# PART 7: CLASSMETHOD AND STATICMETHOD DECORATORS
# ============================================================================

class MathOperations:
    """
    Demonstrates @classmethod and @staticmethod.

    These provide different levels of abstraction and encapsulation.
    """

    PI = 3.14159

    def __init__(self, precision: int = 2):
        """Instance method - requires instance."""
        self.precision = precision

    @classmethod
    def from_config(cls, config: dict):
        """
        Class method - receives class as first argument.

        Common use: Alternative constructors (factory methods).
        Can access class attributes and create instances.
        """
        precision = config.get("precision", 2)
        return cls(precision)

    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Static method - no self or cls parameter.

        Use when method doesn't need instance or class data.
        Belongs to class namespace but doesn't access class state.
        """
        return a + b

    @classmethod
    def get_pi(cls) -> float:
        """Class method accessing class attribute."""
        return cls.PI


# ============================================================================
# PART 8: CUSTOM PROPERTY DECORATOR
# ============================================================================

def cached_property(func):
    """
    Custom decorator creating a cached property.

    Demonstrates how decorators enable encapsulation patterns.
    Computes value once and caches it.
    """
    attr_name = f"_cached_{func.__name__}"

    @functools.wraps(func)
    def wrapper(self):
        """Wrapper function that caches result."""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property(wrapper)


class DataProcessor:
    """Class using custom cached property."""

    def __init__(self, data: list):
        self.data = data

    @cached_property
    def processed_data(self) -> list:
        """
        Expensive computation cached after first access.

        Accessed as: processor.processed_data
        """
        print("Processing data (only runs once)...")
        return [x * 2 for x in self.data]


# ============================================================================
# PART 9: MIXIN CLASSES - COMPOSITION OVER INHERITANCE
# ============================================================================

class LoggerMixin:
    """
    Mixin providing logging functionality.

    Mixins add functionality without being full base classes.
    Use for cross-cutting concerns.
    """

    def log(self, message: str, level: str = "INFO") -> None:
        """Add logging capability to any class."""
        print(f"[{level}] {self.__class__.__name__}: {message}")


class SerializableMixin:
    """Mixin providing serialization."""

    def to_dict(self) -> dict:
        """Convert public attributes to dictionary."""
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith('_')}


class User(LoggerMixin, SerializableMixin):
    """
    Class using multiple mixins.

    Gains logging and serialization without deep inheritance.
    """

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.log(f"User {username} created")


# ============================================================================
# PART 10: INTERFACE SEGREGATION WITH ABC
# ============================================================================

class Readable(ABC):
    """Small, focused interface for reading."""

    @abstractmethod
    def read(self) -> str:
        pass


class Writable(ABC):
    """Small, focused interface for writing."""

    @abstractmethod
    def write(self, data: str) -> None:
        pass


class File(Readable, Writable):
    """
    Class implementing multiple small interfaces.

    Interface Segregation Principle: Many specific interfaces
    are better than one general-purpose interface.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self._content = ""

    def read(self) -> str:
        """Implement Readable interface."""
        return self._content

    def write(self, data: str) -> None:
        """Implement Writable interface."""
        self._content = data


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=== ENCAPSULATION DEMO ===")
    account = BankAccount("ACC123", 1000)
    account.deposit(500)
    print(f"Balance: ${account.get_balance()}")

    print("\n=== PROPERTY DEMO ===")
    temp = Temperature()
    temp.celsius = 25
    print(f"Temperature: {temp.celsius}°C = {temp.fahrenheit}°F")

    print("\n=== ABSTRACTION (ABC) DEMO ===")
    dog = Dog("Buddy")
    print(f"{dog.name} says: {dog.make_sound()}")
    print(f"{dog.name} moves by: {dog.move()}")

    print("\n=== PROTOCOL DEMO ===")
    circle = Circle(5)
    square = Square(4)
    print(f"Is circle Drawable? {isinstance(circle, Drawable)}")
    render(circle)
    render(square)

    print("\n=== DESCRIPTOR DEMO ===")
    person = Person("John", "Doe")
    print(f"Name: {person.first_name} {person.last_name}")

    print("\n=== CACHED PROPERTY DEMO ===")
    processor = DataProcessor([1, 2, 3, 4, 5])
    print(processor.processed_data)  # Processes
    print(processor.processed_data)  # Uses cache

    print("\n=== MIXIN DEMO ===")
    user = User("johndoe", "john@example.com")
    print(user.to_dict())


