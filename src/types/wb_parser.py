from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class WBParseProductResult:
    """
    1 product parsing result
    frozen=True for immutable
    """
    id: int
    name: str
    price: int
    sale_price: int
    brand: str
    rating: float
    feedbacks: int
    supplier: Optional[str]
    link: str
