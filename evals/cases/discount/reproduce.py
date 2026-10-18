from toy_orders import apply_discount

actual = apply_discount(1000, 20)
print(f"payable={actual}; expected=800")
assert actual == 800
