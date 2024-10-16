from dataclasses import dataclass

from product import Product


@dataclass
class ApiResponse:
    prducts: list[Product]
    total: int
    skip: int
    limit: int