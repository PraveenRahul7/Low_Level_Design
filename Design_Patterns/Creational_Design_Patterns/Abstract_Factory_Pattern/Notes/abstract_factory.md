---

## 🧠 Abstract Factory Pattern — Notes

### 🔹 Definition

> **Abstract Factory** is a **creational design pattern** that provides an interface for creating **families of related or dependent objects** without specifying their concrete classes.

---

### 🧩 Participants

| Role              | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| `AbstractFactory` | Declares interfaces for creating abstract products         |
| `ConcreteFactory` | Implements creation methods for a specific product family  |
| `AbstractProduct` | Interface/type for product objects (e.g., `RequestParser`) |
| `ConcreteProduct` | Specific implementation for a product                      |
| `Client`          | Uses factory to create and use products via abstract types |

---

### 🔄 Flow (PayGate Example)

```
Client
 └── uses → PayGateFactory (Abstract)
           ├── WellsFargoFactory (Concrete)
           │     ├── WellsFargoRequestParser
           │     └── WellsFargoResponseBuilder
           └── ChaseFactory (Concrete)
                 ├── ChaseRequestParser
                 └── ChaseResponseBuilder
```
* The first thing the Abstract Factory pattern suggests is to explicitly declare interfaces for each distinct product of the product family (e.g., chair, sofa or coffee table). Then you can make all variants of products follow those interfaces. For example, all chair variants can implement the Chair interface; all coffee table variants can implement the CoffeeTable interface, and so on.
* The next move is to declare the Abstract Factory—an interface with a list of creation methods for all products that are part of the product family (for example, createChair, createSofa and createCoffeeTable). These methods must return abstract product types represented by the interfaces we extracted previously: Chair, Sofa, CoffeeTable and so on.
* Now, how about the product variants? For each variant of a product family, we create a separate factory class based on the AbstractFactory interface. A factory is a class that returns products of a particular kind. For example, the ModernFurnitureFactory can only create ModernChair, ModernSofa and ModernCoffeeTable objects.
* The client code has to work with both factories and products via their respective abstract interfaces. This lets you change the type of a factory that you pass to the client code, as well as the product variant that the client code receives, without breaking the actual client code.
---

### 🧰 When to Use

* When you need to create **related objects** together.
* Use the Abstract Factory when your code needs to work with various families of related products, but you don’t want it to depend on the concrete classes of those products—they might be unknown beforehand or you simply want to allow for future extensibility.
*  Consider implementing the Abstract Factory when you have a class with a set of Factory Methods that blur its primary responsibility.
* When families of objects should be **used together** (e.g., Parser + ResponseBuilder).
* When you want to **decouple the client** from knowing which class it is instantiating.

---

## 🆚 Abstract Factory vs Factory Method (aka Plain Factory)

| Feature                    | **Abstract Factory**                                    | **Factory Method**                           |
| -------------------------- | ------------------------------------------------------- | -------------------------------------------- |
| Purpose                    | Creates **families of related objects**                 | Creates **one product type**                 |
| Structure                  | Uses **multiple factories** producing multiple products | Uses **a single method** to create a product |
| Flexibility                | High — can enforce compatible families                  | Moderate — only handles one product type     |
| Use case example           | Parser + ResponseBuilder for a gateway                  | Just a single Parser for a gateway           |
| Client knows concrete type | **No**                                                  | Often needs to know product variations       |

---

### ✅ Quick Analogy

Imagine a **furniture factory**:

* Abstract Factory: Builds a **chair + sofa + table** — all in **Victorian** or **Modern** style.
* Factory Method: Only builds **a chair**, depending on config (e.g., VictorianChair or ModernChair).

---

### 💡 Benefits of Abstract Factory

* Enforces **consistency** between products.
* Makes adding new product families **easy**.
* Promotes **dependency inversion** — code depends on abstractions, not concretes.

---

### ⚠️ Drawbacks

* Can get **complex** with many products and factories.
* Adding a new product type across all factories requires updating every factory.

---

