class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius Cannot be Negative")
        self._radius = value

    def __call__(self, new_radius):
        """Set radius when object is called"""
        self.radius = new_radius  # This uses the setter with validation
        return f"Radius updated to {self._radius}"


if __name__ == '__main__':
    circle = Circle(5)

    # Method 1: Using property setter directly
    circle.radius = 10
    print(f"Radius: {circle.radius}")  # 10

    # Method 2: Using __call__ to set radius
    print(circle(15))  # "Radius updated to 15"
    print(f"Radius: {circle.radius}")  # 15

    # Both methods validate the input
    try:
        circle(-1)  # Will raise ValueError
    except ValueError as e:
        print(f"Error: {e}")  # "Error: Radius Cannot be Negative"


class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius Cannot be Negative")
        self._radius = value

    def __call__(self, new_radius):
        self.radius = new_radius
        return self  # Return self for chaining

    def __repr__(self):
        return f"Circle(radius={self._radius})"


# Usage
circle = Circle(5)
print(circle(10)(15)(20))  # Method chaining! → Circle(radius=20)