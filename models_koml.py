from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)
class Product:
    name: str
    price: float

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Product.price must be >= 0")

    def __str__(self) -> str:
        return f"{self.name} — {self.price:.2f}€"

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price:.2f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price == other.price

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price


@dataclass(frozen=True)
class Discount:
    description: str
    discount_percent: float

    def __post_init__(self) -> None:
        if not (0 <= self.discount_percent <= 100):
            raise ValueError("Discount.discount_percent must be in [0..100]")

    def __str__(self) -> str:
        return f"{self.description} (-{self.discount_percent:.0f}%)"

    def __repr__(self) -> str:
        return f"Discount(description={self.description!r}, discount_percent={self.discount_percent:.2f})"

    @staticmethod
    def price_with_discount(price: float, discount_percent: float) -> float:
        if price < 0:
            raise ValueError("price must be >= 0")
        if not (0 <= discount_percent <= 100):
            raise ValueError("discount_percent must be in [0..100]")
        return price * (1 - discount_percent / 100)

    @staticmethod
    def seasonal(percent: float) -> "Discount":
        return Discount("Seasonal discount", percent)

    @staticmethod
    def promo_code(code: str) -> "Discount":
        codes = {
            "WELCOME": 10,
            "NY2026": 15,
            "VIP": 20,
        }
        percent = float(codes.get(code.upper(), 0))
        desc = f"Promo code {code.upper()}" if percent else f"Promo code {code.upper()} (0%)"
        return Discount(desc, percent)

    @staticmethod
    def bulk_order(subtotal: float) -> "Discount":
        if subtotal >= 300:
            return Discount("Bulk order discount", 12)
        if subtotal >= 150:
            return Discount("Bulk order discount", 7)
        return Discount("Bulk order discount", 0)


@dataclass
class Order:
    products: list[Product] = field(default_factory=list)
    discounts: list[Discount] = field(default_factory=list)

    _registry: ClassVar[list["Order"]] = []

    def __post_init__(self) -> None:
        Order._registry.append(self)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def add_discount(self, discount: Discount) -> None:
        self.discounts.append(discount)

    @property
    def subtotal(self) -> float:
        return sum(p.price for p in self.products)

    @property
    def total(self) -> float:
        total = self.subtotal
        for d in self.discounts:
            total = Discount.price_with_discount(total, d.discount_percent)
        return round(total, 2)

    def __str__(self) -> str:
        items = ", ".join(p.name for p in self.products) if self.products else "—"
        disc = ", ".join(str(d) for d in self.discounts) if self.discounts else "без скидок"
        return f"Order[{items}] | {disc} | subtotal: {self.subtotal:.2f}€ -> total: {self.total:.2f}€"

    def __repr__(self) -> str:
        return f"Order(products={self.products!r}, discounts={self.discounts!r})"

    @classmethod
    def total_orders(cls) -> int:
        return len(cls._registry)

    @classmethod
    def total_revenue(cls) -> float:
        return round(sum(o.total for o in cls._registry), 2)


@dataclass
class Customer:
    name: str
    orders: list[Order] = field(default_factory=list)

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def __str__(self) -> str:
        return f"Customer({self.name}, orders={len(self.orders)})"

    def __repr__(self) -> str:
        return f"Customer(name={self.name!r}, orders={self.orders!r})"
