from toy_orders import paginate

result = paginate([1, 2, 3, 4, 5], page=3, page_size=2)
print(f"items={result.items}; total_pages={result.total_pages}; expected=3")
assert result.items == (5,)
assert result.total_pages == 3
