from models import Customer, Discount, Order, Product


def demo() -> None:
    laptop = Product("Laptop", 1299.00)
    mouse = Product("Mouse", 29.90)
    keyboard = Product("Keyboard", 79.50)
    monitor = Product("Monitor", 249.00)

    print("Product сравнение по цене:")
    print("mouse < keyboard:", mouse < keyboard)
    print("monitor == другой монитор по цене:", monitor == Product("Monitor v2", 249.00))
    print()

    alice = Customer("Alice")
    bob = Customer("Bob")

    order1 = Order()
    order1.add_product(laptop)
    order1.add_product(mouse)

    # разные виды скидок
    order1.add_discount(Discount.seasonal(5))
    order1.add_discount(Discount.promo_code("WELCOME"))
    order1.add_discount(Discount.bulk_order(order1.subtotal))

    alice.add_order(order1)

    order2 = Order(products=[monitor, keyboard, mouse])
    order2.add_discount(Discount.promo_code("VIP"))
    bob.add_order(order2)

    print(alice)
    for o in alice.orders:
        print(" ", o)

    print(bob)
    for o in bob.orders:
        print(" ", o)

    print("\nСтатистика по всем заказам:")
    print("Total orders:", Order.total_orders())
    print("Total revenue:", f"{Order.total_revenue():.2f}€")


if __name__ == "__main__":
    demo()
