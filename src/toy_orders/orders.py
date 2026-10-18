"""Order aggregation."""

from collections.abc import Iterable

from .models import OrderLine


def order_total(lines: Iterable[OrderLine], shipping_cents: int = 0) -> int:
    """Sum line totals, then add shipping once; do not apply discounts."""
    if type(shipping_cents) is not int or shipping_cents < 0:
        raise ValueError("shipping_cents must be a nonnegative integer")
    return sum(line.unit_price_cents for line in lines) + shipping_cents
