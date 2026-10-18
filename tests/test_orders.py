import pytest

from toy_orders import OrderLine, order_total


def test_single_unit_lines():
    lines = [OrderLine("book", 1000), OrderLine("pen", 200)]
    assert lines[0].total_cents == 1000
    assert order_total(lines, shipping_cents=100) == 1300


def test_empty_order():
    assert order_total([]) == 0
    assert order_total([], shipping_cents=100) == 100


@pytest.mark.parametrize("sku,price,quantity", [("", 1, 1), ("a", -1, 1), ("a", 1, 0), ("a", 1, True)])
def test_invalid_line(sku, price, quantity):
    with pytest.raises(ValueError):
        OrderLine(sku, price, quantity)


def test_invalid_shipping():
    with pytest.raises(ValueError):
        order_total([], shipping_cents=-1)
