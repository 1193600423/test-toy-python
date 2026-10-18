"""One-based pagination of in-memory sequences."""

from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: tuple[T, ...]
    number: int
    page_size: int
    total_items: int
    total_pages: int


def paginate(items: Sequence[T], page: int = 1, page_size: int = 10) -> Page[T]:
    """Return a page; empty input has zero pages, out-of-range pages are empty."""
    if type(page) is not int or page < 1:
        raise ValueError("page must be a positive integer")
    if type(page_size) is not int or page_size < 1:
        raise ValueError("page_size must be a positive integer")
    start = (page - 1) * page_size
    return Page(
        items=tuple(items[start : start + page_size]),
        number=page,
        page_size=page_size,
        total_items=len(items),
        total_pages=len(items) // page_size,
    )
