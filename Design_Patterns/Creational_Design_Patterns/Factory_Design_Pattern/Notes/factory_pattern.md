The **Factory Design Pattern** is a **creational design pattern** that provides an interface for creating objects in a **superclass**, but allows **subclasses to alter the type of objects that will be created**.

### 📌 Key Idea:

Instead of instantiating classes directly using the `new` keyword (or constructor), you use a factory method to create objects. This makes your code more flexible, extensible, and easier to maintain.

---

### ✅ When to Use It:

* You have a **superclass** with multiple **subclasses**, and you want to **instantiate** one of the subclasses **based on input or configuration**.
* Use the Factory Method when you don’t know beforehand the exact types and dependencies of the objects your code should work with.
*  Use the Factory Method when you want to provide users of your library or framework with a way to extend its internal components.
* You want to **encapsulate object creation logic**.

---

### 🧱 Basic Structure (in Python):

```python
class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Drawing a Circle")

class Square(Shape):
    def draw(self):
        print("Drawing a Square")

class ShapeFactory:
    @staticmethod
    def get_shape(shape_type):
        if shape_type == "circle":
            return Circle() #returns object
        elif shape_type == "square":
            return Square() #returns object
        else:
            raise ValueError("Unknown shape type")

# Usage
shape = ShapeFactory.get_shape("circle")
shape.draw()  # Output: Drawing a Circle
```

---

### 🎯 Benefits:

* **Decouples** object creation from its usage.
* Makes code **easier to maintain** and **extend**.
* Supports **Open/Closed Principle** (open for extension, closed for modification).

Would you like to see how this applies in a real-world example like database connectors or payment gateways?
