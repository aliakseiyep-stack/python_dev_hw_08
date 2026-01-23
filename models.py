class Product:
    def __init__(self, name: str, price: float):
        if price < 0:
            raise ValueError("price must be >= 0")
        self.name = name
        self.price = float(price)

    def __str__(self) -> str:
        return f"{self.name} ({self.price:.2f}€)"

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price:.2f})"

    # сравнение по цене
    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price == other.price

    def __lt__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price


class Discount:
    def __init__(self, description: str, discount_percent: float):
        if not (0 <= discount_percent <= 100):
            raise ValueError("discount_percent must be in [0..100]")
        self.description = description
        self.discount_percent = float(discount_percent)

    def __str__(self) -> str:
        return f"{self.description} (-{self.discount_percent:.0f}%)"

    def __repr__(self) -> str:
        return f"Discount(description={self.description!r}, discount_percent={self.discount_percent:.2f})"

    @staticmethod
    def price_with_discount(price: float, discount_percent: float) -> float:
        """Базовый расчёт цены со скидкой."""
        return round(price * (1 - discount_percent / 100), 2)

    @staticmethod
    def seasonal_10() -> "Discount":
        """Сезонная скидка 10%."""
        return Discount("Seasonal discount", 10)

    @staticmethod
    def for_product(product_name: str, percent: float) -> "Discount":
        """Скидка на конкретный товар."""
        return Discount(f"Product discount: {product_name}", percent)


class Order:
    _all_orders = []  # реестр всех заказов (для classmethod)

    def __init__(self):
        self.products = []
        self._seasonal_discount = None          # Discount или None
        self._product_discounts = {}            # product_name -> Discount
        Order._all_orders.append(self)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def set_seasonal_discount(self) -> None:
        self._seasonal_discount = Discount.seasonal_10()

    def set_product_discount(self, product_name: str, percent: float) -> None:
        # 5..10 по твоему условию (но можно и шире — оставим проверку мягкой)
        self._product_discounts[product_name] = Discount.for_product(product_name, percent)

    def subtotal(self) -> float:
        return round(sum(p.price for p in self.products), 2)

    def total(self) -> float:
        # 1) скидки на товары
        total = 0.0
        for p in self.products:
            d = self._product_discounts.get(p.name)
            if d:
                total += Discount.price_with_discount(p.price, d.discount_percent)
            else:
                total += p.price

        total = round(total, 2)

        # 2) сезонная на весь заказ
        if self._seasonal_discount:
            total = Discount.price_with_discount(total, self._seasonal_discount.discount_percent)

        return round(total, 2)

    def __str__(self) -> str:
        items = ", ".join(p.name for p in self.products) if self.products else "—"

        product_discounts = ", ".join(
            f"{name}(-{d.discount_percent:.0f}%)" for name, d in self._product_discounts.items()
        ) or "нет"

        seasonal = str(self._seasonal_discount) if self._seasonal_discount else "нет"

        return (
            f"Order: [{items}] | "
            f"product discounts: {product_discounts} | "
            f"seasonal: {seasonal} | "
            f"subtotal: {self.subtotal():.2f}€ -> total: {self.total():.2f}€"
        )

    def __repr__(self) -> str:
        return f"Order(products={self.products!r})"

    @classmethod
    def total_orders(cls) -> int:
        return len(cls._all_orders)

    @classmethod
    def total_sum(cls) -> float:
        return round(sum(o.total() for o in cls._all_orders), 2)


class Customer:
    def __init__(self, name: str):
        self.name = name
        self.orders = []

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def __str__(self) -> str:
        return f"Customer: {self.name} (orders: {len(self.orders)})"

    def __repr__(self) -> str:
        return f"Customer(name={self.name!r}, orders={self.orders!r})"
