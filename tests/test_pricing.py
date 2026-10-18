import pytest

from toy_orders import apply_discount


def test_half_price():
    assert apply_discount(1000, 50) == 500


def test_zero_amount():
    assert apply_discount(0, 25) == 0


@pytest.mark.parametrize("amount,percent", [(-1, 10), (100, -1), (100, 101), (1.5, 10), (100, True)])
def test_invalid_discount(amount, percent):
    with pytest.raises(ValueError):
        apply_discount(amount, percent)
