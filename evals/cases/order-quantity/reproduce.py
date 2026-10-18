from toy_orders import OrderLine, order_total

line = OrderLine("book", 1200, 3)
actual = order_total([line], shipping_cents=200)
print(f"line={line.total_cents}; order={actual}; expected=3600,3800")
assert line.total_cents == 3600
assert actual == 3800
