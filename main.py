from models import Customer, Order, Product


def main():
    # продукты
    laptop = Product("Laptop", 1000)
    mouse = Product("Mouse", 40)
    keyboard = Product("Keyboard", 80)

    # проверим сравнение по цене (Product.__lt__/__eq__)
    print("Compare products by price:")
    print("mouse < keyboard:", mouse < keyboard)
    print("keyboard == 80€ product:", keyboard == Product("Any", 80))
    print()

    # клиенты
    alice = Customer("Alice")
    bob = Customer("Bob")

    # заказ 1: сезонная 10% + скидка на мышь 5%
    order1 = Order()
    order1.add_product(laptop)
    order1.add_product(mouse)
    order1.set_product_discount("Mouse", 5)
    order1.set_seasonal_discount()
    alice.add_order(order1)

    # заказ 2: только скидки на товары (Keyboard 10%, Mouse 7%)
    order2 = Order()
    order2.add_product(keyboard)
    order2.add_product(mouse)
    order2.set_product_discount("Keyboard", 10)
    order2.set_product_discount("Mouse", 7)
    bob.add_order(order2)

    # вывод через dunder __str__
    print(alice)
    for o in alice.orders:
        print(" ", o)

    print(bob)
    for o in bob.orders:
        print(" ", o)

    # classmethod в Order
    print("\nAll orders stats:")
    print("Total orders:", Order.total_orders())
    print("Total sum:", f"{Order.total_sum():.2f}€")


if __name__ == "__main__":
    main()
