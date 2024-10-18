import attrs


@attrs.define
class SolutionItem:
    url: str
    name: str
    brand: str
    sku: str
    price: str
    rating: float
    reviews: int
