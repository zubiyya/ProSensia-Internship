from inventory_utils import restock_product
import random

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} | Rs. {self.price} | Qty: {self.quantity} | Total: Rs. {self.total_value():.2f}"

class PerishableProduct(Product):
    def __init__(self, name, price, quantity, expiry_days):
        super().__init__(name, price, quantity)
        self.expiry_days = expiry_days

    def total_value(self):
        total = super().total_value()
        if self.expiry_days < 5:
            return total * 0.8
        return total

    def __str__(self):
        return f"{super().__str__()} | Expires in: {self.expiry_days} days"

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def list_inventory(self):
        for i, product in enumerate(self.products, 1):
            print(f"{i}. {product}")

    def search_by_name(self, term):
        return list(filter(lambda p: term.lower() in p.name.lower(), self.products))

    def restock_all(self):
        for product in self.products:
            restock_product(product)

    def export_summary(self, filename="inventory_report.txt"):
        with open(filename, "w") as f:
            for i, product in enumerate(self.products, 1):
                f.write(f"{i}. {product}\n")
            total = sum(p.total_value() for p in self.products)
            f.write(f"\nTotal Inventory Value: Rs. {total:.2f}\n")

if __name__ == "__main__":
    manager = InventoryManager()
    manager.add_product(Product("Shampoo", 120, 10))
    manager.add_product(PerishableProduct("Milk", 80, 5, 2))
    manager.add_product(PerishableProduct("Yogurt", 70, 4, 7))

    print("\n📦 Initial Inventory:")
    manager.list_inventory()

    print("\n🔍 Search for 'milk':")
    for p in manager.search_by_name("milk"):
        print(p)

    print("\n🔁 Restocking all products...")
    manager.restock_all()

    print("\n📦 Inventory After Restock:")
    manager.list_inventory()

    print("\n💾 Writing inventory_report.txt...")
    manager.export_summary()
    print("✅ Report saved.")