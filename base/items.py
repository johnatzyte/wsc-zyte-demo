import attrs

@attrs.define
class ProductItem:
    name: str
    price: float
    sku: str
    url: str


@attrs.define
class CategoryItem:
    book_urls: list[str]
    next_page_url: str