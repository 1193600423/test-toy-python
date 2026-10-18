import pytest

from toy_orders import paginate


def test_exact_pages():
    result = paginate([1, 2, 3, 4], page=2, page_size=2)
    assert result.items == (3, 4)
    assert result.total_items == 4
    assert result.total_pages == 2
    assert result.number == 2
    assert result.page_size == 2


def test_empty_and_out_of_range():
    assert paginate([]).total_pages == 0
    assert paginate([1, 2], page=3, page_size=1).items == ()


@pytest.mark.parametrize("page,size", [(0, 1), (1, 0), (-1, 2), (1, 1.5), (True, 1)])
def test_invalid_pagination(page, size):
    with pytest.raises(ValueError):
        paginate([], page=page, page_size=size)
