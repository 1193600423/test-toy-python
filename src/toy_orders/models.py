"""Order data and per-line calculations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    sku: str
    unit_price_cents: int
    quantity: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.sku, str) or not self.sku.strip():
            raise ValueError("sku must be a nonempty string")
        if type(self.unit_price_cents) is not int or self.unit_price_cents < 0:
            raise ValueError("unit_price_cents must be a nonnegative integer")
        if type(self.quantity) is not int or self.quantity < 1:
            raise ValueError("quantity must be a positive integer")

    @property
    def total_cents(self) -> int:
        """Return the price of all units on this line."""
        return self.unit_price_cents
