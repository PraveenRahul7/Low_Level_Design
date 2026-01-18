"""
INHERITANCE VS COMPOSITION IN PYTHON
=====================================

INHERITANCE: "IS-A" Relationship
- A class extends another class
- Inherits all attributes and methods
- Creates tight coupling between parent and child

COMPOSITION: "HAS-A" Relationship
- A class contains instances of other classes
- Builds complex functionality by combining simpler objects
- Creates loose coupling and better flexibility

COMPOSITION OVER INHERITANCE PRINCIPLE:
Favor object composition over class inheritance to achieve more flexible,
maintainable, and testable code.
"""

from abc import ABC, abstractmethod
from typing import List, Protocol
from dataclasses import dataclass


# ============================================================================
# PART 1: INHERITANCE BASICS
# ============================================================================

class Animal:
    """
    Base class demonstrating inheritance.

    Inheritance models "IS-A" relationships:
    - A Dog IS-A Animal
    - A Cat IS-A Animal

    Use inheritance when:
    - There's a clear hierarchical relationship
    - Subclasses are specialized versions of the base class
    - You want to share common behavior across related classes
    """

    def __init__(self, name: str, age: int):
        """
        Initialize common animal attributes.

        All subclasses inherit these attributes automatically.
        """
        self.name = name
        self.age = age
        self._energy = 100

    def eat(self) -> str:
        """
        Common behavior inherited by all animals.

        Subclasses can use this as-is or override it.
        """
        self._energy = min(100, self._energy + 20)
        return f"{self.name} is eating and gained energy"

    def sleep(self) -> str:
        """Another shared behavior."""
        self._energy = 100
        return f"{self.name} is sleeping"

    def make_sound(self) -> str:
        """
        Method meant to be overridden by subclasses.

        Provides a default but expects specialization.
        """
        return "Some generic animal sound"


class Dog(Animal):
    """
    Dog inherits from Animal.

    Inheritance Benefits Demonstrated:
    1. Code reuse: Gets eat(), sleep(), age, name for free
    2. Polymorphism: Can be treated as Animal
    3. Specialization: Adds dog-specific behavior
    """

    def __init__(self, name: str, age: int, breed: str):
        """
        Initialize Dog with parent class initialization.

        super().__init__() calls parent constructor to set up
        inherited attributes before adding dog-specific ones.
        """
        super().__init__(name, age)
        self.breed = breed  # Dog-specific attribute

    def make_sound(self) -> str:
        """
        Override parent method with dog-specific implementation.

        Method overriding allows specialized behavior while
        maintaining the same interface.
        """
        return f"{self.name} says: Woof! Woof!"

    def fetch(self) -> str:
        """
        Dog-specific behavior not in parent class.

        Adds functionality unique to dogs.
        """
        if self._energy < 20:
            return f"{self.name} is too tired to fetch"
        self._energy -= 20
        return f"{self.name} fetches the ball!"


class Cat(Animal):
    """Cat inherits from Animal with cat-specific behavior."""

    def __init__(self, name: str, age: int, indoor: bool):
        super().__init__(name, age)
        self.indoor = indoor

    def make_sound(self) -> str:
        """Cat-specific sound."""
        return f"{self.name} says: Meow!"

    def scratch(self) -> str:
        """Cat-specific behavior."""
        return f"{self.name} scratches the furniture"


# ============================================================================
# PART 2: PROBLEMS WITH DEEP INHERITANCE
# ============================================================================

class Vehicle:
    """Base class for vehicles."""

    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model

    def start_engine(self) -> str:
        return f"{self.brand} {self.model} engine started"


class Car(Vehicle):
    """Car inherits from Vehicle."""

    def __init__(self, brand: str, model: str, doors: int):
        super().__init__(brand, model)
        self.doors = doors

    def open_trunk(self) -> str:
        return "Trunk opened"


class ElectricCar(Car):
    """
    Problem: Deep inheritance creates tight coupling.

    Issues with this approach:
    1. Inherits ALL behavior from Car and Vehicle
    2. Cannot easily share electric functionality with ElectricMotorcycle
    3. If Car changes, ElectricCar might break
    4. Stuck with assumptions from parent classes (like having a trunk)
    5. Cannot compose different capabilities flexibly

    What if we want:
    - Electric motorcycle (no trunk, no 4 doors)
    - Hybrid car (both electric AND gas engine)
    - Electric boat (no wheels, but has electric motor)

    Inheritance becomes rigid and problematic.
    """

    def __init__(self, brand: str, model: str, doors: int, battery_capacity: int):
        super().__init__(brand, model, doors)
        self.battery_capacity = battery_capacity

    def charge_battery(self) -> str:
        return f"Charging {self.battery_capacity}kWh battery"

    def start_engine(self) -> str:
        """
        Problem: Must override parent method.

        Electric cars don't have traditional engines,
        but we're forced to deal with parent's engine concept.
        """
        return "Electric motor activated (no engine)"


# ============================================================================
# PART 3: COMPOSITION BASICS
# ============================================================================

class Engine:
    """
    Standalone component for engine functionality.

    Composition Principle: Create small, focused classes that do one thing well.
    These can be composed together to build complex behavior.

    Benefits:
    - Reusable across different vehicle types
    - Easy to test in isolation
    - Can be swapped or upgraded independently
    - No inheritance hierarchy needed
    """

    def __init__(self, engine_type: str, horsepower: int):
        """Initialize engine specifications."""
        self.engine_type = engine_type
        self.horsepower = horsepower
        self._running = False

    def start(self) -> str:
        """Start the engine."""
        self._running = True
        return f"{self.engine_type} engine started ({self.horsepower}hp)"

    def stop(self) -> str:
        """Stop the engine."""
        self._running = False
        return f"{self.engine_type} engine stopped"

    def is_running(self) -> bool:
        """Check if engine is running."""
        return self._running


class ElectricMotor:
    """
    Alternative to Engine for electric vehicles.

    Composition allows us to have completely different power sources
    without forcing them into an inheritance hierarchy.
    """

    def __init__(self, battery_capacity: int, motor_power: int):
        """Initialize electric motor specifications."""
        self.battery_capacity = battery_capacity
        self.motor_power = motor_power
        self._charge_level = 100
        self._active = False

    def start(self) -> str:
        """Activate electric motor."""
        if self._charge_level > 0:
            self._active = True
            return f"Electric motor activated ({self.motor_power}kW)"
        return "Battery too low to start"

    def stop(self) -> str:
        """Deactivate electric motor."""
        self._active = False
        return "Electric motor deactivated"

    def charge(self) -> str:
        """Charge the battery."""
        self._charge_level = 100
        return f"Battery charged to {self._charge_level}%"

    def is_running(self) -> bool:
        """Check if motor is active."""
        return self._active


class Wheels:
    """
    Component for wheel functionality.

    Can be used by cars, motorcycles, trucks, etc.
    without forcing them into same inheritance tree.
    """

    def __init__(self, count: int, size: int):
        """Initialize wheel specifications."""
        self.count = count
        self.size = size

    def rotate(self) -> str:
        """Rotate wheels for movement."""
        return f"{self.count} wheels rotating (size: {self.size} inches)"


class GPS:
    """
    Optional component for navigation.

    Composition Advantage: Can add GPS to ANY vehicle
    without changing inheritance hierarchy.
    """

    def __init__(self):
        """Initialize GPS system."""
        self._location = "Unknown"

    def get_location(self) -> str:
        """Get current location."""
        return f"Current location: {self._location}"

    def navigate_to(self, destination: str) -> str:
        """Navigate to destination."""
        return f"Navigating to {destination}"


# ============================================================================
# PART 4: COMPOSITION OVER INHERITANCE - THE SOLUTION
# ============================================================================

class ModernCar:
    """
    Car built using COMPOSITION instead of INHERITANCE.

    Advantages:
    1. Flexible: Can easily swap components (electric motor vs gas engine)
    2. Maintainable: Changes to Engine don't affect Car
    3. Testable: Each component can be tested independently
    4. Extensible: Add new components (GPS, radio) without changing class hierarchy
    5. Reusable: Same components can be used in different vehicle types

    This is "HAS-A" relationship:
    - Car HAS-A Engine
    - Car HAS-A Wheels
    - Car HAS-A GPS (optional)
    """

    def __init__(
            self,
            brand: str,
            model: str,
            engine: Engine,
            wheels: Wheels,
            gps: GPS = None
    ):
        """
        Initialize car with composed components.

        Dependency Injection: Components are provided from outside,
        making the class flexible and testable.
        """
        self.brand = brand
        self.model = model
        self._engine = engine  # Composed component
        self._wheels = wheels  # Composed component
        self._gps = gps  # Optional composed component

    def start(self) -> str:
        """
        Delegate to engine component.

        Car doesn't know HOW to start an engine,
        it just asks its engine component to start.
        """
        return f"{self.brand} {self.model}: {self._engine.start()}"

    def drive(self) -> str:
        """
        Use multiple components together.

        Combines engine and wheels functionality.
        """
        if not self._engine.is_running():
            return "Cannot drive - engine not started"
        return f"Driving with {self._wheels.rotate()}"

    def navigate(self, destination: str) -> str:
        """
        Use optional component if available.

        Composition allows optional features without inheritance.
        """
        if self._gps is None:
            return "No GPS system installed"
        return self._gps.navigate_to(destination)

    def upgrade_to_gps(self, gps: GPS) -> None:
        """
        Add component at runtime.

        With composition, can add features after object creation!
        Impossible with pure inheritance.
        """
        self._gps = gps


class ModernElectricCar:
    """
    Electric car using composition.

    Same pattern as ModernCar, but with ElectricMotor instead of Engine.
    No inheritance needed - just different composition!

    This is MORE flexible than ElectricCar(Car) inheritance because:
    - Can reuse ElectricMotor in boats, bikes, scooters
    - Can easily create HybridCar with BOTH Engine and ElectricMotor
    - No baggage from parent class assumptions
    """

    def __init__(
            self,
            brand: str,
            model: str,
            motor: ElectricMotor,
            wheels: Wheels,
            gps: GPS = None
    ):
        self.brand = brand
        self.model = model
        self._motor = motor
        self._wheels = wheels
        self._gps = gps

    def start(self) -> str:
        """Delegate to electric motor."""
        return f"{self.brand} {self.model}: {self._motor.start()}"

    def drive(self) -> str:
        """Drive using electric motor."""
        if not self._motor.is_running():
            return "Cannot drive - motor not activated"
        return f"Driving silently with {self._wheels.rotate()}"

    def charge(self) -> str:
        """Charge battery - electric-specific feature."""
        return self._motor.charge()

    def navigate(self, destination: str) -> str:
        """Navigate using GPS if available."""
        if self._gps is None:
            return "No GPS system installed"
        return self._gps.navigate_to(destination)


class HybridCar:
    """
    Hybrid car with BOTH gas engine AND electric motor.

    The Ultimate Composition Example:
    With inheritance, how would you create a class that inherits from
    both GasCar and ElectricCar? Multiple inheritance is messy.

    With composition? Easy! Just include both components.
    This demonstrates why composition is more flexible.
    """

    def __init__(
            self,
            brand: str,
            model: str,
            engine: Engine,
            motor: ElectricMotor,
            wheels: Wheels
    ):
        """
        Initialize with both power sources.

        Composition makes this trivial - just add both components!
        """
        self.brand = brand
        self.model = model
        self._engine = engine
        self._motor = motor
        self._wheels = wheels
        self._mode = "electric"  # Default to electric mode

    def start(self) -> str:
        """Start in electric mode by default."""
        result = self._motor.start()
        return f"{self.brand} {self.model}: {result}"

    def switch_to_gas(self) -> str:
        """Switch to gas engine mode."""
        self._motor.stop()
        self._engine.start()
        self._mode = "gas"
        return "Switched to gas engine mode"

    def switch_to_electric(self) -> str:
        """Switch to electric motor mode."""
        self._engine.stop()
        self._motor.start()
        self._mode = "electric"
        return "Switched to electric motor mode"

    def drive(self) -> str:
        """Drive using current mode."""
        if self._mode == "electric" and self._motor.is_running():
            return f"Driving on electric: {self._wheels.rotate()}"
        elif self._mode == "gas" and self._engine.is_running():
            return f"Driving on gas: {self._wheels.rotate()}"
        return "No power source active"


# ============================================================================
# PART 5: INTERFACE-BASED COMPOSITION (PROTOCOL)
# ============================================================================

class PowerSource(Protocol):
    """
    Protocol defining interface for any power source.

    Benefits of Protocol with Composition:
    - Define what components must do (interface)
    - Don't care about HOW they do it (implementation)
    - Extremely flexible - any class matching this interface works

    This enables true polymorphism without inheritance!
    """

    def start(self) -> str:
        """Start the power source."""
        ...

    def stop(self) -> str:
        """Stop the power source."""
        ...

    def is_running(self) -> bool:
        """Check if power source is active."""
        ...


class UniversalVehicle:
    """
    Vehicle that works with ANY power source matching the protocol.

    Composition + Protocol = Maximum Flexibility:
    - Can use Engine, ElectricMotor, or any future power source
    - No inheritance required
    - Power source just needs to match the interface

    This is composition over inheritance at its finest!
    """

    def __init__(
            self,
            brand: str,
            model: str,
            power_source: PowerSource,  # Accept ANY PowerSource
            wheels: Wheels
    ):
        """
        Initialize with any power source.

        Type hint says "any object matching PowerSource protocol"
        Don't care if it's Engine, ElectricMotor, or NuclearReactor!
        """
        self.brand = brand
        self.model = model
        self._power_source = power_source
        self._wheels = wheels

    def start(self) -> str:
        """
        Start using whatever power source we have.

        Works with ANY object that has start() method!
        """
        return f"{self.brand} {self.model}: {self._power_source.start()}"

    def drive(self) -> str:
        """Drive using any power source."""
        if not self._power_source.is_running():
            return "Cannot drive - power source not active"
        return f"Driving with {self._wheels.rotate()}"


# ============================================================================
# PART 6: COMPOSITION WITH DELEGATION
# ============================================================================

class Logger:
    """Component for logging functionality."""

    def log(self, message: str) -> None:
        """Log a message."""
        print(f"[LOG] {message}")


class Authenticator:
    """Component for authentication."""

    def __init__(self):
        self._users = {"admin": "password123"}

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user."""
        return self._users.get(username) == password


class DatabaseConnection:
    """Component for database operations."""

    def __init__(self):
        self._data = {}

    def save(self, key: str, value: any) -> None:
        """Save data to database."""
        self._data[key] = value

    def get(self, key: str) -> any:
        """Retrieve data from database."""
        return self._data.get(key)


class UserService:
    """
    Service using composition and delegation.

    Delegation Pattern:
    - UserService delegates logging to Logger
    - UserService delegates auth to Authenticator
    - UserService delegates storage to DatabaseConnection

    Benefits:
    1. Single Responsibility: Each component has one job
    2. Testability: Can mock any component for testing
    3. Flexibility: Can swap implementations (file logger vs database logger)
    4. Maintainability: Changes to logging don't affect authentication

    Compare to inheritance:
    - Would need UserService(Logger, Authenticator, Database)?
    - Multiple inheritance is complicated and fragile
    - Composition is clean and simple
    """

    def __init__(
            self,
            logger: Logger,
            authenticator: Authenticator,
            database: DatabaseConnection
    ):
        """
        Inject all dependencies.

        This is Dependency Injection + Composition.
        Makes class incredibly flexible and testable.
        """
        self._logger = logger
        self._authenticator = authenticator
        self._database = database

    def register_user(self, username: str, password: str) -> bool:
        """
        Register new user using composed components.

        Notice how each component handles its own concern:
        - Logger handles logging
        - Database handles storage
        - This class just orchestrates
        """
        self._logger.log(f"Attempting to register user: {username}")

        if self._database.get(username):
            self._logger.log(f"Registration failed: {username} already exists")
            return False

        self._database.save(username, password)
        self._logger.log(f"User registered successfully: {username}")
        return True

    def login(self, username: str, password: str) -> bool:
        """
        Login user using composed components.

        Delegates authentication to Authenticator component.
        """
        self._logger.log(f"Login attempt: {username}")

        if self._authenticator.authenticate(username, password):
            self._logger.log(f"Login successful: {username}")
            return True

        self._logger.log(f"Login failed: {username}")
        return False


# ============================================================================
# PART 7: WHEN TO USE INHERITANCE VS COMPOSITION
# ============================================================================

"""
USE INHERITANCE WHEN:
---------------------
1. There's a clear "IS-A" relationship
   - Dog IS-A Animal ✓
   - Square IS-A Shape ✓

2. The hierarchy is shallow (2-3 levels max)
   - Shape -> Polygon -> Triangle ✓

3. Subclasses are true specializations
   - All dogs share animal characteristics

4. You need polymorphism with a fixed interface
   - All shapes must have area() and perimeter()

Example: Animal hierarchy (shown in Part 1)


USE COMPOSITION WHEN:
--------------------
1. There's a "HAS-A" or "USES-A" relationship
   - Car HAS-A Engine ✓
   - Service USES-A Logger ✓

2. You need flexibility in behavior
   - Swap gas engine for electric motor
   - Change logger implementation

3. You want to combine features from multiple sources
   - Hybrid car with engine AND motor
   - Service with logger AND authenticator AND database

4. The hierarchy would be deep or complex
   - Vehicle -> Car -> ElectricCar -> LuxuryElectricCar ✗
   - Better: Vehicle with composed components ✓

5. You want runtime flexibility
   - Add GPS after car creation
   - Switch power sources dynamically

Example: Modern vehicles (shown in Part 4)


COMPOSITION OVER INHERITANCE PRINCIPLE:
---------------------------------------
Default to composition. Only use inheritance when there's
a genuine hierarchical relationship and you need polymorphism.

Composition gives you:
- Loose coupling
- High flexibility
- Better testability
- Easier maintenance
- Runtime adaptability

Inheritance gives you:
- Code reuse
- Polymorphism
- Clear hierarchies
- Simpler in trivial cases

Most real-world problems benefit from composition!
"""

# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=== INHERITANCE DEMO ===")
    dog = Dog("Buddy", 5, "Golden Retriever")
    cat = Cat("Whiskers", 3, True)

    print(dog.make_sound())
    print(dog.fetch())
    print(cat.make_sound())
    print(cat.scratch())

    # Polymorphism: treating different animals uniformly
    animals: List[Animal] = [dog, cat]
    for animal in animals:
        print(animal.eat())

    print("\n=== COMPOSITION DEMO ===")

    # Create components
    gas_engine = Engine("V6", 300)
    electric_motor = ElectricMotor(75, 200)
    car_wheels = Wheels(4, 18)
    gps = GPS()

    # Build gas car with composition
    gas_car = ModernCar("Toyota", "Camry", gas_engine, car_wheels, gps)
    print(gas_car.start())
    print(gas_car.drive())
    print(gas_car.navigate("Downtown"))

    # Build electric car with composition
    electric_car = ModernElectricCar("Tesla", "Model 3", electric_motor, car_wheels)
    print(electric_car.start())
    print(electric_car.drive())
    print(electric_car.charge())

    # Add GPS later (impossible with pure inheritance!)
    electric_car._gps = GPS()
    print(electric_car.navigate("Supercharger Station"))

    print("\n=== HYBRID CAR DEMO (Composition Power) ===")
    hybrid_engine = Engine("Inline-4", 150)
    hybrid_motor = ElectricMotor(50, 100)
    hybrid_wheels = Wheels(4, 17)

    hybrid = HybridCar("Toyota", "Prius", hybrid_engine, hybrid_motor, hybrid_wheels)
    print(hybrid.start())
    print(hybrid.drive())
    print(hybrid.switch_to_gas())
    print(hybrid.drive())

    print("\n=== PROTOCOL-BASED COMPOSITION ===")
    # UniversalVehicle works with ANY PowerSource
    universal1 = UniversalVehicle("Generic", "V1", Engine("V8", 400), car_wheels)
    universal2 = UniversalVehicle("Generic", "V2", ElectricMotor(100, 250), car_wheels)

    print(universal1.start())
    print(universal2.start())

    print("\n=== DELEGATION PATTERN ===")
    logger = Logger()
    auth = Authenticator()
    db = DatabaseConnection()

    user_service = UserService(logger, auth, db)
    user_service.register_user("alice", "secure_password")
    user_service.login("alice", "secure_password")
    user_service.login("alice", "wrong_password")