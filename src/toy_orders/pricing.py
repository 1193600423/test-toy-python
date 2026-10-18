"""Price calculations use integer cents and whole percentage points."""


def apply_discount(amount_cents: int, percent: int) -> int:
    """Return the amount payable after discount; round down to whole cents."""
    if type(amount_cents) is not int or amount_cents < 0:
        raise ValueError("amount_cents must be a nonnegative integer")
    if type(percent) is not int or not 0 <= percent <= 100:
        raise ValueError("percent must be an integer between 0 and 100")
    return amount_cents * percent // 100
